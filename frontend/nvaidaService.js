/**
 * NVIDIA AI Integration Service
 * =============================
 * Client-side service for calling NVIDIA AI endpoints from React components.
 * 
 * Usage:
 * import { aiService } from './nvaidaService'
 * const response = await aiService.explainPhishing(email, subject)
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// ============================================================================
// API CLIENT CLASS
// ============================================================================

class NVidiaAIService {
  constructor(baseURL = API_BASE_URL) {
    this.baseURL = baseURL;
    this.apiPath = '/api/security/nvidia';
  }

  /**
   * Make API request with error handling
   */
  async request(endpoint, data = null) {
    try {
      const url = `${this.baseURL}${this.apiPath}${endpoint}`;
      
      const options = {
        method: data ? 'POST' : 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      };

      if (data) {
        options.body = JSON.stringify(data);
      }

      const response = await fetch(url, options);

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || `API Error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // ========================================================================
  // PHISHING ANALYSIS
  // ========================================================================

  /**
   * Analyze email for phishing indicators
   * @param {string} emailContent - Full email body
   * @param {string} subject - Email subject line
   * @param {string} sender - Sender email address
   * @returns {Promise<Object>} Analysis result with AI explanation
   */
  async explainPhishing(emailContent, subject = '', sender = '') {
    return this.request('/explain-phishing', {
      email_content: emailContent,
      subject,
      sender
    });
  }

  // ========================================================================
  // URL ANALYSIS
  // ========================================================================

  /**
   * Analyze URL for security threats
   * @param {string} url - URL to analyze
   * @param {Object} domainInfo - Optional domain information
   * @param {Array<string>} threats - Optional list of detected threats
   * @returns {Promise<Object>} Analysis result
   */
  async analyzeURL(url, domainInfo = null, threats = null) {
    return this.request('/analyze-url', {
      url,
      domain_info: domainInfo,
      threats
    });
  }

  // ========================================================================
  // PASSWORD COACHING
  // ========================================================================

  /**
   * Get password security coaching
   * @param {Object} passwordData - Password analysis data
   * @returns {Promise<Object>} Coaching with AI explanation
   */
  async passwordCoaching(passwordData) {
    return this.request('/password-coaching', {
      password_strength: passwordData.strength,
      score: passwordData.score,
      entropy: passwordData.entropy,
      issues: passwordData.issues,
      crack_time: passwordData.crackTime
    });
  }

  // ========================================================================
  // FILE RISK EXPLANATION
  // ========================================================================

  /**
   * Explain file security risks
   * @param {Object} fileData - File analysis data
   * @returns {Promise<Object>} Risk explanation
   */
  async explainFileRisk(fileData) {
    return this.request('/explain-file-risk', {
      filename: fileData.filename,
      file_type: fileData.fileType,
      risk_level: fileData.riskLevel,
      risk_indicators: fileData.riskIndicators,
      entropy: fileData.entropy
    });
  }

  // ========================================================================
  // SECURITY Q&A
  // ========================================================================

  /**
   * Ask cybersecurity chatbot a question
   * @param {string} question - Security question
   * @returns {Promise<Object>} AI answer
   */
  async askSecurityQuestion(question) {
    return this.request('/ask-security-question', {
      question
    });
  }

  // ========================================================================
  // THREAT EXPLANATIONS
  // ========================================================================

  /**
   * Explain a cybersecurity threat
   * @param {string} threatType - Type of threat
   * @param {string} context - Optional context
   * @returns {Promise<Object>} Threat explanation
   */
  async explainThreat(threatType, context = '') {
    return this.request('/explain-threat', {
      threat_type: threatType,
      context
    });
  }

  /**
   * Explain a best practice
   * @param {string} practice - Best practice to explain
   * @returns {Promise<Object>} Best practice explanation
   */
  async explainBestPractice(practice) {
    return this.request('/explain-best-practice', {
      practice
    });
  }

  // ========================================================================
  // CONVERSATION HISTORY
  // ========================================================================

  /**
   * Get chat conversation history
   * @returns {Promise<Object>} Conversation history
   */
  async getChatHistory() {
    return this.request('/chat-history');
  }

  /**
   * Clear chat history
   * @returns {Promise<Object>} Result confirmation
   */
  async clearChatHistory() {
    return this.request('/clear-chat');
  }

  // ========================================================================
  // MONITORING
  // ========================================================================

  /**
   * Get NVIDIA API usage statistics
   * @returns {Promise<Object>} Usage stats
   */
  async getUsageStats() {
    return this.request('/usage-stats');
  }

  /**
   * Check service health
   * @returns {Promise<Object>} Health status
   */
  async healthCheck() {
    return this.request('/health');
  }
}

// ============================================================================
// SINGLETON INSTANCE
// ============================================================================

export const aiService = new NVidiaAIService();

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Format API response for display
 */
export const formatResponse = (response) => {
  return {
    explanation: response.explanation || response.answer || '',
    tokensUsed: response.tokens_used || 0,
    confidence: response.confidence || 0,
    timestamp: response.timestamp || new Date().toISOString(),
    riskLevel: response.risk_level || 'Unknown'
  };
};

/**
 * Display loading state while waiting for API
 */
export const createLoadingState = () => ({
  isLoading: true,
  error: null,
  data: null
});

/**
 * Format error message for user display
 */
export const formatError = (error) => {
  if (error.message.includes('API Error')) {
    return 'Service temporarily unavailable. Please try again.';
  }
  return error.message || 'An error occurred';
};

/**
 * Debounce API calls to prevent multiple simultaneous requests
 */
export const debounceAPI = (func, delay = 500) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

export default aiService;
