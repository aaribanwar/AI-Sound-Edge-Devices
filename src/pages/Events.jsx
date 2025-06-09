import React, { useState } from 'react';
import SearchBar from '../components/SearchBar';
import SoundEventTable from '../components/SoundEventTable';
import ExportLogsButton from '../components/ExportLogsButton';
import EventDetailsModal from '../components/EventDetailsModal';

import '../styles/Events.css';
import Header from '../components/Header';  // Import Header

const sampleEvents = [
  { type: 'Gunshot', confidence: 95, time: '2025-05-22 14:30' },
  { type: 'Scream', confidence: 88, time: '2025-05-22 13:10' },
];

const Events = () => {
  const [events] = useState(sampleEvents);
  const [selectedEvent, setSelectedEvent] = useState(null);

  const handleSearch = (query) => {
    alert(`Search: ${query}`);
  };

  return (
    <div className="page events-page">
      <Header /> {/* Add Header here */}
      <h2>📑 Sound Events Log</h2>
      <SearchBar onSearch={handleSearch} />
      <SoundEventTable events={events} onSelect={setSelectedEvent} />
      <ExportLogsButton />
      <EventDetailsModal event={selectedEvent} onClose={() => setSelectedEvent(null)} />
    </div>
  );
};

export default Events;
