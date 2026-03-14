import React, { useState } from 'react';
import axios from 'axios';

/**
 * URLChecker Component
 * Analyzes URLs for phishing, malware, and other security threats
 */
function URLChecker({ user }) {
  const [url, setUrl] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

  const analyzeURL = async (e) => {
    e.preventDefault();
    if (!url) return;

    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('auth_token');
      const response = await axios.post(
        `${API_BASE}/security/analyze-url`,
        { url },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setAnalysis(response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to analyze URL');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level) => {
    const colors = {
      'SAFE': 'bg-green-500',
      'SUSPICIOUS': 'bg-yellow-500',
      'HIGH_RISK': 'bg-red-500',
    };
    return colors[level] || 'bg-gray-500';
  };

  const getRiskIcon = (level) => {
    const icons = {
      'SAFE': '✅',
      'SUSPICIOUS': '⚠️',
      'HIGH_RISK': '🚨',
    };
    return icons[level] || '❓';
  };

  return (
    <div className="max-w-4xl mx-auto px-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 mb-8">
        <div className="flex items-center space-x-3 mb-6">
          <span className="text-4xl">🌐</span>
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">URL Safety Checker</h1>
            <p className="text-gray-600 dark:text-gray-400">Verify if a link is safe before clicking</p>
          </div>
        </div>

        <form onSubmit={analyzeURL} className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Enter URL to Check
            </label>
            <div className="flex">
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://example.com"
                className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-l-lg focus:outline-none focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              />
              <button
                type="submit"
                disabled={!url || loading}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold rounded-r-lg transition"
              >
                {loading ? '🔄 Checking...' : '🔍 Check'}
              </button>
            </div>
          </div>
        </form>

        {error && (
          <div className="mt-6 p-4 bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 rounded-lg">
            <p className="text-red-700 dark:text-red-200 font-semibold">Error: {error}</p>
          </div>
        )}

        {analysis && (
          <div className="mt-8 space-y-6">
            {/* Risk Level */}
            <div className="flex items-center justify-between p-6 bg-gray-100 dark:bg-gray-700 rounded-lg border-l-4" style={{borderColor: analysis.risk_level === 'SAFE' ? '#10b981' : analysis.risk_level === 'SUSPICIOUS' ? '#f59e0b' : '#ef4444'}}>
              <div>
                <p className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">Risk Level</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{analysis.risk_level}</p>
              </div>
              <div className="text-5xl">{getRiskIcon(analysis.risk_level)}</div>
            </div>

            {/* Risk Score */}
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <label className="font-semibold text-gray-900 dark:text-white">Safety Score</label>
                <span className="text-lg font-bold text-gray-900 dark:text-white">{analysis.score}/100</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4 overflow-hidden">
                <div 
                  className={`h-full transition-all duration-500 ${getRiskColor(analysis.risk_level)}`}
                  style={{ width: `${analysis.score}%` }}
                ></div>
              </div>
            </div>

            {/* Domain Info */}
            {analysis.domain_info && (
              <div className="p-4 bg-blue-50 dark:bg-blue-900 rounded-lg border border-blue-200 dark:border-blue-700">
                <h3 className="font-bold text-blue-900 dark:text-blue-100 mb-3">🔍 Domain Information</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs font-semibold text-blue-700 dark:text-blue-300 mb-1">DOMAIN</p>
                    <p className="text-sm font-mono text-blue-900 dark:text-blue-100 break-all">{analysis.domain_info.domain}</p>
                  </div>
                  <div>
                    <p className="text-xs font-semibold text-blue-700 dark:text-blue-300 mb-1">PROTOCOL</p>
                    <p className="text-sm font-mono text-blue-900 dark:text-blue-100">{analysis.domain_info.protocol}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Threats */}
            {analysis.threats && analysis.threats.length > 0 && (
              <div className="p-4 bg-red-50 dark:bg-red-900 rounded-lg border border-red-200 dark:border-red-700">
                <h3 className="font-bold text-red-900 dark:text-red-100 mb-3">🚨 Threats Detected</h3>
                <ul className="space-y-2">
                  {analysis.threats.map((threat, idx) => (
                    <li key={idx} className="text-red-800 dark:text-red-200 text-sm flex items-center space-x-2">
                      <span>⚠️</span>
                      <span>{threat}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Recommendations */}
            {analysis.recommendations && analysis.recommendations.length > 0 && (
              <div className="p-4 bg-green-50 dark:bg-green-900 rounded-lg border border-green-200 dark:border-green-700">
                <h3 className="font-bold text-green-900 dark:text-green-100 mb-3">✅ Recommendations</h3>
                <ul className="space-y-2">
                  {analysis.recommendations.map((rec, idx) => (
                    <li key={idx} className="text-green-800 dark:text-green-200 text-sm flex items-center space-x-2">
                      <span>→</span>
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* AI Explanation */}
            {analysis.ai_explanation && (
              <div className="p-4 bg-purple-50 dark:bg-purple-900 rounded-lg border border-purple-200 dark:border-purple-700">
                <h3 className="font-bold text-purple-900 dark:text-purple-100 mb-2">🤖 AI Explanation</h3>
                <p className="text-purple-800 dark:text-purple-200 text-sm">{analysis.ai_explanation}</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Tips */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <TipCard 
          title="URL Safety Tips"
          tips={[
            "Always check the domain name carefully",
            "Look for HTTPS (not HTTP) before entering data",
            "Hover over links to see actual destination",
            "Be suspicious of URL shorteners (bit.ly, tinyurl)",
            "Report phishing URLs to authorities"
          ]}
        />
        <TipCard 
          title="Common Phishing Tricks"
          tips={[
            "Typosquatting (gogle.com instead of google.com)",
            "Lookalike domains (paypa1.com with 1 instead of l)",
            "IP addresses instead of domain names",
            "Unusual subdomains (secure.account.update.com)",
            "Sensitive info requests via URL parameters"
          ]}
        />
      </div>
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
            <span className="text-blue-600 dark:text-blue-400 font-bold">•</span>
            <span className="text-gray-700 dark:text-gray-300 text-sm">{tip}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default URLChecker;
