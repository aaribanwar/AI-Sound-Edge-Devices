// src/components/SystemSummary.jsx
import React from 'react';
import '../styles/SystemSummary.css';

const SystemSummary = () => {
  return (
    <div className="card system-summary">
      <h3>📊 System Summary</h3>
      <div className="summary-grid">
        <div>
          <h4>🔊 Total Events</h4>
          <p>143</p>
        </div>
        <div>
          <h4>🎯 Custom Sounds</h4>
          <p>6</p>
        </div>
        <div>
          <h4>📅 Today</h4>
          <p>21 Events</p>
        </div>
      </div>
    </div>
  );
};

export default SystemSummary;
