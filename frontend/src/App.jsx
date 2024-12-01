import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [participants, setParticipants] = useState([]);
  const [loading, setLoading] = useState(false);

  const gameName = "Hanskyeul";
  const tagLine = "NA1";

    useEffect(() => {
    // Fetch participants when the component loads
    setLoading(true);
    axios
      .get(`/api/participants/${gameName}/${tagLine}`)
      .then((response) => {
        setParticipants(response.data.participants);
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

  return (
    <div style={{ padding: "20px" }}>
      <h1>Match Participants</h1>

      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p style={{ color: "red" }}>{error}</p>
      ) : (
        <ul>
          {participants.map((participant, index) => (
            <li key={index}>{participant}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;