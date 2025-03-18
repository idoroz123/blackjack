def calculate_score(hand):
    values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
              "10": 10, "JACK": 10, "QUEEN": 10, "KING": 10, "ACE": 11}

    score = sum(values[card["value"]] for card in hand)
    num_aces = sum(1 for card in hand if card["value"] == "ACE")

    # Convert Aces from 11 to 1 if needed
    while score > 21 and num_aces:
        score -= 10
        num_aces -= 1

    return score

from datetime import datetime
from blackjack_game.models import GameHistory

def log_game_history(session, player_score, dealer_score, outcome):
    """
    Logs the game history in the GameHistory model.
    
    Args:
    - session: The current game session (GameSession object).
    - player_score: The final score of the player.
    - dealer_score: The final score of the dealer.
    - outcome: The result of the game (e.g., 'player_wins', 'dealer_wins', 'draw').
    """
    # Create a new game history entry
    GameHistory.objects.create(
        session_id=session.session_id,
        player_hand=session.player_hand,
        dealer_hand=session.dealer_hand,
        player_score=player_score,
        dealer_score=dealer_score,
        outcome=outcome,
        timestamp=datetime.now().isoformat()
    )