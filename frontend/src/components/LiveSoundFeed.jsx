// src/components/LiveSoundFeed.jsx
import React from 'react';
import '../styles/LiveSoundFeed.css';

const LiveSoundFeed = () => {
  return (
    <div className="card live-feed">
      <h3>🎧 Live Sound Feed</h3>
      <div className="feed-log">
        <p>[12:01] Barking detected</p>
        <p>[12:02] Glass breaking detected</p>
        <p>[12:03] Unknown sound</p>
      </div>
    </div>
  );
};

export default LiveSoundFeed;
