// src/components/NewCustomSoundForm.jsx
import React, { useState } from 'react';
import '../styles/NewCustomSoundForm.css';

const NewCustomSoundForm = () => {
  const [file, setFile] = useState(null);

  const handleUpload = (e) => {
    setFile(e.target.files[0]);
  };

  return (
    <div className="card new-custom-sound-form">
      <h3>➕ Add New Custom Sound</h3>
      <input type="file" accept="audio/*" onChange={handleUpload} />
      {file && <p>Uploaded: {file.name}</p>}
    </div>
  );
};

export default NewCustomSoundForm;
