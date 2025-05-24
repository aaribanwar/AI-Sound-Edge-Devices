import React from "react";
import { useTheme } from "../context/ThemeContext";
import "../App.css";

const Navbar = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="navbar">
      <div className="navbar-buttons">
        <button className="theme-toggle" onClick={toggleTheme}>
          {theme === "light" ? "🌙 Dark" : "☀️ Light"}
        </button>
      </div>
    </header>
  );
};

export default Navbar;
