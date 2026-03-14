import React, { useState } from 'react';
import axios from 'axios';

/**
 * PhishingDetector Component
 * Analyzes emails and messages for phishing indicators
 */
function PhishingDetector({ user }) {
  const [analysisType, setAnalysisType] = useState('email');
  const [subject, setSubject] = useState('');
  const [sender, setSender] = useState('');
  const [body, setBody] = useState('');
  const [url, setUrl] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

  const analyzePhishing = async (e) => {
    e.preventDefault();

    if (analysisType === 'email' && (!subject || !body || !sender)) {
      setError('Please fill in all email fields');
      return;
    }
    if (analysisType === 'url' && !url) {
      setError('Please enter a URL');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('auth_token');
      const endpoint = analysisType === 'email' ? 'detect-phishing-email' : 'detect-phishing-url';
      const payload = analysisType === 'email' 
        ? { subject, sender, body }
        : { url };

      const response = await axios.post(
        `${API_BASE}/security/${endpoint}`,
        payload,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setAnalysis(response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to analyze');
    } finally {
      setLoading(false);
    }
  };

  const getRiskLevel = (isPhishing, confidence) => {
    if (isPhishing && confidence > 0.8) return 'CRITICAL_PHISHING';
    if (isPhishing && confidence > 0.6) return 'LIKELY_PHISHING';
    if (isPhishing) return 'POSSIBLE_PHISHING';
    return 'LEGITIMATE';
  };

  const getRiskIcon = (riskLevel) => {
    const icons = {
      'CRITICAL_PHISHING': '🚨🚨🚨',
      'LIKELY_PHISHING': '🚨🚨',
      'POSSIBLE_PHISHING': '⚠️',
      'LEGITIMATE': '✅',
    };
    return icons[riskLevel] || '❓';
  };

  const getRiskColor = (riskLevel) => {
    const colors = {
      'CRITICAL_PHISHING': 'red',
      'LIKELY_PHISHING': 'orange',
      'POSSIBLE_PHISHING': 'yellow',
      'LEGITIMATE': 'green',
    };
    return colors[riskLevel] || 'gray';
  };

  return (
    <div className="max-w-4xl mx-auto px-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 mb-8">
        <div className="flex items-center space-x-3 mb-6">
          <span className="text-4xl">🚨</span>
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Phishing Detector</h1>
            <p className="text-gray-600 dark:text-gray-400">Identify malicious emails and URLs</p>
          </div>
        </div>

        {/* Tab Selection */}
        <div className="mb-6 flex gap-2">
          <button
            onClick={() => { setAnalysisType('email'); setAnalysis(null); }}
            className={`px-6 py-2 rounded-lg font-semibold transition ${
              analysisType === 'email'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white'
            }`}
          >
            📧 Email Analysis
          </button>
          <button
            onClick={() => { setAnalysisType('url'); setAnalysis(null); }}
            className={`px-6 py-2 rounded-lg font-semibold transition ${
              analysisType === 'url'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white'
            }`}
          >
            🔗 URL Analysis
          </button>
        </div>

        <form onSubmit={analyzePhishing} className="space-y-4">
          {analysisType === 'email' ? (
            <>
              <div>
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Sender Email
                </label>
                <input
                  type="email"
                  value={sender}
                  onChange={(e) => setSender(e.target.value)}
                  placeholder="sender@example.com"
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Email Subject
                </label>
                <input
                  type="text"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  placeholder="Email subject line"
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Email Body
                </label>
                <textarea
                  value={body}
                  onChange={(e) => setBody(e.target.value)}
                  placeholder="Paste the email content here"
                  rows="6"
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                ></textarea>
              </div>
            </>
          ) : (
            <div>
              <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                URL to Check
              </label>
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://example.com"
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              />
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg transition"
          >
            {loading ? '🔄 Analyzing...' : '🔍 Analyze'}
          </button>
        </form>

        {error && (
          <div className="mt-6 p-4 bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 rounded-lg">
            <p className="text-red-700 dark:text-red-200 font-semibold">Error: {error}</p>
          </div>
        )}

        {analysis && (
          <div className="mt-8 space-y-6">
            {/* Risk Assessment */}
            <div className={`p-6 rounded-lg border-l-4 bg-${getRiskColor(getRiskLevel(analysis.is_phishing, analysis.confidence))}-50 dark:bg-${getRiskColor(getRiskLevel(analysis.is_phishing, analysis.confidence))}-900 border-${getRiskColor(getRiskLevel(analysis.is_phishing, analysis.confidence))}-400 dark:border-${getRiskColor(getRiskLevel(analysis.is_phishing, analysis.confidence))}-700`}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-semibold mb-1 text-gray-600 dark:text-gray-400">Phishing Status</p>
                  <p className="text-3xl font-bold text-gray-900 dark:text-white">
                    {analysis.is_phishing ? '⚠️ PHISHING DETECTED' : '✅ LEGITIMATE'}
                  </p>
                  <p className="text-sm mt-2 text-gray-700 dark:text-gray-300">
                    Confidence: {(analysis.confidence * 100).toFixed(1)}%
                  </p>
                </div>
                <div className="text-6xl">{getRiskIcon(getRiskLevel(analysis.is_phishing, analysis.confidence))}</div>
              </div>
            </div>

            {/* Warnings */}
            {analysis.warnings && analysis.warnings.length > 0 && (
              <div className="p-4 bg-red-50 dark:bg-red-900 rounded-lg border border-red-200 dark:border-red-700">
                <h3 className="font-bold text-red-900 dark:text-red-100 mb-3">⚠️ Red Flags</h3>
                <ul className="space-y-2">
                  {analysis.warnings.map((warning, idx) => (
                    <li key={idx} className="text-red-800 dark:text-red-200 text-sm flex items-center space-x-2">
                      <span>🚩</span>
                      <span>{warning}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Detected Features */}
            {analysis.features_detected && (
              <div className="p-4 bg-yellow-50 dark:bg-yellow-900 rounded-lg border border-yellow-200 dark:border-yellow-700">
                <h3 className="font-bold text-yellow-900 dark:text-yellow-100 mb-3">🔍 Suspicious Indicators</h3>
                <div className="grid grid-cols-2 gap-2">
                  {Object.entries(analysis.features_detected).map(([feature, detected]) => (
                    <div key={feature} className="flex items-center space-x-2">
                      <span>{detected ? '✓' : '✗'}</span>
                      <span className="text-sm text-yellow-800 dark:text-yellow-200">
                        {feature.replace(/_/g, ' ').charAt(0).toUpperCase() + feature.slice(1)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Recommendations */}
            {analysis.recommendations && analysis.recommendations.length > 0 && (
              <div className="p-4 bg-green-50 dark:bg-green-900 rounded-lg border border-green-200 dark:border-green-700">
                <h3 className="font-bold text-green-900 dark:text-green-100 mb-3">✅ What To Do</h3>
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

            {/* Explanation */}
            {analysis.explanation && (
              <div className="p-4 bg-blue-50 dark:bg-blue-900 rounded-lg border border-blue-200 dark:border-blue-700">
                <h3 className="font-bold text-blue-900 dark:text-blue-100 mb-2">🤖 AI Analysis</h3>
                <p className="text-blue-800 dark:text-blue-200 text-sm">{analysis.explanation}</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Tips */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <TipCard 
          title="Phishing Red Flags"
          icons={['🚩', '🚨', '⚠️', '❌', '🔴']}
          tips={[
            "Urgent language demanding immediate action",
            "Requests for passwords, credit cards, or personal info",
            "Misspelled domains or strange email addresses",
            "Generic greetings ('Dear Customer' instead of your name)",
            "Suspicious attachments or links"
          ]}
        />
        <TipCard 
          title="What To Do If Phished"
          icons={['✓', '📞', '🔒', '📧', '⏰']}
          tips={[
            "Don't click any links or open attachments",
            "Contact the company directly using a known number",
            "Change passwords immediately",
            "Report to phishing@&lt;company&gt;.com",
            "Monitor accounts for suspicious activity"
          ]}
        />
      </div>
    </div>
  );
}

function TipCard({ title, icons, tips }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">{title}</h3>
      <ul className="space-y-2">
        {tips.map((tip, idx) => (
          <li key={idx} className="flex items-start space-x-3">
            <span className="text-lg">{icons[idx % icons.length]}</span>
            <span className="text-gray-700 dark:text-gray-300 text-sm">{tip}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PhishingDetector;
