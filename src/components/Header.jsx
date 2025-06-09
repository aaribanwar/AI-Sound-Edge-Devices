// src/components/Header.jsx
import React from 'react';
import { useTheme } from '../context/ThemeContext';
import '../styles/Header.css';

const Header = () => {
  const { darkMode, setDarkMode } = useTheme();

  return (
    <header className="header">
      <h1>Sound Detection System</h1>
      <nav>
        <a href="/dashboard">Dashboard</a>
        <a href="/custom-sounds">Custom Sounds</a>
        <a href="/alerts">Alerts</a>
        <a href="/events">Events</a>
        <a href="/settings">Settings</a>
      </nav>
      <button className="theme-toggle" onClick={() => setDarkMode(!darkMode)}>
        {darkMode ? '☀️ Light' : '🌙 Dark'}
      </button>
    </header>
  );
};

export default Header;
