// src/components/AlertPanel.jsx
import React from 'react';
import '../styles/AlertPanel.css';

const AlertPanel = () => {
  return (
    <div className="card alert-panel">
      <h3>🚨 Live Alerts</h3>
      <ul>
        <li className="alert critical">[12:02] Glass breaking! (Critical)</li>
        <li className="alert warning">[12:01] Barking detected (Warning)</li>
        <li className="alert info">[12:00] Ambient noise (Info)</li>
      </ul>
    </div>
  );
};

export default AlertPanel;
