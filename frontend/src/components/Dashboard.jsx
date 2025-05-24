// src/components/Dashboard.jsx
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className="dashboard">
      <h1>🔊 Sound Recognition Dashboard</h1>

      <div className="sections">
        <div className="section alerts" onClick={() => navigate("/alerts")}>
          <h2>📢 Real-time Alerts</h2>
          <p>No new alerts</p>
        </div>

        <div className="section logs" onClick={() => navigate("/logs")}>
          <h2>📜 Alert Logs</h2>
          <p>Previous detected sounds will appear here.</p>
        </div>

        <div className="section settings" onClick={() => navigate("/settings")}>
          <h2>⚙️ Settings</h2>
          <p>Configure your custom sounds & notifications.</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
