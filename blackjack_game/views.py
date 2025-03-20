import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404

from blackjack_game.utils import calculate_score, log_game_history
from .models import GameHistory, GameSession

DECK_API_URL = "https://deckofcardsapi.com/api/deck"

def start_game(request):
    response = requests.get(f"{DECK_API_URL}/new/shuffle/?deck_count=1")
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch deck"}, status=500)

    data = response.json()
    deck_id = data["deck_id"]

    # Draw initial 4 cards (2 for player, 2 for dealer)
    draw_response = requests.get(f"{DECK_API_URL}/{deck_id}/draw/?count=4")
    if draw_response.status_code != 200:
        return JsonResponse({"error": "Failed to draw initial cards"}, status=500)

    draw_data = draw_response.json()
    cards = draw_data["cards"]

    player_hand = [cards[0], cards[2]]
    dealer_hand = [cards[1], cards[3]]  # Dealer’s second card is hidden

    # Save game session
    session = GameSession.objects.create(
        deck_id=deck_id,
        player_hand=player_hand,
        dealer_hand=[dealer_hand[0]],  # Only show one card for now
        game_state="PLAYER_TURN"
    )

    return JsonResponse({
        "message": "Blackjack game started!",
        "session_id": str(session.session_id),
        "deck_id": deck_id,
        "player_hand": player_hand,
        "dealer_hand": [dealer_hand[0]],  # Hide second card
        "game_state": session.game_state
    })

def game_state(request, session_id):
    session = get_object_or_404(GameSession, session_id=session_id)

    return JsonResponse({
        "session_id": str(session.session_id),
        "player_hand": session.player_hand,
        "dealer_hand": session.dealer_hand,
        "game_state": session.game_state
    })
    
def hit(request, session_id):
    session = get_object_or_404(GameSession, session_id=session_id)

    if session.game_state != "PLAYER_TURN":
        return JsonResponse({"error": "Invalid action"}, status=400)

    # Draw a card from the deck
    draw_response = requests.get(f"{DECK_API_URL}/{session.deck_id}/draw/?count=1")
    if draw_response.status_code != 200:
        return JsonResponse({"error": "Failed to draw a card"}, status=500)

    card = draw_response.json()["cards"][0]
    session.player_hand.append(card)  # Add card to player’s hand
    session.save()

    # Check if player busts
    player_score = calculate_score(session.player_hand)
    if player_score > 21:
        session.game_state = "GAME_OVER"
        session.save()

        log_game_history(session, player_score, 0, 'dealer_wins')
        
        return JsonResponse({
            "message": "Player busted!",
            "player_hand": session.player_hand,
            "game_state": session.game_state
        })

    return JsonResponse({
        "message": "Player drew a card",
        "player_hand": session.player_hand,
        "game_state": session.game_state
    })

def dealer_play(deck_id, dealer_hand):
    while calculate_score(dealer_hand) < 17:
        draw_response = requests.get(f"{DECK_API_URL}/{deck_id}/draw/?count=1")
        if draw_response.status_code != 200:
            return None  # Handle error gracefully

        dealer_hand.append(draw_response.json()["cards"][0])

    return dealer_hand

def stand(request, session_id):
    session = get_object_or_404(GameSession, session_id=session_id)

    if session.game_state != "PLAYER_TURN":
        return JsonResponse({"error": "Invalid action"}, status=400)

    # Reveal dealer's full hand
    dealer_hand = session.dealer_hand
    session.dealer_hand = dealer_play(session.deck_id, dealer_hand)
    session.game_state = "GAME_OVER"
    session.save()

    # Determine winner
    player_score = calculate_score(session.player_hand)
    dealer_score = calculate_score(session.dealer_hand)

    if dealer_score > 21 or player_score > dealer_score:
        result = "Player wins!"
        outcome = 'player_wins'
    elif player_score == dealer_score:
        result = "It's a tie!"
        outcome = 'draw'
    else:
        result = "Dealer wins!"
        outcome = 'dealer_wins'

    # Log the game result
    log_game_history(session, player_score, dealer_score, outcome)

    return JsonResponse({
        "message": result,
        "player_hand": session.player_hand,
        "dealer_hand": session.dealer_hand,
        "game_state": session.game_state
    })

def restart_game(request, session_id):
    session = get_object_or_404(GameSession, session_id=session_id)

    # Save the current game history before restarting
    player_score = calculate_score(session.player_hand)
    dealer_score = calculate_score(session.dealer_hand)

    log_game_history(session, player_score, dealer_score, 'game_restarted')

    # Shuffle the deck
    shuffle_response = requests.get(f"{DECK_API_URL}/{session.deck_id}/shuffle/")
    if shuffle_response.status_code != 200:
        return JsonResponse({"error": "Failed to shuffle deck"}, status=500)

    # Reset hands
    session.player_hand = []
    session.dealer_hand = []

    # Draw initial cards
    draw_response = requests.get(f"{DECK_API_URL}/{session.deck_id}/draw/?count=4")
    if draw_response.status_code != 200:
        return JsonResponse({"error": "Failed to draw cards"}, status=500)

    cards = draw_response.json()["cards"]
    session.player_hand = [cards[0], cards[2]]  # Player gets two cards
    session.dealer_hand = [cards[1], cards[3]]  # Dealer gets two cards

    # Reset game state
    session.game_state = "PLAYER_TURN"
    session.save()

    return JsonResponse({
        "message": "Game restarted",
        "player_hand": session.player_hand,
        "dealer_hand": [session.dealer_hand[0], {"value": "Hidden", "suit": "Hidden"}],  # Hide second dealer card
        "game_state": session.game_state
    })

def get_game_history(request, session_id):
    """
    Fetches the game history for a given session_id.
    """
    history_entries = get_list_or_404(GameHistory, session_id=session_id)

    # Serialize history entries
    history_data = [
        {
            "player_hand": entry.player_hand,
            "dealer_hand": entry.dealer_hand,
            "player_score": entry.player_score,
            "dealer_score": entry.dealer_score,
            "outcome": entry.outcome,
            "timestamp": entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for entry in history_entries
    ]

    return JsonResponse({"session_id": session_id, "history": history_data})