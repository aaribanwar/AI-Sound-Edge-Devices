import "./App.css";

function App() {
  return (
    <div className="dashboard">
      <h1>🔊 Sound Recognition Dashboard</h1>

      <div className="sections">
        <div className="section alerts">
          <h2>📢 Real-time Alerts</h2>
          <p>No new alerts</p>
        </div>

        <div className="section logs">
          <h2>📜 Alert Logs</h2>
          <p>Previous detected sounds will appear here.</p>
        </div>

        <div className="section settings">
          <h2>⚙️ Settings</h2>
          <p>Configure your custom sounds & notifications.</p>
        </div>
      </div>
    </div>
  );
}

export default App;
