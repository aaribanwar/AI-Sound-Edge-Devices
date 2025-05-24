// src/components/SoundPlayPreview.jsx
import React from 'react';
import '../styles/SoundPlayPreview.css';

const SoundPlayPreview = () => {
  return (
    <div className="card sound-play-preview">
      <h3>▶️ Preview Sound</h3>
      <audio controls>
        <source src="/example.mp3" type="audio/mp3" />
        Your browser does not support the audio element.
      </audio>
    </div>
  );
};

export default SoundPlayPreview;
