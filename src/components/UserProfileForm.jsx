// src/components/UserProfileForm.jsx
import React, { useState } from 'react';
import '../styles/UserProfileForm.css';

const UserProfileForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: ''
  });

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value});
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Profile updated!');
  };

  return (
    <form className="user-profile-form" onSubmit={handleSubmit}>
      <h3>👤 User Profile</h3>
      <input name="name" placeholder="Name" value={formData.name} onChange={handleChange} />
      <input name="email" placeholder="Email" value={formData.email} onChange={handleChange} />
      <input name="password" type="password" placeholder="New Password" value={formData.password} onChange={handleChange} />
      <button type="submit">Update</button>
    </form>
  );
};

export default UserProfileForm;
