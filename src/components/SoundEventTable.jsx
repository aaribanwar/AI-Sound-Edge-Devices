// src/components/SoundEventTable.jsx
import React from 'react';
import '../styles/SoundEventTable.css';

const SoundEventTable = ({ events, onSelect }) => {
  return (
    <table className="sound-event-table">
      <thead>
        <tr>
          <th>Type</th>
          <th>Confidence</th>
          <th>Time</th>
        </tr>
      </thead>
      <tbody>
        {events.map((event, idx) => (
          <tr key={idx} onClick={() => onSelect(event)}>
            <td>{event.type}</td>
            <td>{event.confidence}%</td>
            <td>{event.time}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default SoundEventTable;
