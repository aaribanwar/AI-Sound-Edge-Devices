// src/components/ExportLogsButton.jsx
import React from 'react';
import '../styles/ExportLogsButton.css';

const ExportLogsButton = () => {
  const handleExport = () => {
    alert("Logs exported as CSV!");
  };

  return (
    <button className="export-logs-button" onClick={handleExport}>
      📤 Export Logs
    </button>
  );
};

export default ExportLogsButton;
