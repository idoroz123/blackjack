import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api"; // Update if needed

export const startGame = async () => {
  const response = await axios.get(`${API_BASE_URL}/start_game/`);
  return response.data;
};

export const getGameState = async (sessionId: string) => {
  const response = await axios.get(`${API_BASE_URL}/game_state/${sessionId}/`);
  return response.data;
};

export const hit = async (sessionId: string) => {
  const response = await axios.get(`${API_BASE_URL}/hit/${sessionId}/`);
  return response.data;
};

export const stand = async (sessionId: string) => {
  const response = await axios.get(`${API_BASE_URL}/stand/${sessionId}/`);
  return response.data;
};

export const restartGame = async (sessionId: string) => {
  const response = await axios.get(`${API_BASE_URL}/restart/${sessionId}/`);
  return response.data;
};

export const fetchGameHistory = async (sessionId: string) => {
  const response = await axios.get(`${API_BASE_URL}/history/${sessionId}/`);
  return response.data;
};
