import React, { useState } from 'react';
import PlayerList from './components/PlayerList';
import LoginForm from './components/LoginForm';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLoginSuccess = (token) => {
    console.log('Login successful, token:', token);
    setIsLoggedIn(true);
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Everything League</h1>
      {isLoggedIn ? (
        <PlayerList />
      ) : (
        <LoginForm onLoginSuccess={handleLoginSuccess} />
      )}
    </div>
  );
};

export default App;
