import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./LoginRegister.css";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const user = { email, password };
    localStorage.setItem("registeredUser", JSON.stringify(user));
    alert("Registered successfully!");
    navigate("/login");
  };

  return (
    <div className="auth-container">
      <form onSubmit={handleSubmit} className="auth-box">
        <h2>Register</h2>
        <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} required />
        <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit">Register</button>
        <p style={{ marginTop: "10px" }}>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  );
}
