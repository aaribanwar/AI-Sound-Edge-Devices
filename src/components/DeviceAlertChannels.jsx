import React from 'react';
import '../styles/Alerts.css';

const DeviceAlertChannels = () => {
  return (
    <div className="alert-card">
      <h3>📡 Alert Channels</h3>
      <p>
        Configure which devices send alerts through which channels. More
        customization options coming soon!
      </p>
      <ul>
        <li>Device A: Email + Push</li>
        <li>Device B: SMS only</li>
      </ul>
    </div>
  );
};

export default DeviceAlertChannels;
