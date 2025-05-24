// src/pages/Home.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home-page">
      <h1>🎧 AI Sound Recognition Dashboard</h1>
      <p>Monitor. Detect. Respond – in Real Time.</p>

      <div className="home-buttons">
        <button onClick={() => navigate('/dashboard')}>Go to Dashboard</button>
        <button onClick={() => navigate('/custom-sounds')}>Custom Sounds</button>
        <button onClick={() => navigate('/alerts')}>Alerts</button>
        <button onClick={() => navigate('/events')}>Events Log</button>
        <button onClick={() => navigate('/settings')}>Settings</button>
        <button onClick={() => navigate('/login')}>Login</button>
        <button onClick={() => navigate('/register')}>Register</button>
      </div>
    </div>
  );
};

export default Home;
