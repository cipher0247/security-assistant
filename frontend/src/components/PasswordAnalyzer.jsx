import React, { useState } from 'react';
import axios from 'axios';

/**
 * PasswordAnalyzer Component
 * Allows users to check password strength and get improvement suggestions
 */
function PasswordAnalyzer({ user }) {
  const [password, setPassword] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showPassword, setShowPassword] = useState(false);

  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

  const analyzePassword = async (e) => {
    e.preventDefault();
    if (!password) return;

    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('auth_token');
      const response = await axios.post(
        `${API_BASE}/security/analyze-password`,
        { password },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setAnalysis(response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to analyze password');
    } finally {
      setLoading(false);
    }
  };

  const getStrengthColor = (strength) => {
    const colors = {
      'Very Weak': 'bg-red-500',
      'Weak': 'bg-orange-500',
      'Fair': 'bg-yellow-500',
      'Strong': 'bg-green-500',
      'Very Strong': 'bg-blue-500',
    };
    return colors[strength] || 'bg-gray-500';
  };

  const getScorePercentage = (score) => {
    return Math.min(100, (score / 100) * 100);
  };

  return (
    <div className="max-w-4xl mx-auto px-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 mb-8">
        <div className="flex items-center space-x-3 mb-6">
          <span className="text-4xl">🔐</span>
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Password Strength Analyzer</h1>
            <p className="text-gray-600 dark:text-gray-400">Enter a password to analyze its security</p>
          </div>
        </div>

        <form onSubmit={analyzePassword} className="space-y-4">
          <div className="relative">
            <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Password (Demo Only - Not Stored)
            </label>
            <div className="flex">
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter a password to analyze"
                className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-l-lg focus:outline-none focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="px-4 py-3 bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-r-l transition"
              >
                {showPassword ? '👁️‍🗨️' : '👁️'}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={!password || loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg transition"
          >
            {loading ? 'Analyzing...' : 'Analyze Password'}
          </button>
        </form>

        {error && (
          <div className="mt-6 p-4 bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 rounded-lg">
            <p className="text-red-700 dark:text-red-200 font-semibold">Error: {error}</p>
          </div>
        )}

        {analysis && (
          <div className="mt-8 space-y-6">
            {/* Strength Gauge */}
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <label className="font-semibold text-gray-900 dark:text-white">Overall Strength</label>
                <span className={`px-4 py-2 rounded-full text-white font-bold ${getStrengthColor(analysis.strength)}`}>
                  {analysis.strength}
                </span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4 overflow-hidden">
                <div 
                  className={`h-full transition-all duration-500 ${getStrengthColor(analysis.strength)}`}
                  style={{ width: `${getScorePercentage(analysis.score)}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Score: {analysis.score}/100</p>
            </div>

            {/* Statistics */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <StatBox label="Length" value={password.length} />
              <StatBox label="Entropy" value={analysis.entropy.toFixed(2)} />
              <StatBox label="Character Types" value={analysis.character_types || '?'} />
              <StatBox label="Complexity" value="Medium" />
            </div>

            {/* Issues Found */}
            {analysis.issues && analysis.issues.length > 0 && (
              <div className="p-4 bg-orange-50 dark:bg-orange-900 rounded-lg border border-orange-200 dark:border-orange-700">
                <h3 className="font-bold text-orange-900 dark:text-orange-100 mb-3 flex items-center space-x-2">
                  <span>⚠️</span>
                  <span>Issues Found</span>
                </h3>
                <ul className="space-y-2">
                  {analysis.issues.map((issue, idx) => (
                    <li key={idx} className="text-orange-800 dark:text-orange-200 text-sm flex items-center space-x-2">
                      <span>•</span>
                      <span>{issue}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Suggestions */}
            {analysis.suggestions && analysis.suggestions.length > 0 && (
              <div className="p-4 bg-green-50 dark:bg-green-900 rounded-lg border border-green-200 dark:border-green-700">
                <h3 className="font-bold text-green-900 dark:text-green-100 mb-3 flex items-center space-x-2">
                  <span>💡</span>
                  <span>Improvement Suggestions</span>
                </h3>
                <ul className="space-y-2">
                  {analysis.suggestions.map((suggestion, idx) => (
                    <li key={idx} className="text-green-800 dark:text-green-200 text-sm flex items-center space-x-2">
                      <span>✓</span>
                      <span>{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Crack Time */}
            {analysis.crack_time && (
              <div className="p-4 bg-blue-50 dark:bg-blue-900 rounded-lg border border-blue-200 dark:border-blue-700">
                <h3 className="font-bold text-blue-900 dark:text-blue-100 mb-3">⏱️ Time to Crack</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  <div>
                    <p className="text-xs text-blue-700 dark:text-blue-300 font-semibold">ONLINE (1 attempt/sec)</p>
                    <p className="text-lg font-bold text-blue-900 dark:text-blue-100">{analysis.crack_time.online}</p>
                  </div>
                  <div>
                    <p className="text-xs text-blue-700 dark:text-blue-300 font-semibold">GPU (10B attempts/sec)</p>
                    <p className="text-lg font-bold text-blue-900 dark:text-blue-100">{analysis.crack_time.gpu}</p>
                  </div>
                  <div>
                    <p className="text-xs text-blue-700 dark:text-blue-300 font-semibold">SUPERCOMPUTER (1T/sec)</p>
                    <p className="text-lg font-bold text-blue-900 dark:text-blue-100">{analysis.crack_time.supercomputer}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Tips */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <TipCard 
          title="Password Best Practices"
          tips={[
            "Use at least 12-16 characters",
            "Mix uppercase, lowercase, numbers, symbols",
            "Avoid common words or patterns",
            "Use unique passwords per account",
            "Enable two-factor authentication"
          ]}
        />
        <TipCard 
          title="Password Manager Recommendations"
          tips={[
            "Bitwarden (open-source, free)",
            "1Password (paid, trusted)",
            "KeePass (offline, free)",
            "Dashlane (simple, paid)",
            "Store securely, backup recovery codes"
          ]}
        />
      </div>
    </div>
  );
}

function StatBox({ label, value }) {
  return (
    <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4 text-center">
      <p className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">{label}</p>
      <p className="text-2xl font-bold text-gray-900 dark:text-white">{value}</p>
    </div>
  );
}

function TipCard({ title, tips }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">💡 {title}</h3>
      <ul className="space-y-2">
        {tips.map((tip, idx) => (
          <li key={idx} className="flex items-start space-x-3">
            <span className="text-green-600 dark:text-green-400 font-bold">✓</span>
            <span className="text-gray-700 dark:text-gray-300 text-sm">{tip}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PasswordAnalyzer;
