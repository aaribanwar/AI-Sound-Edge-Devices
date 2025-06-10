import React from 'react';
import CustomSoundList from '../components/CustomSoundList';
import NewCustomSoundForm from '../components/NewCustomSoundForm';
import SoundTrainingStatus from '../components/SoundTrainingStatus';
import SoundPlayPreview from '../components/SoundPlayPreview';

import '../styles/CustomSounds.css';
import Header from '../components/Header'; // Import Header

const CustomSounds = () => {
  return (
    <div className="page custom-sounds-page">
      <Header /> {/* Add Header here */}
      <h2>🎼 Custom Sounds Management</h2>
      <div className="custom-sounds-grid">
        <CustomSoundList />
        <NewCustomSoundForm />
        <SoundTrainingStatus />
        <SoundPlayPreview />
      </div>
    </div>
  );
};

export default CustomSounds;
