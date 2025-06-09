// src/components/CustomSoundList.jsx
import React from 'react';
import '../styles/CustomSoundList.css';

const CustomSoundList = () => {
  const sounds = [
    { name: 'Glass Breaking', date: '2025-05-20' },
    { name: 'Dog Barking', date: '2025-05-19' },
    { name: 'Siren', date: '2025-05-18' },
  ];

  return (
    <div className="card custom-sound-list">
      <h3>🎵 Trained Custom Sounds</h3>
      <ul>
        {sounds.map((sound, idx) => (
          <li key={idx}>
            <strong>{sound.name}</strong> <span>{sound.date}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomSoundList;
