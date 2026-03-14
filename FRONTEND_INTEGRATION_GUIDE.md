```markdown
# Frontend Integration Guide: NVIDIA AI

Complete guide for connecting React components to NVIDIA AI backend endpoints.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Component Integration](#component-integration)
4. [Error Handling](#error-handling)
5. [Loading States](#loading-states)
6. [Best Practices](#best-practices)
7. [Testing](#testing)

---

## Quick Start

### 1. Install the Service

Copy these two files to your frontend:
- `nvaidaService.js` - NVIDIA AI client service
- `IntegrationExamples.jsx` - Example implementations

### 2. Update App Configuration

In your main App.jsx:

```javascript
import { aiService } from './nvaidaService'

// Configure API base URL if different from localhost:8000
// const customService = new NVidiaAIService('https://api.example.com')
```

### 3. Use in Your Components

```javascript
import { aiService } from './nvaidaService'

const MyComponent = () => {
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleClick = async () => {
    setLoading(true)
    try {
      const result = await aiService.explainPhishing(emailContent)
      setResponse(result)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <button onClick={handleClick} disabled={loading}>
        {loading ? 'Analyzing...' : 'Analyze'}
      </button>
      {response && <p>{response.explanation}</p>}
    </div>
  )
}
```

---

## Installation

### Step 1: Add Service Files

```bash
# Copy NVIDIA AI service to frontend
cp backend/nvaidaService.js frontend/

# Copy integration examples
cp backend/IntegrationExamples.jsx frontend/
```

### Step 2: Set Environment Variables

Create `.env` in your frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=development
```

For production:

```env
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_ENV=production
```

### Step 3: Import Service

In any component where you want to use NVIDIA AI:

```javascript
import { aiService, formatResponse, formatError } from '../nvaidaService'
```

---

## Component Integration

### PhishingDetector Component Update

**Before**: Component only shows local analysis

**After**: Add NVIDIA AI explanation

```javascript
import React, { useState } from 'react'
import { aiService, formatResponse } from '../nvaidaService'

export const PhishingDetector = ({ email, subject, sender }) => {
  const [aiResult, setAiResult] = useState(null)
  const [aiLoading, setAiLoading] = useState(false)
  const [aiError, setAiError] = useState(null)

  // Get local analysis (existing code)
  const localAnalysis = analyzePhishingLocally(email, subject, sender)

  // Add NVIDIA AI analysis
  const getAIAnalysis = async () => {
    setAiLoading(true)
    setAiError(null)
    try {
      const response = await aiService.explainPhishing(email, subject, sender)
      setAiResult(formatResponse(response))
    } catch (error) {
      setAiError(error.message)
    } finally {
      setAiLoading(false)
    }
  }

  return (
    <div className="phishing-detector">
      {/* Existing UI */}
      <div className="local-analysis">
        {/* Your existing analysis display */}
      </div>

      {/* NEW: AI-powered explanation */}
      <button onClick={getAIAnalysis} disabled={aiLoading}>
        {aiLoading ? 'Getting AI explanation...' : 'Explain with AI'}
      </button>

      {aiError && <div className="error">{aiError}</div>}

      {aiResult && (
        <div className="ai-explanation">
          <h3>🤖 AI Coach Explains:</h3>
          <p>{aiResult.explanation}</p>
          <div className="confidence">
            Confidence: {(aiResult.confidence * 100).toFixed(0)}%
          </div>
        </div>
      )}
    </div>
  )
}

export default PhishingDetector
```

### URLChecker Component Update

```javascript
import React, { useState } from 'react'
import { aiService } from '../nvaidaService'

export const URLChecker = ({ url, basicAnalysis }) => {
  const [aiAnalysis, setAiAnalysis] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const analyzeWithAI = async () => {
    setIsLoading(true)
    try {
      // Extract domain info from basic analysis if available
      const domainInfo = basicAnalysis?.domainInfo || {}
      const threats = basicAnalysis?.threats || []

      const response = await aiService.analyzeURL(url, domainInfo, threats)
      setAiAnalysis(response)
    } catch (error) {
      console.error('AI analysis failed:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="url-checker">
      {/* Existing basic analysis */}
      <div className="basic-analysis">
        {basicAnalysis && (
          <>
            <h2>Quick Check</h2>
            <p>Domain: {basicAnalysis.domain}</p>
            <p>Age: {basicAnalysis.age}</p>
          </>
        )}
      </div>

      {/* NEW: AI-powered detailed analysis */}
      <button onClick={analyzeWithAI} disabled={isLoading}>
        {isLoading ? 'Analyzing...' : 'Deep Dive with AI'}
      </button>

      {aiAnalysis && (
        <div className="ai-analysis">
          <h3>Deep Analysis Results</h3>
          <p>{aiAnalysis.explanation}</p>
          <div className={`safety ${aiAnalysis.is_safe ? 'safe' : 'unsafe'}`}>
            {aiAnalysis.is_safe ? '✓ Safe' : '✗ Unsafe'}
          </div>
        </div>
      )}
    </div>
  )
}

export default URLChecker
```

### PasswordAnalyzer Component Update

```javascript
import React, { useState } from 'react'
import { aiService } from '../nvaidaService'

export const PasswordAnalyzer = ({ password }) => {
  const [analysis, setAnalysis] = useState(null)
  const [aiCoaching, setAiCoaching] = useState(null)
  const [coachingLoading, setCoachingLoading] = useState(false)

  // Get local password analysis (existing code)
  React.useEffect(() => {
    const result = analyzePasswordLocal(password)
    setAnalysis(result)
  }, [password])

  // Get AI coaching
  const requestCoaching = async () => {
    if (!analysis) return

    setCoachingLoading(true)
    try {
      const response = await aiService.passwordCoaching({
        strength: analysis.strength,
        score: analysis.score,
        entropy: analysis.entropy,
        issues: analysis.issues,
        crackTime: analysis.crackTime
      })
      setAiCoaching(response)
    } catch (error) {
      console.error('Coaching failed:', error)
    } finally {
      setCoachingLoading(false)
    }
  }

  return (
    <div className="password-analyzer">
      {/* Existing analysis display */}
      {analysis && (
        <div className="analysis">
          <div className="score">{analysis.score}/100</div>
          <div className="strength">{analysis.strength}</div>
          {analysis.issues.map(issue => (
            <p key={issue}>⚠ {issue}</p>
          ))}
        </div>
      )}

      {/* NEW: Get AI coaching */}
      <button onClick={requestCoaching} disabled={coachingLoading || !analysis}>
        {coachingLoading ? 'Getting advice...' : 'Get AI Coach Advice'}
      </button>

      {aiCoaching && (
        <div className="coaching">
          <h3>💡 Coach's Advice:</h3>
          <p>{aiCoaching.explanation}</p>
          <div className="improvements">
            {aiCoaching.improvements?.map(tip => (
              <div key={tip}>✓ {tip}</div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default PasswordAnalyzer
```

### AIAssistant Component Update (Chatbot)

```javascript
import React, { useState, useRef, useEffect } from 'react'
import { aiService } from '../nvaidaService'

export const AIAssistant = () => {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  // Scroll to latest message
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Initialize with greeting
  useEffect(() => {
    setMessages([
      {
        id: 1,
        role: 'assistant',
        content: 'Hello! I\'m your cybersecurity mentor. Ask me anything about staying safe online!'
      }
    ])
  }, [])

  const sendMessage = async () => {
    if (!input.trim()) return

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      role: 'user',
      content: input
    }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      // Get AI response
      const response = await aiService.askSecurityQuestion(input)

      // Add AI message
      const aiMessage = {
        id: messages.length + 2,
        role: 'assistant',
        content: response.answer
      }
      setMessages(prev => [...prev, aiMessage])
    } catch (error) {
      // Add error message
      const errorMessage = {
        id: messages.length + 2,
        role: 'assistant',
        content: `Sorry, I encountered an error. Please try again.`
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="ai-assistant">
      <div className="chat-header">
        <h2>🤖 Cybersecurity Mentor</h2>
      </div>

      <div className="chat-messages">
        {messages.map(msg => (
          <div key={msg.id} className={`message ${msg.role}`}>
            <div className="message-icon">
              {msg.role === 'user' ? '👤' : '🤖'}
            </div>
            <div className="message-content">
              {msg.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant typing">
            <span></span><span></span><span></span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <input
          type="text"
          placeholder="Ask me anything..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={e => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              sendMessage()
            }
          }}
          disabled={isLoading}
        />
        <button onClick={sendMessage} disabled={isLoading || !input.trim()}>
          Send
        </button>
      </div>

      <style jsx>{`
        .message.typing span {
          display: inline-block;
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #999;
          margin: 0 2px;
          animation: bounce 1.4s ease-in-out infinite;
        }
        .message.typing span:nth-child(2) {
          animation-delay: 0.2s;
        }
        .message.typing span:nth-child(3) {
          animation-delay: 0.4s;
        }
        @keyframes bounce {
          0%, 80%, 100% { opacity: 0.3; }
          40% { opacity: 1; }
        }
      `}</style>
    </div>
  )
}

export default AIAssistant
```

---

## Error Handling

### Global Error Boundary

```javascript
import React from 'react'

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, info) {
    console.error('AI Service Error:', error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>❌ Service Error</h2>
          <p>Unable to connect to AI service. Please try again.</p>
          <button onClick={() => window.location.reload()}>
            Reload Page
          </button>
        </div>
      )
    }

    return this.props.children
  }
}
```

### Specific Error Handling

```javascript
// Handle different error types
const handleAPIError = (error) => {
  if (error.message.includes('API Error: 401')) {
    return 'Authentication failed. Please check your API key.'
  } else if (error.message.includes('API Error: 429')) {
    return 'Too many requests. Please wait a moment before trying again.'
  } else if (error.message.includes('API Error: 500')) {
    return 'Server error. Our team is working on it.'
  } else {
    return 'An error occurred. Please try again.'
  }
}
```

---

## Loading States

### Skeleton Loading

```javascript
export const AnalysisSkeleton = () => (
  <div className="skeleton">
    <div className="skeleton-text"></div>
    <div className="skeleton-text"></div>
    <div className="skeleton-text"></div>
  </div>
)

// Usage
{isLoading ? <AnalysisSkeleton /> : <AnalysisResult />}
```

### Loading Spinner

```javascript
export const LoadingSpinner = ({ message = 'Loading...' }) => (
  <div className="spinner-container">
    <div className="spinner"></div>
    <p>{message}</p>
  </div>
)

// CSS
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

---

## Best Practices

### 1. Validate Input Before Sending

```javascript
const validatePhishingInput = (email, subject) => {
  const errors = []

  if (!email || email.trim().length < 10) {
    errors.push('Please provide email content (min 10 characters)')
  }

  if (email.length > 10000) {
    errors.push('Email content too long (max 10000 characters)')
  }

  if (subject && subject.length > 200) {
    errors.push('Subject too long (max 200 characters)')
  }

  return errors
}

// Usage
const inputErrors = validatePhishingInput(email, subject)
if (inputErrors.length > 0) {
  setError(inputErrors[0])
  return
}
```

### 2. Debounce Rapid Requests

```javascript
import { useCallback } from 'react'

export const useDebounce = (fn, delay = 500) => {
  const timeoutRef = useRef(null)

  return useCallback((...args) => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current)
    }
    timeoutRef.current = setTimeout(() => fn(...args), delay)
  }, [fn, delay])
}

// Usage
const debouncedAnalyze = useDebounce(
  async (url) => {
    const result = await aiService.analyzeURL(url)
    setResult(result)
  },
  1000
)
```

### 3. Cache Responses

```javascript
const [responseCache, setResponseCache] = useState({})

const analyzeWithCache = async (url) => {
  const cacheKey = `url_${url}`

  if (responseCache[cacheKey]) {
    return responseCache[cacheKey]
  }

  const response = await aiService.analyzeURL(url)
  setResponseCache(prev => ({
    ...prev,
    [cacheKey]: response
  }))

  return response
}
```

### 4. Handle Abort Requests

```javascript
import { useEffect, useRef } from 'react'

export const useAbortableAPI = () => {
  const abortControllerRef = useRef(null)

  const makeRequest = async (fn) => {
    abortControllerRef.current = new AbortController()
    try {
      return await fn(abortControllerRef.current.signal)
    } catch (error) {
      if (error.name !== 'AbortError') {
        throw error
      }
    }
  }

  const abort = () => {
    abortControllerRef.current?.abort()
  }

  return { makeRequest, abort }
}
```

### 5. Rate Limit on Frontend

```javascript
export const useRateLimit = (maxRequests = 5, windowMs = 60000) => {
  const requests = useRef([])

  const isLimited = () => {
    const now = Date.now()
    requests.current = requests.current.filter(
      time => now - time < windowMs
    )
    return requests.current.length >= maxRequests
  }

  const recordRequest = () => {
    requests.current.push(Date.now())
  }

  return { isLimited, recordRequest }
}
```

---

## Testing

### Unit Test Example

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { PhishingDetectorIntegration } from '../IntegrationExamples'
import * as aiService from '../nvaidaService'

jest.mock('../nvaidaService')

describe('PhishingDetectorIntegration', () => {
  test('displays loading state while analyzing', async () => {
    aiService.aiService.explainPhishing.mockImplementation(
      () => new Promise(resolve => setTimeout(resolve, 100))
    )

    render(<PhishingDetectorIntegration />)

    const button = screen.getByText('Analyze Email')
    fireEvent.click(button)

    expect(screen.getByText('Analyzing...')).toBeInTheDocument()
  })

  test('displays analysis result on success', async () => {
    const mockResponse = {
      explanation: 'This is a phishing email',
      tokens_used: 256,
      confidence: 0.85,
      risk_level: 'High',
      timestamp: new Date().toISOString()
    }

    aiService.aiService.explainPhishing.mockResolvedValue(mockResponse)

    render(<PhishingDetectorIntegration />)

    fireEvent.click(screen.getByText('Analyze Email'))

    await waitFor(() => {
      expect(screen.getByText(/This is a phishing email/)).toBeInTheDocument()
    })
  })

  test('displays error message on failure', async () => {
    aiService.aiService.explainPhishing.mockRejectedValue(
      new Error('API Error')
    )

    render(<PhishingDetectorIntegration />)

    fireEvent.click(screen.getByText('Analyze Email'))

    await waitFor(() => {
      expect(screen.getByText(/Error/)).toBeInTheDocument()
    })
  })
})
```

### Integration Test Example

```javascript
describe('NVIDIA AI Service Integration', () => {
  test('end-to-end phishing analysis', async () => {
    const email = 'Click here to verify account'
    const subject = 'Urgent: Account Verification'

    const response = await aiService.explainPhishing(email, subject)

    expect(response).toHaveProperty('explanation')
    expect(response).toHaveProperty('tokens_used')
    expect(response).toHaveProperty('confidence')
  })
})
```

---

## Environment Configuration

### .env.development

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_LOG_LEVEL=debug
```

### .env.production

```env
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_LOG_LEVEL=error
```

### Load in App.jsx

```javascript
useEffect(() => {
  const apiUrl = process.env.REACT_APP_API_URL
  console.log(`Connected to: ${apiUrl}`)
}, [])
```

---

## Troubleshooting

### "CORS Error"

**Solution**: Ensure backend has CORS enabled

```python
# backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_methods=["*"],
    allow_headers=["*"]
)
```

### "404 Not Found"

**Solution**: Check API URL and endpoint paths

```javascript
// Verify in browser DevTools → Network tab
// Should see requests like:
// POST http://localhost:8000/api/security/nvidia/explain-phishing
```

### "Timeouts"

**Solution**: Increase timeout in nvaidaService.js

```javascript
const options = {
  // ... other options
  signal: AbortSignal.timeout(60000) // 60 seconds
}
```

---

## Summary

✅ **Completed**:
- NVIDIA AI service wrapper (`nvaidaService.js`)
- Example implementations for all features
- Component integration patterns
- Error handling strategies
- Testing examples

✅ **Next Steps**:
1. Copy service files to frontend folder
2. Update environment variables
3. Integrate components one by one
4. Test with backend running
5. Deploy to production

---

**Last Updated**: January 2024  
**Status**: Ready for Production
```
