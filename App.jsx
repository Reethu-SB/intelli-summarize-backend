import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState } from 'react';

import Home  from './pages/Home';
import  Login from './pages/Login';
import Signup  from './pages/Signup';
import DocumentSummarizer from './pages/DocumentSummarizer';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  return (
    <Router basename="/">
      <Routes>
        {/* Home Page */}
        <Route path="/" element={<Home />} />
        <Route path="/preview_page_v2.html" element={<Home />} />

        {/* Login */}
        <Route
          path="/login"
          element={
            isAuthenticated ? (
              <Navigate to="/dashboard" replace />
            ) : (
              <Login onLogin={handleLogin} />
            )
          }
        />

        {/* Signup */}
        <Route
          path="/signup"
          element={
            isAuthenticated ? (
              <Navigate to="/dashboard" replace />
            ) : (
              <Signup onSignup={handleLogin} />
            )
          }
        />

        {/* Dashboard (Protected Route) */}
        <Route
          path="/dashboard"
          element={
            isAuthenticated ? (
              <DocumentSummarizer onLogout={handleLogout} />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Home />} />
      </Routes>
    </Router>
  );
}
