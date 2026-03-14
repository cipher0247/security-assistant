import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';
import Dashboard from './components/Dashboard';
import PasswordAnalyzer from './components/PasswordAnalyzer';
import URLChecker from './components/URLChecker';
import PhishingDetector from './components/PhishingDetector';
import AIAssistant from './components/AIAssistant';
import LeaderboardView from './components/LeaderboardView';
import SecurityScore from './components/SecurityScore';
import './App.css';

/**
 * Main App Component
 * Handles routing and global state for the security platform
 */
function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [theme, setTheme] = useState('light');

  // API base URL
  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

  useEffect(() => {
    // Check if user is authenticated
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('auth_token');
        if (token) {
          const response = await axios.get(`${API_BASE}/auth/me`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          setUser(response.data);
        }
      } catch (error) {
        console.log('Not authenticated');
        localStorage.removeItem('auth_token');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();

    // Set theme preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    document.documentElement.classList.toggle('dark', savedTheme === 'dark');
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    setUser(null);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="animate-pulse text-center">
          <div className="text-4xl mb-4">🛡️</div>
          <h1 className="text-2xl font-bold text-gray-800">Security Assistant</h1>
          <p className="text-gray-600 mt-2">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4">
          <div className="text-center mb-8">
            <div className="text-5xl mb-4">🛡️</div>
            <h1 className="text-3xl font-bold text-gray-900">Security Assistant</h1>
            <p className="text-gray-600 mt-2">Your AI Cybersecurity Mentor</p>
          </div>
          
          <div className="space-y-4">
            <button 
              onClick={() => window.location.href = '/login'}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition"
            >
              Login
            </button>
            <button 
              onClick={() => window.location.href = '/register'}
              className="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg transition"
            >
              Register
            </button>
          </div>

          <div className="mt-8 p-4 bg-blue-50 rounded-lg">
            <h3 className="font-bold text-blue-900 mb-2">Demo Mode Available</h3>
            <p className="text-blue-700 text-sm">
              Try our tools without logging in to explore password strength, 
              URL safety, and phishing detection.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className={theme === 'dark' ? 'dark' : ''}>
        <nav className="bg-white dark:bg-gray-800 shadow-lg">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center space-x-8">
                <Link to="/dashboard" className="flex items-center space-x-2">
                  <span className="text-2xl">🛡️</span>
                  <span className="font-bold text-lg dark:text-white">Security Assistant</span>
                </Link>
                
                <div className="hidden md:flex space-x-6">
                  <Link to="/dashboard" className="text-gray-700 dark:text-gray-300 hover:text-blue-600 transition">Dashboard</Link>
                  <Link to="/password" className="text-gray-700 dark:text-gray-300 hover:text-blue-600 transition">Password</Link>
                  <Link to="/url" className="text-gray-700 dark:text-gray-300 hover:text-blue-600 transition">URL Check</Link>
                  <Link to="/phishing" className="text-gray-700 dark:text-gray-300 hover:text-blue-600 transition">Phishing</Link>
                  <Link to="/assistant" className="text-gray-700 dark:text-gray-300 hover:text-blue-600 transition">AI Help</Link>
                  <Link to="/leaderboard" className="text-gray-700 dark:text-gray-300 hover:text-blue-600 transition">Rankings</Link>
                </div>
              </div>

              <div className="flex items-center space-x-4">
                <button 
                  onClick={toggleTheme}
                  className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition"
                  title="Toggle theme"
                >
                  {theme === 'light' ? '🌙' : '☀️'}
                </button>
                
                <div className="flex items-center space-x-2">
                  <span className="text-sm dark:text-gray-300">{user.username}</span>
                  <button 
                    onClick={handleLogout}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition text-sm"
                  >
                    Logout
                  </button>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <main className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
          <Routes>
            <Route path="/dashboard" element={<Dashboard user={user} />} />
            <Route path="/password" element={<PasswordAnalyzer user={user} />} />
            <Route path="/url" element={<URLChecker user={user} />} />
            <Route path="/phishing" element={<PhishingDetector user={user} />} />
            <Route path="/assistant" element={<AIAssistant user={user} />} />
            <Route path="/leaderboard" element={<LeaderboardView user={user} />} />
            <Route path="/" element={<Dashboard user={user} />} />
          </Routes>
        </main>

        <footer className="bg-white dark:bg-gray-800 border-t dark:border-gray-700 mt-12 py-6">
          <div className="max-w-7xl mx-auto px-4 text-center text-gray-600 dark:text-gray-400 text-sm">
            <p>🛡️ Security Assistant v2.0 | Your AI Cybersecurity Mentor</p>
            <p className="mt-2">Never store your real passwords. Always verify domains before entering credentials.</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
