import React from 'react';
import UserProfileForm from '../components/UserProfileForm';
import DeviceManagement from '../components/DeviceManagement';
import SystemPreferences from '../components/SystemPreferences';

import '../styles/Settings.css';
import Header from '../components/Header'; // Import Header

const Settings = () => {
  return (
    <div className="page settings-page">
      <Header /> {/* Add Header here */}
      <h2>⚙️ Settings</h2>
      <UserProfileForm />
      <DeviceManagement />
      <SystemPreferences />
    </div>
  );
};

export default Settings;
