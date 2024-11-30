import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    // Fetch data from Flask backend
    axios
      .get('/api/data') // Proxy sends this to Flask backend
      .then((response) => {
        setMessage(response.data.message);
        setError('');
      })
      .catch((err) => {
        console.error(err);
        setError('Failed to fetch data from backend.');
      });
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1>React + Flask Integration</h1>
      {error ? (
        <p style={{ color: 'red' }}>{error}</p>
      ) : (
        <p>{message || 'Loading...'}</p>
      )}
    </div>
  );
}

export default App;
