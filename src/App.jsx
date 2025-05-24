import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Alerts from './pages/Alerts';
import CustomSounds from './pages/CustomSounds';
import Events from './pages/Events';
import Settings from './pages/Settings';
import Header from './components/Header';


function ProtectedRoute({ children }) {
  const isLoggedIn = localStorage.getItem("loggedInUser");
  return isLoggedIn ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/custom-sounds" element={<CustomSounds />} />
        <Route path="/events" element={<Events />} />
        <Route path="/settings" element={<Settings />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}
