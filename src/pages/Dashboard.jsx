// src/pages/Dashboard.jsx
import React from "react";
import Header from "../components/Header";
import LiveSoundFeed from "../components/LiveSoundFeed";
import AlertPanel from "../components/AlertPanel";
import SoundGraph from "../components/SoundGraph";
import DeviceStatusCard from "../components/DeviceStatusCard";
import SystemSummary from "../components/SystemSummary";
import "../styles/Dashboard.css";

export default function Dashboard() {
  return (
    <div className="dashboard-container">
      <Header />
      <div className="dashboard-main">
        <div className="dashboard-card"><LiveSoundFeed /></div>
        <div className="dashboard-card"><AlertPanel /></div>
        <div className="dashboard-card"><SoundGraph /></div>
        <div className="dashboard-card"><DeviceStatusCard /></div>
        <div className="dashboard-card"><SystemSummary /></div>
<div className="dashboard-card">
  <h3>🛠️ System Health Summary</h3>
  <ul className="health-list">
    <li><strong>CPU Usage:</strong> 23%</li>
    <li><strong>Memory Usage:</strong> 45%</li>
    <li><strong>System Uptime:</strong> 12h 38m</li>
    <li><strong>Temperature:</strong> 58°C</li>
    <li><strong>Status:</strong> ✅ Running Smoothly</li>
  </ul>
</div>
      </div>
    </div>
  );
}
