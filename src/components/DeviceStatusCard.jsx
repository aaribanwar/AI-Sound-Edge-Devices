// src/components/DeviceStatusCard.jsx
import React from 'react';
import '../styles/DeviceStatusCard.css';

const DeviceStatusCard = () => {
  return (
    <div className="card device-status">
      <h3>📟 Device Status</h3>
      <ul>
        <li><strong>Device A:</strong> 🟢 Online (Last Active: 12:20)</li>
        <li><strong>Device B:</strong> 🔴 Offline (Last Active: 11:55)</li>
      </ul>
    </div>
  );
};

export default DeviceStatusCard;
