```markdown
# NVIDIA AI Integration Setup Guide

Complete guide for integrating NVIDIA AI APIs into the Security Assistant platform.

## Table of Contents
1. [Getting Your API Key](#getting-your-api-key)
2. [Environment Configuration](#environment-configuration)
3. [Installation & Setup](#installation--setup)
4. [Using the AI Services](#using-the-ai-services)
5. [API Endpoints](#api-endpoints)
6. [Monitoring & Costs](#monitoring--costs)
7. [Troubleshooting](#troubleshooting)
8. [Security Best Practices](#security-best-practices)

---

## Getting Your API Key

### Step 1: Create NVIDIA Account

1. Visit [https://build.nvidia.com](https://build.nvidia.com)
2. Click "Sign In" in the top right
3. Create a free NVIDIA developer account or sign in with existing credentials
4. Complete email verification if required

### Step 2: Generate API Key

1. After signing in, go to your **Profile** or **API Keys** section
2. Click **"Generate New API Key"**
3. Select scope: **General audience models**
4. Copy the generated key (format: `nvapi-xxxxxxxxxxxxxxxx...`)
   - Keys are typically 60+ characters
   - Must start with `nvapi-` prefix
5. **Store securely** - this is your only chance to copy it
6. If you lose it, regenerate a new one

### Step 3: Test Your Key

```bash
# Test connectivity with your API key
curl -X POST https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta/llama-3.1-8b-instruct",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 100
  }'
```

---

## Environment Configuration

### Step 1: Create .env File

1. Copy `.env.example` to `.env` in the project root:

```bash
cp .env.example .env
```

2. Edit `.env` and add your NVIDIA API key:

```env
NVIDIA_API_KEY=nvapi-your-actual-key-here
NVIDIA_API_ENDPOINT=https://integrate.api.nvidia.com/v1
NVIDIA_MODEL_MAIN=meta/llama-3.1-70b-instruct
NVIDIA_MODEL_FAST=meta/llama-3.1-8b-instruct
```

### Step 2: Verify Configuration

```bash
# Python: Verify environment variable is loaded
python -c "import os; print('✓ API Key loaded' if os.getenv('NVIDIA_API_KEY') else '✗ No API Key')"
```

### Step 3: Secure Your .env File

**CRITICAL**: Protect your .env file:

```bash
# Make .env readable only by owner (Linux/Mac)
chmod 600 .env

# Windows: Use File Properties to restrict access
# Right-click .env → Properties → Security → Advanced → Disable inheritance
```

Add to `.gitignore` to prevent committing secrets:

```bash
# .gitignore
.env
.env.local
.env.*.local
*.key
secr*
```

---

## Installation & Setup

### Step 1: Install Dependencies

```bash
# Install Python packages for NVIDIA AI integration
pip install openai python-dotenv pydantic fastapi

# Or use requirements file
pip install -r backend/requirements.txt
```

### Step 2: Update Main Application

Add NVIDIA AI routes to your FastAPI main application (`backend/main.py`):

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes_nvidia_ai import router as nvidia_router
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Security Assistant API",
    description="AI-powered cybersecurity awareness platform"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include NVIDIA AI routes
app.include_router(nvidia_router)

# Other routes...
```

### Step 3: Test the Integration

```bash
# Start the FastAPI server
uvicorn main:app --reload --port 8000

# In another terminal - Test phishing analysis
curl -X POST http://localhost:8000/api/security/nvidia/explain-phishing \
  -H "Content-Type: application/json" \
  -d '{
    "email_content": "Click here to verify your account",
    "subject": "Verify Account",
    "sender": "noreply@fake-bank.com"
  }'
```

---

## Using the AI Services

### Service Classes

The NVIDIA AI integration provides modular services:

#### 1. PhishingAnalyzerService

```python
from ai_services import AIServicesFactory

# Get the service
phishing_service = AIServicesFactory.get_phishing_analyzer()

# Analyze email
result = phishing_service.analyze_email(
    email_content="Your account will be closed. Click now!",
    subject="Urgent: Verify Account",
    sender="support@fake-bank.com"
)

print(result.ai_explanation)  # Beginner-friendly threat explanation
print(f"Tokens used: {result.tokens_used}")
```

#### 2. URLSecurityAnalyzerService

```python
# Get the service
url_service = AIServicesFactory.get_url_analyzer()

# Analyze URL with context
result = url_service.analyze_with_context(
    url="https://amaz0n-account.com/verify",
    domain_info={"domain": "amaz0n-account.com", "age_days": 7},
    threats=["typosquatting", "phishing"]
)

print(result.ai_explanation)
```

#### 3. PasswordCoachService

```python
# Get the service
password_service = AIServicesFactory.get_password_coach()

# Provide coaching
result = password_service.explain_weakness(
    password_strength="Weak",
    score=35,
    entropy=24.25,
    issues=["Common word", "No special characters", "Predictable pattern"],
    crack_time={"online": "Instantly", "gpu": "Milliseconds"}
)

print(result.ai_explanation)
```

#### 4. FileSecurityService

```python
# Get the service
file_service = AIServicesFactory.get_file_security()

# Explain file risks
result = file_service.explain_risk(
    filename="document.exe",
    file_type="exe",
    risk_level="High",
    risk_indicators=["executable", "unknown_source", "high_entropy"],
    entropy=7.85
)

print(result.ai_explanation)
```

#### 5. CybersecurityChatbotService

```python
# Get the service
chatbot = AIServicesFactory.get_chatbot()

# Ask questions
result = chatbot.ask_question("What is a VPN and why should I use it?")
print(result.ai_explanation)

# Get conversation history
history = chatbot.get_conversation_history()
for msg in history:
    print(f"{msg['role']}: {msg['content']}")

# Clear history
chatbot.clear_history()
```

#### 6. ThreatExplainerService

```python
# Get the service
threat_service = AIServicesFactory.get_threat_explainer()

# Explain threats
result = threat_service.explain_threat(
    threat_type="Ransomware",
    context="How does it work and how do I prevent it?"
)
print(result.ai_explanation)

# Explain best practices
result = threat_service.explain_best_practice("Two-factor authentication")
print(result.ai_explanation)
```

---

## API Endpoints

### Phishing Analysis

**POST** `/api/security/nvidia/explain-phishing`

```json
REQUEST:
{
  "email_content": "Urgent: Verify your account immediately",
  "subject": "Account Verification Required",
  "sender": "support@fake-bank.com"
}

RESPONSE:
{
  "analysis_type": "phishing_email",
  "explanation": "This email contains several phishing red flags...",
  "tokens_used": 256,
  "confidence": 0.85,
  "risk_level": "High",
  "timestamp": "2024-01-15T10:30:00"
}
```

### URL Analysis

**POST** `/api/security/nvidia/analyze-url`

```json
REQUEST:
{
  "url": "https://amaz0n-account.com/verify",
  "domain_info": {"domain": "amaz0n-account.com", "age_days": 7},
  "threats": ["typosquatting"]
}

RESPONSE:
{
  "url": "https://amaz0n-account.com/verify",
  "analysis_type": "url_security",
  "explanation": "This URL appears to be a typosquatted domain...",
  "tokens_used": 180,
  "confidence": 0.88,
  "is_safe": false,
  "risk_level": "High",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Password Coaching

**POST** `/api/security/nvidia/password-coaching`

```json
REQUEST:
{
  "password_strength": "Weak",
  "score": 35,
  "entropy": 24.25,
  "issues": ["Common word", "Predictable numbers", "No special chars"],
  "crack_time": {
    "online": "Instantly",
    "gpu": "Milliseconds",
    "offline": "Hours"
  }
}

RESPONSE:
{
  "analysis_type": "password_coaching",
  "explanation": "Your password uses common words and patterns...",
  "tokens_used": 320,
  "confidence": 0.90,
  "score": 35,
  "improvements": [
    "Add special characters (!@#$%)",
    "Use 12+ characters",
    "Avoid dictionary words"
  ],
  "timestamp": "2024-01-15T10:30:00"
}
```

### File Risk Explanation

**POST** `/api/security/nvidia/explain-file-risk`

```json
REQUEST:
{
  "filename": "document.exe",
  "file_type": "exe",
  "risk_level": "High",
  "risk_indicators": ["executable", "unknown_source", "high_entropy"],
  "entropy": 7.85
}

RESPONSE:
{
  "filename": "document.exe",
  "analysis_type": "file_risk",
  "explanation": "EXE files are executables that can run code...",
  "tokens_used": 256,
  "confidence": 0.82,
  "risk_level": "High",
  "safe_to_open": false,
  "recommended_action": "Do not open",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Security Q&A

**POST** `/api/security/nvidia/ask-security-question`

```json
REQUEST:
{
  "question": "What is two-factor authentication and why is it important?"
}

RESPONSE:
{
  "question": "What is two-factor authentication and why is it important?",
  "answer": "Two-factor authentication (2FA) is a security method that requires...",
  "tokens_used": 400,
  "confidence": 0.85,
  "related_topics": ["password_security", "account_security"],
  "timestamp": "2024-01-15T10:30:00"
}
```

### Threat Explanation

**POST** `/api/security/nvidia/explain-threat`

```json
REQUEST:
{
  "threat_type": "Ransomware",
  "context": "How does it work and how do I prevent it?"
}

RESPONSE:
{
  "threat_type": "Ransomware",
  "explanation": "Ransomware is malicious software that encrypts...",
  "tokens_used": 380,
  "prevention_tips": [
    "Keep software updated",
    "Use strong passwords",
    "Backup important files",
    "Be cautious with email attachments"
  ],
  "timestamp": "2024-01-15T10:30:00"
}
```

### Chat History

**GET** `/api/security/nvidia/chat-history`

```json
RESPONSE:
{
  "messages": [
    {
      "role": "user",
      "content": "What is phishing?"
    },
    {
      "role": "assistant",
      "content": "Phishing is a type of social engineering attack..."
    }
  ],
  "total_messages": 8,
  "total_conversations": 4
}
```

### Usage Statistics

**GET** `/api/security/nvidia/usage-stats`

```json
RESPONSE:
{
  "total_requests": 42,
  "total_tokens_used": 15240,
  "average_tokens_per_request": 362.86,
  "active_sessions": 1,
  "service_status": "operational"
}
```

---

## Monitoring & Costs

### Understanding Token Usage

**Token Pricing** (as of January 2024):
- **70B Model (Main)**: Input $0.30/1M tokens, Output $1.00/1M tokens
- **8B Model (Fast)**: Input $0.05/1M tokens, Output $0.15/1M tokens
- **Embedding Model**: $0.02/1M tokens

### Estimating Costs

```
Formula: (input_tokens × input_price + output_tokens × output_price) / 1,000,000

Example (70B model):
- Input: 200 tokens × $0.30/1M = $0.00006
- Output: 500 tokens × $1.00/1M = $0.0005
- Total: ~$0.00056 per request

For 1000 requests/month:
- Estimated cost: ~$0.56/month (70B model)
- With 8B model: ~$0.12/month (much cheaper)
```

### Monitoring Usage

```python
# Check usage statistics
from ai_services import AIServicesFactory

chatbot = AIServicesFactory.get_chatbot()
stats = chatbot.client.get_usage_stats()

print(f"Total requests: {stats['requests']}")
print(f"Total tokens: {stats['tokens_used']}")
print(f"Avg tokens/request: {stats['tokens_used']/stats['requests']}")

# Estimate monthly cost (using 70B model pricing)
PRICE_PER_1M = 0.30 + 1.00  # input + output average
monthly_cost = (stats['tokens_used'] * PRICE_PER_1M) / 1_000_000_000 * 30
print(f"Estimated monthly cost: ${monthly_cost:.2f}")
```

### Setting Rate Limits

```python
# In .env
RATE_LIMIT_REQUESTS=100      # Max 100 requests
RATE_LIMIT_PERIOD=3600       # Per 1 hour

# Implementation example
import time
from functools import wraps

request_times = []

def rate_limit(max_requests: int, period_seconds: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old requests outside the period
            request_times[:] = [t for t in request_times if t > now - period_seconds]
            
            if len(request_times) >= max_requests:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            
            request_times.append(now)
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## Troubleshooting

### Issue: "API Key not found"

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Verify API key format
grep NVIDIA_API_KEY .env

# Reload environment variables
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('NVIDIA_API_KEY'))"
```

### Issue: "Connection timeout"

**Solution:**
```python
# Add timeout configuration
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1",
    timeout=30.0  # 30 second timeout
)
```

### Issue: "Invalid API Key"

**Solution:**
```bash
# Regenerate key at https://build.nvidia.com
# 1. Go to your API Keys section
# 2. Delete old key
# 3. Generate new key
# 4. Update .env with new key
# 5. Restart application
```

### Issue: "Model not found"

**Solution:**
```bash
# Verify model names in .env
# Latest models:
# - meta/llama-3.1-70b-instruct (70 billion parameters)
# - meta/llama-3.1-8b-instruct (8 billion parameters)
# - nvidia/nv-embedqa-e5-v5 (embeddings)

# List available models:
# Visit https://build.nvidia.com/meta/llama-3_1-70b-instruct
```

### Issue: "Rate limited (429 error)"

**Solution:**
```python
# Implement exponential backoff
import time
import random

def retry_with_backoff(max_retries=3):
    for attempt in range(max_retries):
        try:
            return make_api_call()
        except RateLimitError:
            wait_time = 2 ** attempt + random.uniform(0, 1)
            print(f"Rate limited. Retrying in {wait_time:.1f}s...")
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

---

## Security Best Practices

### 1. API Key Security

✅ **DO:**
```bash
# Rotate keys periodically (every 30-90 days)
# Store in .env file with restricted permissions
chmod 600 .env

# Use environment variables, never hardcode
api_key = os.getenv("NVIDIA_API_KEY")

# Use key rotation strategy
# Keep old and new key for 24 hours during migration
```

❌ **DON'T:**
```python
# ❌ Never hardcode API keys
api_key = "nvapi-xxxxx"

# ❌ Never commit .env to git
git add .env  # DON'T DO THIS

# ❌ Never use API key in frontend JavaScript
# Always call from backend only
```

### 2. Request Validation

```python
# Validate user input before sending to API
from pydantic import BaseModel, Field

class SecurityQuestionRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=500)
    # Prevents injection attacks and spam

# Sanitize email content
import re

def sanitize_email(email_content: str) -> str:
    # Remove potential injection attempts
    return re.sub(r'[<>{}[\]"]', '', email_content)
```

### 3. Response Handling

```python
# Never expose API key in responses
response = {
    "explanation": result.ai_explanation,
    "tokens_used": result.tokens_used,
    # ❌ DON'T include: "api_key": api_key
}

# Always validate response structure
if not isinstance(result.ai_explanation, str):
    log_error("Invalid response structure")
    return error_response()
```

### 4. Logging & Monitoring

```python
import logging

logger = logging.getLogger(__name__)

# ✅ Log API calls for audit trail
logger.info(f"API call: {endpoint} - Tokens: {tokens_used}")

# ❌ Never log sensitive data
logger.info(f"API Key: {api_key}")  # DON'T DO THIS

# Monitor for suspicious activity
if tokens_used > 10000:  # Unusually high
    logger.warning("High token usage detected")
```

### 5. Rate Limiting & Quotas

```python
# Implement rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/security/nvidia/explain-phishing")
@limiter.limit("100/hour")  # Max 100 requests per hour
async def explain_phishing(request: PhishingAnalysisRequest):
    # API endpoint implementation
    pass
```

### 6. Data Privacy

```python
# ✅ DO process data securely
- Don't store email content long-term
- Don't store passwords or personal data
- Clear sensitive data from memory after processing

# ✅ DO encrypt sensitive data in transit
- Always use HTTPS in production
- Use SSL/TLS certificates
```

### 7. Fallback & Resilience

```python
# Handle API failures gracefully
from ai_services import NVIDIAAPIError

try:
    response = client.explain_phishing(email_content)
except NVIDIAAPIError as e:
    logger.error(f"NVIDIA API error: {e}")
    # Use cached response or fallback explanation
    return get_fallback_explanation()
```

---

## Production Deployment

### Environment-Specific Configuration

**Development (.env.dev):**
```env
NVIDIA_API_KEY=nvapi-dev-key
ENVIRONMENT=development
LOG_LEVEL=DEBUG
RATE_LIMIT_REQUESTS=1000
```

**Production (.env.prod):**
```env
NVIDIA_API_KEY=nvapi-prod-key
ENVIRONMENT=production
LOG_LEVEL=ERROR
RATE_LIMIT_REQUESTS=100
MONITOR_ENABLED=true
```

### Docker Setup

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Security: Don't copy .env into image
# Use environment variables at runtime
RUN chmod +x startup.sh

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Deploy with environment variables
docker run -e NVIDIA_API_KEY=$NVIDIA_API_KEY \
           -e NVIDIA_MODEL_MAIN=meta/llama-3.1-70b-instruct \
           -p 8000:8000 \
           security-assistant:latest
```

---

## Next Steps

1. ✅ Set up NVIDIA API key
2. ✅ Configure .env file
3. ✅ Install dependencies
4. ✅ Test integration with curl
5. ✅ Connect frontend components
6. ✅ Handle errors and fallbacks
7. ✅ Monitor usage and costs
8. ✅ Deploy to production

## Support Resources

- **NVIDIA Build Portal**: https://build.nvidia.com
- **API Documentation**: https://docs.nvidia.com/cloud/cloud-partner/api-docs
- **GitHub Issues**: Report bugs and request features
- **Community Forum**: Get help from other developers

---

**Last Updated**: January 2024  
**Status**: Production Ready
```
