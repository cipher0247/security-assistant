/**
 * Frontend Integration Examples
 * =============================
 * Example React components showing how to integrate NVIDIA AI endpoints.
 * 
 * Copy patterns from these examples into your existing components.
 */

import React, { useState } from 'react';
import { aiService, formatResponse, formatError, createLoadingState } from './nvaidaService';

// ============================================================================
// EXAMPLE 1: PHISHING DETECTOR INTEGRATION
// ============================================================================

export const PhishingDetectorIntegration = () => {
  const [email, setEmail] = useState('');
  const [subject, setSubject] = useState('');
  const [sender, setSender] = useState('');
  const [state, setState] = useState(createLoadingState());

  const analyzePhishing = async () => {
    setState(createLoadingState());
    try {
      const response = await aiService.explainPhishing(email, subject, sender);
      setState({
        isLoading: false,
        error: null,
        data: formatResponse(response)
      });
    } catch (error) {
      setState({
        isLoading: false,
        error: formatError(error),
        data: null
      });
    }
  };

  return (
    <div className="phishing-detector">
      <h2>🎣 Phishing Email Analyzer</h2>
      
      <textarea
        placeholder="Paste entire email here..."
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        rows="8"
      />
      
      <input
        type="text"
        placeholder="Email subject"
        value={subject}
        onChange={(e) => setSubject(e.target.value)}
      />
      
      <input
        type="email"
        placeholder="Sender email"
        value={sender}
        onChange={(e) => setSender(e.target.value)}
      />
      
      <button onClick={analyzePhishing} disabled={state.isLoading}>
        {state.isLoading ? 'Analyzing...' : 'Analyze Email'}
      </button>

      {state.error && (
        <div className="error-message">
          ❌ {state.error}
        </div>
      )}

      {state.data && (
        <div className="analysis-result">
          <div className={`risk-badge risk-${state.data.riskLevel.toLowerCase()}`}>
            {state.data.riskLevel}
          </div>
          
          <div className="explanation">
            <h3>AI Analysis</h3>
            <p>{state.data.explanation}</p>
          </div>
          
          <div className="metadata">
            <span>Confidence: {(state.data.confidence * 100).toFixed(0)}%</span>
            <span>Tokens: {state.data.tokensUsed}</span>
            <span>{new Date(state.data.timestamp).toLocaleTimeString()}</span>
          </div>
        </div>
      )}
    </div>
  );
};

// ============================================================================
// EXAMPLE 2: URL CHECKER INTEGRATION
// ============================================================================

export const URLCheckerIntegration = () => {
  const [url, setUrl] = useState('');
  const [state, setState] = useState(createLoadingState());

  const checkURL = async () => {
    setState(createLoadingState());
    try {
      const response = await aiService.analyzeURL(url);
      setState({
        isLoading: false,
        error: null,
        data: formatResponse(response)
      });
    } catch (error) {
      setState({
        isLoading: false,
        error: formatError(error),
        data: null
      });
    }
  };

  return (
    <div className="url-checker">
      <h2>🔗 URL Security Analyzer</h2>
      
      <input
        type="url"
        placeholder="Enter URL (e.g., https://example.com)"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      
      <button onClick={checkURL} disabled={state.isLoading}>
        {state.isLoading ? 'Checking...' : 'Check URL'}
      </button>

      {state.error && (
        <div className="error-message">
          ❌ {state.error}
        </div>
      )}

      {state.data && (
        <div className="analysis-result">
          <div className={`safety-indicator ${state.data.riskLevel === 'Low' ? 'safe' : 'unsafe'}`}>
            {state.data.riskLevel === 'Low' ? '✓ Safe' : '⚠ Unsafe'}
          </div>
          
          <div className="explanation">
            <h3>Why?</h3>
            <p>{state.data.explanation}</p>
          </div>
          
          <div className="recommendation">
            {state.data.riskLevel === 'Low' 
              ? '✓ It appears safe to click this link'
              : '✗ Avoid clicking this link - it may be dangerous'}
          </div>
        </div>
      )}
    </div>
  );
};

// ============================================================================
// EXAMPLE 3: PASSWORD ANALYZER INTEGRATION
// ============================================================================

export const PasswordAnalyzerIntegration = ({ passwordScore, entropy, issues }) => {
  const [state, setState] = useState(createLoadingState());

  const requestCoaching = async () => {
    setState(createLoadingState());
    try {
      const response = await aiService.passwordCoaching({
        strength: passwordScore < 50 ? 'Weak' : passwordScore < 75 ? 'Fair' : 'Strong',
        score: passwordScore,
        entropy: entropy,
        issues: issues,
        crackTime: {
          online: 'Instantly',
          gpu: 'Seconds',
          offline: 'Days'
        }
      });
      
      setState({
        isLoading: false,
        error: null,
        data: formatResponse(response)
      });
    } catch (error) {
      setState({
        isLoading: false,
        error: formatError(error),
        data: null
      });
    }
  };

  return (
    <div className="password-coaching">
      <h2>🔐 Password Security Coach</h2>
      
      <div className="password-stats">
        <div className="stat">
          <span>Strength Score:</span>
          <strong>{passwordScore}/100</strong>
        </div>
        <div className="stat">
          <span>Entropy:</span>
          <strong>{entropy.toFixed(2)} bits</strong>
        </div>
      </div>

      {issues.length > 0 && (
        <div className="issues-list">
          <h3>Issues Found:</h3>
          <ul>
            {issues.map((issue, idx) => (
              <li key={idx}>⚠ {issue}</li>
            ))}
          </ul>
        </div>
      )}

      <button onClick={requestCoaching} disabled={state.isLoading}>
        {state.isLoading ? 'Getting coaching...' : 'Get AI Coaching'}
      </button>

      {state.error && (
        <div className="error-message">
          ❌ {state.error}
        </div>
      )}

      {state.data && (
        <div className="coaching-result">
          <div className="explanation">
            <h3>💡 Coach's Advice</h3>
            <p>{state.data.explanation}</p>
          </div>
          
          <div className="tips">
            <h3>🎯 Recommended Improvements:</h3>
            <ul>
              <li>✓ Use 12+ characters</li>
              <li>✓ Add special characters (!@#$%)</li>
              <li>✓ Mix uppercase and lowercase</li>
              <li>✓ Avoid common words</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

// ============================================================================
// EXAMPLE 4: FILE SECURITY ANALYZER INTEGRATION
// ============================================================================

export const FileSecurityIntegration = ({ fileName, fileType, riskLevel, indicators }) => {
  const [state, setState] = useState(createLoadingState());

  const explainRisk = async () => {
    setState(createLoadingState());
    try {
      const response = await aiService.explainFileRisk({
        filename: fileName,
        fileType: fileType,
        riskLevel: riskLevel,
        riskIndicators: indicators
      });

      setState({
        isLoading: false,
        error: null,
        data: formatResponse(response)
      });
    } catch (error) {
      setState({
        isLoading: false,
        error: formatError(error),
        data: null
      });
    }
  };

  return (
    <div className="file-security">
      <h2>📁 File Security Analyzer</h2>
      
      <div className="file-info">
        <div className="info-row">
          <span>Filename:</span>
          <strong>{fileName}</strong>
        </div>
        <div className="info-row">
          <span>Type:</span>
          <strong>.{fileType}</strong>
        </div>
        <div className={`info-row risk-${riskLevel.toLowerCase()}`}>
          <span>Risk Level:</span>
          <strong>{riskLevel}</strong>
        </div>
      </div>

      {indicators.length > 0 && (
        <div className="risk-indicators">
          <h3>⚠ Risk Indicators:</h3>
          <ul>
            {indicators.map((indicator, idx) => (
              <li key={idx}>{indicator}</li>
            ))}
          </ul>
        </div>
      )}

      <button onClick={explainRisk} disabled={state.isLoading}>
        {state.isLoading ? 'Explaining...' : 'Explain Risk'}
      </button>

      {state.error && (
        <div className="error-message">
          ❌ {state.error}
        </div>
      )}

      {state.data && (
        <div className="risk-explanation">
          <div className="explanation">
            <h3>🔍 Why is this file risky?</h3>
            <p>{state.data.explanation}</p>
          </div>

          <div className={`recommendation ${riskLevel === 'High' ? 'danger' : 'caution'}`}>
            {riskLevel === 'High'
              ? '🚫 Do not open this file'
              : '⚠️ Be careful when opening this file'}
          </div>

          <div className="safety-tips">
            <h3>🛡️ Stay Safe:</h3>
            <ul>
              <li>✓ Only open files from trusted sources</li>
              <li>✓ Keep antivirus software updated</li>
              <li>✓ Never enable macros unless necessary</li>
              <li>✓ Scan files before opening</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

// ============================================================================
// EXAMPLE 5: SECURITY CHATBOT INTEGRATION
// ============================================================================

export const SecurityChatbotIntegration = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I\'m your cybersecurity coach. Ask me anything about staying safe online!' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user message to chat
    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await aiService.askSecurityQuestion(input);
      
      const aiMessage = {
        role: 'assistant',
        content: response.answer
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${formatError(error)}`
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = async () => {
    try {
      await aiService.clearChatHistory();
      setMessages([
        { role: 'assistant', content: 'Chat cleared! How can I help you?' }
      ]);
    } catch (error) {
      console.error('Failed to clear chat:', error);
    }
  };

  return (
    <div className="chatbot-container">
      <h2>🤖 Cybersecurity Tutor</h2>
      
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="message-badge">
              {msg.role === 'user' ? '👤 You' : '🤖 Coach'}
            </div>
            <div className="message-content">
              {msg.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
            <div className="typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
      </div>

      <div className="chat-input-area">
        <input
          type="text"
          placeholder="Ask me anything about cybersecurity..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          disabled={isLoading}
        />
        <button onClick={sendMessage} disabled={isLoading || !input.trim()}>
          Send
        </button>
        <button onClick={handleClearChat} className="clear-btn">
          Clear
        </button>
      </div>

      <style jsx>{`
        .message {
          margin: 10px 0;
          padding: 10px;
          border-radius: 5px;
        }
        .message.user {
          background-color: #e3f2fd;
          margin-left: 40px;
        }
        .message.assistant {
          background-color: #f5f5f5;
          margin-right: 40px;
        }
      `}</style>
    </div>
  );
};

// ============================================================================
// EXAMPLE 6: THREAT EXPLAINER INTEGRATION
// ============================================================================

export const ThreatExplainerIntegration = ({ threatType }) => {
  const [state, setState] = useState(createLoadingState());

  const getThreatExplanation = async () => {
    setState(createLoadingState());
    try {
      const response = await aiService.explainThreat(threatType);
      setState({
        isLoading: false,
        error: null,
        data: formatResponse(response)
      });
    } catch (error) {
      setState({
        isLoading: false,
        error: formatError(error),
        data: null
      });
    }
  };

  React.useEffect(() => {
    getThreatExplanation();
  }, [threatType]);

  return (
    <div className="threat-explainer">
      <h2>🛡️ Threat: {threatType}</h2>

      {state.isLoading && (
        <div className="loading">
          <p>📖 Learning about {threatType}...</p>
        </div>
      )}

      {state.error && (
        <div className="error-message">
          ❌ {state.error}
        </div>
      )}

      {state.data && (
        <div className="threat-content">
          <div className="explanation">
            <p>{state.data.explanation}</p>
          </div>

          <div className="prevention">
            <h3>🛡️ How to Protect Yourself:</h3>
            <ul>
              <li>✓ Keep software and OS updated</li>
              <li>✓ Use strong, unique passwords</li>
              <li>✓ Enable two-factor authentication</li>
              <li>✓ Be cautious with email attachments</li>
              <li>✓ Use antivirus/antimalware software</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

// ============================================================================
// EXPORT INTEGRATION GUIDE
// ============================================================================

export default {
  PhishingDetectorIntegration,
  URLCheckerIntegration,
  PasswordAnalyzerIntegration,
  FileSecurityIntegration,
  SecurityChatbotIntegration,
  ThreatExplainerIntegration
};
