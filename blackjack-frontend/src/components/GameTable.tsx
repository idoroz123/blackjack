import { motion } from "framer-motion";
import { useGameStore } from "../store/gameStore";
import { useEffect } from "react";
import "./GameTable.css";

const cardVariants = {
  initial: { opacity: 0, y: -20 },
  animate: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 200 } },
};

const GameTable = () => {
  const {
    sessionId,
    playerHand,
    dealerHand,
    gameState,
    startNewGame,
    playerHit,
    playerStand,
    fetchGameState,
  } = useGameStore();

  useEffect(() => {
    if (sessionId) fetchGameState();
  }, [sessionId, fetchGameState]);

  return (
    <div className="game-table">
      <h1 className="game-title">Blackjack</h1>

      {/* Dealer Cards */}
      <div className="card-container dealer-cards">
        {dealerHand.map((card, index) => (
          <motion.img
            key={index}
            src={`https://deckofcardsapi.com/static/img/${card.code}.png`}
            alt={card.value}
            className="card"
            variants={cardVariants}
            initial="initial"
            animate="animate"
          />
        ))}
      </div>

      {/* Game Controls */}
      <div className="controls">
        {!sessionId ? (
          <button onClick={startNewGame} className="btn start-btn">
            Start Game
          </button>
        ) : (
          <>
            {gameState === "PLAYER_TURN" && (
              <>
                <button onClick={playerHit} className="btn hit-btn">
                  Hit
                </button>
                <button onClick={playerStand} className="btn stand-btn">
                  Stand
                </button>
              </>
            )}
            {gameState === "GAME_OVER" && (
              <button onClick={startNewGame} className="btn start-btn">
                Start Game
              </button>
            )}
          </>
        )}
      </div>

      {/* Player Cards */}
      <div className="card-container player-cards">
        {playerHand.map((card, index) => (
          <motion.img
            key={index}
            src={`https://deckofcardsapi.com/static/img/${card.code}.png`}
            alt={card.value}
            className="card"
            variants={cardVariants}
            initial="initial"
            animate="animate"
          />
        ))}
      </div>

      {/* Game State Display */}
      {gameState !== "IN_PROGRESS" && sessionId && (
        <div className="game-state">{gameState}</div>
      )}
    </div>
  );
};

export default GameTable;
