import { create } from "zustand";
import { startGame, hit, stand, restartGame, getGameState } from "../api/game";

interface Card {
  code: string;
  suit: string;
  value: string;
}

interface GameState {
  sessionId: string | null;
  playerHand: Card[];
  dealerHand: Card[];
  gameState: string;
  isLoading: boolean;
  startNewGame: () => Promise<void>;
  playerHit: () => Promise<void>;
  playerStand: () => Promise<void>;
  restartCurrentGame: () => Promise<void>;
  fetchGameState: () => Promise<void>;
}

export const useGameStore = create<GameState>((set, get) => ({
  sessionId: null,
  playerHand: [],
  dealerHand: [],
  gameState: "NOT_STARTED",
  isLoading: false,

  startNewGame: async () => {
    set({ isLoading: true });
    try {
      const data = await startGame();
      set({
        sessionId: data.session_id,
        playerHand: data.player_hand,
        dealerHand: data.dealer_hand,
        gameState: data.game_state,
      });
    } catch (error) {
      console.error("Failed to start game", error);
    } finally {
      set({ isLoading: false });
    }
  },

  fetchGameState: async () => {
    const { sessionId } = get();
    if (!sessionId) return;
    set({ isLoading: true });
    try {
      const data = await getGameState(sessionId);
      set({
        playerHand: data.player_hand,
        dealerHand: data.dealer_hand,
        gameState: data.game_state,
      });
    } catch (error) {
      console.error("Failed to fetch game state", error);
    } finally {
      set({ isLoading: false });
    }
  },

  playerHit: async () => {
    const { sessionId } = get();
    if (!sessionId) return;
    try {
      const data = await hit(sessionId);
      set({
        playerHand: data.player_hand,
        gameState: data.game_state,
      });
    } catch (error) {
      console.error("Failed to hit", error);
    }
  },

  playerStand: async () => {
    const { sessionId } = get();
    if (!sessionId) return;
    try {
      const data = await stand(sessionId);
      set({
        dealerHand: data.dealer_hand,
        gameState: data.game_state,
      });
    } catch (error) {
      console.error("Failed to stand", error);
    }
  },

  restartCurrentGame: async () => {
    const { sessionId } = get();
    if (!sessionId) return;
    set({ isLoading: true });
    try {
      const data = await restartGame(sessionId);
      set({
        playerHand: data.player_hand,
        dealerHand: data.dealer_hand,
        gameState: data.game_state,
      });
    } catch (error) {
      console.error("Failed to restart game", error);
    } finally {
      set({ isLoading: false });
    }
  },
}));
