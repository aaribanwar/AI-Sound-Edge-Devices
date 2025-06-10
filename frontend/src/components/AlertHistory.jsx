import React from 'react';
import '../styles/Alerts.css';

const AlertHistory = () => {
  const sampleAlerts = [
    { time: '2025-05-21 10:00', message: 'Loud sound detected near Device A' },
    { time: '2025-05-21 09:20', message: 'Device B triggered threshold alert' },
  ];

  return (
    <div className="alert-card">
      <h3>📜 Alert History</h3>
      <ul>
        {sampleAlerts.map((alert, index) => (
          <li key={index}>
            <strong>{alert.time}</strong>: {alert.message}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AlertHistory;
