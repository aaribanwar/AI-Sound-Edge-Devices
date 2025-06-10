// src/components/SystemPreferences.jsx
import React from 'react';
import '../styles/SystemPreferences.css';

const SystemPreferences = () => {
  return (
    <div className="system-preferences">
      <h3>⚙️ System Preferences</h3>
      <label>
        Detection Sensitivity:
        <input type="range" min="1" max="10" defaultValue="5" />
      </label>
    </div>
  );
};

export default SystemPreferences;
