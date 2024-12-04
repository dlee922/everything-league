import React, { useState } from 'react';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:5000';

const LoginForm = ({ onLoginSuccess }) => {
  const [userName, setUserName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = () => {
    if (!userName || !password) {
      setError('Both username and password are required.');
      return;
    }

    axios
      .post(`${API_BASE}/api/login`, { userName, password })
      .then((response) => {
        const token = response.data.access_token;
        localStorage.setItem('token', token); // Store token in localStorage
        setError(''); // Clear any previous errors
        onLoginSuccess(token); // Notify parent component of successful login
      })
      .catch((err) => {
        setError(err.response?.data?.error || 'Invalid username or password');
      });
  };

  return (
    <div>
      <h2>Login</h2>
      <input
        type="text"
        placeholder="Username"
        value={userName}
        onChange={(e) => setUserName(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default LoginForm;
