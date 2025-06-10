// src/components/EventDetailsModal.jsx
import React from 'react';
import '../styles/EventDetailsModal.css';

const EventDetailsModal = ({ event, onClose }) => {
  if (!event) return null;

  return (
    <div className="modal-overlay">
      <div className="event-details-modal">
        <h3>📝 Event Details</h3>
        <p><strong>Type:</strong> {event.type}</p>
        <p><strong>Confidence:</strong> {event.confidence}%</p>
        <p><strong>Time:</strong> {event.time}</p>
        <p><strong>Device:</strong> {event.device || 'Mic A'}</p>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default EventDetailsModal;
