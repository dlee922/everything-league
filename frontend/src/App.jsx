import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [playerToDelete, setPlayerToDelete] = useState('');
  const [gameName, setGameName] = useState('');
  const [tagLine, setTagLine] = useState('');

  useEffect(() => {
  // Fetch players when the component loads
  setLoading(true);
  axios
    .get(`/api/players`)
    .then((response) => {
      console.log('Response Data: ', response.data)
      console.log('Participants: ', response.data.players)
      setPlayers(response.data.players || []);
      setError("");
    })
    .catch((err) => {
      console.error(err);
      setError(err.response?.data?.error || "An error occurred");
    })
    .finally(() => {
      setLoading(false);
    });
  }, []);
  
  useEffect(() => {
  // For now: log player to delete when delete button is clicked
    if (playerToDelete) {
      console.log('Player to delete: ', playerToDelete);
    }
  }, [playerToDelete]);

  useEffect(() => {
    // Fetch players when the component loads
    if (playerToDelete) {
      axios
        .delete(`/api/delete-player/${playerToDelete}`)
        .then((response) => {
          setPlayerToDelete('');
          setError('');
        })
        .catch((err) => {
          console.error(err);
          setError(err.response?.data?.error || "An error occurred");
        })
    }
    else {
      console.warn('No selected player to delete')
    }
  }, [playerToDelete]);

  const handleUpdateButton = () => {
    console.log('Game Name:', gameName);
    console.log('Tag Line:', tagLine);

    // Add functionality here to use gameName and tagLine
  }
  
  return (
    <div style={{ padding: "20px" }}>
      <input type="text" placeholder="Summoner Name" value={gameName} onChange={(e) => setGameName(e.target.value)}></input>
      <input type="text" placeholder="Tag Line" value={tagLine} onChange={(e) => setTagLine(e.target.value)}></input>
      <button type="button" onClick={handleUpdateButton}>Update Player Data</button>
      <h1>Summoners</h1>

      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p style={{ color: "red" }}>{error}</p>
      ) : (
        <ul>
          {players.map((player, index) => (
            <li key={index}>{player}
            <button 
              type="button"
              onClick={() => {
                console.log(`Button clicked for player: ${player}, index: ${index}`)
                setPlayerToDelete(player)}
              }
              >Delete Player</button></li>
          ))}
        </ul>
      )}
    </div>
  );


}

export default App;