// src/components/Sidebar.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Sidebar.css';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <Link to="/dashboard">📊 Dashboard</Link>
      <Link to="/custom-sounds">🎵 Custom Sounds</Link>
      <Link to="/alerts">🚨 Alerts</Link>
      <Link to="/events">🗃️ Event Logs</Link>
      <Link to="/settings">⚙️ Settings</Link>
    </aside>
  );
};

export default Sidebar;
