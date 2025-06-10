// src/pages/Alerts.jsx
import React from 'react';
import AlertSettingsForm from '../components/AlertSettingsForm';
import AlertHistory from '../components/AlertHistory';
import DeviceAlertChannels from '../components/DeviceAlertChannels';
import '../styles/Alerts.css';
import Header from '../components/Header';

const Alerts = () => {
  return (
    <div className="page alerts-page">
      <Header />
      <h2>🔔 Alerts & Notifications</h2>
      <div className="alerts-grid">
        <AlertSettingsForm />
        <AlertHistory />
        <DeviceAlertChannels />
      </div>
    </div>
  );
};

export default Alerts;
