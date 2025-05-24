// src/components/RegisterForm.jsx
import React, { useState } from 'react';
import '../styles/RegisterForm.css';

const RegisterForm = () => {
  const [form, setForm] = useState({ name: '', email: '', password: '' });

  const handleChange = (e) => {
    setForm({...form, [e.target.name]: e.target.value});
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Registered!');
  };

  return (
    <form className="register-form" onSubmit={handleSubmit}>
      <h2>📝 Register</h2>
      <input name="name" placeholder="Name" value={form.name} onChange={handleChange} />
      <input name="email" placeholder="Email" value={form.email} onChange={handleChange} />
      <input name="password" type="password" placeholder="Password" value={form.password} onChange={handleChange} />
      <button type="submit">Register</button>
    </form>
  );
};

export default RegisterForm;
