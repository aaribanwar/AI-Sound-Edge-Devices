import React from 'react';
import '../styles/Alerts.css';

const AlertSettingsForm = () => {
  return (
    <div className="alert-card">
      <h3>📋 Alert Settings</h3>
      <form>
        <label>
          Alert Threshold:
          <input type="number" min="0" placeholder="Enter threshold" />
        </label>
        <label>
          Alert Type:
          <select>
            <option>Email</option>
            <option>SMS</option>
            <option>Push Notification</option>
          </select>
        </label>
        <button type="submit">Save Settings</button>
      </form>
    </div>
  );
};

export default AlertSettingsForm;
