import axios from 'axios';

const API_BASE = 'http://127.0.0.1:5000';

export const fetchPlayersAPI = () => {
  return axios.get(`${API_BASE}/api/players`);
};

export const deletePlayerAPI = (playerName) => {
  return axios.delete(`${API_BASE}/api/delete-player/${playerName}`);
};

export const addPlayersAPI = (gameName, tagLine) => {
    return axios.post(`${API_BASE}/api/add-players/${gameName}/${tagLine}`)
}