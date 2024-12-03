import React, { useState, useEffect } from 'react';
import { fetchPlayersAPI, deletePlayerAPI, addPlayersAPI } from '../services/api';

const PlayerList = () => {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [gameName, setGameName] = useState('');
  const [tagLine, setTagLine] = useState('');

  // Fetch players when the component loads
  const fetchPlayers = () => {
    setLoading(true);
    fetchPlayersAPI()
      .then((response) => {
        setPlayers(response.data.players || []);
        setError('');
      })
      .catch((err) => {
        setError(err.response?.data?.error || 'An error occurred');
      })
      .finally(() => {
        setLoading(false);
      });
  };

  // Delete a player
  const deletePlayer = (playerName) => {
    deletePlayerAPI(playerName)
      .then(() => {
        fetchPlayers(); // Refresh players after deletion
      })
      .catch((err) => {
        setError(err.response?.data?.error || 'An error occurred');
      });
  };

  const addPlayers = (gameName, tagLine) => {
    if (gameName == '' || tagLine == '') {
      console.error('Error: gameName and tagLine must be populated');
      alert('Please populate both "Summoner Name" and "Tag Line" before adding players');
      return;
    }
    addPlayersAPI(gameName, tagLine)
      .then(() => {
        fetchPlayers();
      })
      .catch((err) => {
        setError(err.response?.data?.error || 'An error occurred');
      });
  }

  // Initial fetch when the component mounts
  useEffect(() => {
    fetchPlayers();
  }, []);

  const handleUpdateButton = () => {
    console.log('Game Name:', gameName);
    console.log('Tag Line:', tagLine);

    // Add functionality here to use gameName and tagLine
  }
  return (
    <div>
      <h2>Summoners</h2>
      <input type="text" placeholder="Summoner Name" value={gameName} onChange={(e) => setGameName(e.target.value)}></input>
      <input type="text" placeholder="Tag Line" value={tagLine} onChange={(e) => setTagLine(e.target.value)}></input>
      <button type="button" onClick={handleUpdateButton}>Update Player Data</button>
      <h1>Summoners</h1>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p style={{ color: 'red' }}>{error}</p>
      ) : (
        <ul>
          {players.map((player, index) => (
            <li key={index}>
              {player}{' '}
              <button
                type="button"
                onClick={() => deletePlayer(player)}
              >
                Delete Player
              </button>
            </li>
          ))}
        </ul>
      )}
      <button
        type="button"
        onClick={() => addPlayers(gameName, tagLine)}
      >
        Add Players
      </button>
    </div>
  );
};

export default PlayerList;
