// src/components/DeviceManagement.jsx
import React from 'react';
import '../styles/DeviceManagement.css';

const DeviceManagement = () => {
  return (
    <div className="device-management">
      <h3>🔌 Device Management</h3>
      <p>Connected Devices:</p>
      <ul>
        <li>Mic A – Online</li>
        <li>Mic B – Offline</li>
      </ul>
      <button>Add New Device</button>
    </div>
  );
};

export default DeviceManagement;
