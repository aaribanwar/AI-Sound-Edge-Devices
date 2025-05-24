import React from "react";
import "./App.css";
import { Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Dashboard from "./components/Dashboard";
import Alerts from "./pages/Alerts";
import Logs from "./pages/Logs";
import Settings from "./pages/Settings";

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/logs" element={<Logs />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </>
  );
}

export default App;
