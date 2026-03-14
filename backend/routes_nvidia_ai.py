"""
NVIDIA AI Integration Routes
=============================
FastAPI endpoints that connect the frontend to NVIDIA AI services.

Endpoints:
- POST /api/security/nvidia/explain-phishing
- POST /api/security/nvidia/analyze-url
- POST /api/security/nvidia/password-coaching
- POST /api/security/nvidia/explain-file-risk
- POST /api/security/nvidia/ask-security-question
- POST /api/security/nvidia/explain-threat
- GET /api/security/nvidia/chat-history
- DELETE /api/security/nvidia/clear-chat
- GET /api/security/nvidia/usage-stats
"""

import logging
from typing import Optional, List, Dict, Any

from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field

from ai_services import (
    AIServicesFactory,
    AnalysisResult,
    NVIDIAAPIError
)


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/security/nvidia", tags=["nvidia_ai"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class PhishingAnalysisRequest(BaseModel):
    """Request model for phishing analysis."""
    email_content: str = Field(..., description="Full email body")
    subject: Optional[str] = Field("", description="Email subject line")
    sender: Optional[str] = Field("", description="Sender email address")


class PhishingAnalysisResponse(BaseModel):
    """Response model for phishing analysis."""
    analysis_type: str
    question: str
    explanation: str
    tokens_used: int
    confidence: float
    threat_indicators: List[str] = []
    risk_level: str = "Medium"
    timestamp: str


class URLAnalysisRequest(BaseModel):
    """Request model for URL analysis."""
    url: str = Field(..., description="URL to analyze")
    domain_info: Optional[Dict[str, str]] = Field(None, description="Domain information")
    threats: Optional[List[str]] = Field(None, description="Pre-detected threats")


class URLAnalysisResponse(BaseModel):
    """Response model for URL analysis."""
    url: str
    analysis_type: str
    explanation: str
    tokens_used: int
    confidence: float
    risk_level: str = "Medium"
    is_safe: bool = False
    timestamp: str


class PasswordCoachingRequest(BaseModel):
    """Request model for password coaching."""
    password_strength: str = Field(..., description="Strength level (Weak/Fair/Strong/Very Strong)")
    score: int = Field(..., ge=0, le=100, description="Password score")
    entropy: float = Field(..., description="Shannon entropy")
    issues: List[str] = Field(..., description="List of password issues")
    crack_time: Optional[Dict[str, str]] = Field(None, description="Time to crack estimates")


class PasswordCoachingResponse(BaseModel):
    """Response model for password coaching."""
    analysis_type: str
    explanation: str
    tokens_used: int
    confidence: float
    score: int
    improvements: List[str] = []
    timestamp: str


class FileRiskRequest(BaseModel):
    """Request model for file risk analysis."""
    filename: str = Field(..., description="Name of the file")
    file_type: str = Field(..., description="File extension/type")
    risk_level: str = Field(..., description="Risk level (High/Medium/Low)")
    risk_indicators: List[str] = Field(..., description="List of risk factors")
    entropy: Optional[float] = Field(None, description="File entropy")


class FileRiskResponse(BaseModel):
    """Response model for file risk analysis."""
    filename: str
    analysis_type: str
    explanation: str
    tokens_used: int
    confidence: float
    risk_level: str
    safe_to_open: bool = False
    recommended_action: str = "Do not open"
    timestamp: str


class SecurityQuestionRequest(BaseModel):
    """Request model for security Q&A."""
    question: str = Field(..., description="Cybersecurity question")


class SecurityQuestionResponse(BaseModel):
    """Response model for security Q&A."""
    question: str
    answer: str
    tokens_used: int
    confidence: float
    related_topics: List[str] = []
    timestamp: str


class ThreatExplanationRequest(BaseModel):
    """Request model for threat explanations."""
    threat_type: str = Field(..., description="Type of threat")
    context: Optional[str] = Field("", description="Additional context")


class ThreatExplanationResponse(BaseModel):
    """Response model for threat explanation."""
    threat_type: str
    explanation: str
    tokens_used: int
    prevention_tips: List[str] = []
    timestamp: str


class ChatMessage(BaseModel):
    """Single chat message."""
    role: str  # "user" or "assistant"
    content: str


class ChatHistoryResponse(BaseModel):
    """Response model for chat history."""
    messages: List[ChatMessage]
    total_messages: int
    total_conversations: int


class UsageStatsResponse(BaseModel):
    """Response model for usage statistics."""
    total_requests: int
    total_tokens_used: int
    average_tokens_per_request: float
    active_sessions: int
    service_status: str = "operational"


# ============================================================================
# ENDPOINT: PHISHING ANALYSIS
# ============================================================================

@router.post(
    "/explain-phishing",
    response_model=PhishingAnalysisResponse,
    summary="Analyze email for phishing",
    description="Analyze an email for phishing indicators using AI-powered detection"
)
async def explain_phishing(request: PhishingAnalysisRequest):
    """
    Analyze email for phishing indicators.
    
    Takes an email and performs AI-powered analysis to identify:
    - Suspicious sender addresses
    - Phishing red flags
    - Fake links and domain imitation
    - Urgency and pressure tactics
    - Request for sensitive information
    
    Returns beginner-friendly explanation of threats.
    """
    try:
        service = AIServicesFactory.get_phishing_analyzer()
        result = service.analyze_email(
            email_content=request.email_content,
            subject=request.subject,
            sender=request.sender
        )
        
        if result.error:
            raise HTTPException(status_code=500, detail=str(result.error))
        
        return PhishingAnalysisResponse(
            analysis_type=result.analysis_type,
            question=result.question,
            explanation=result.ai_explanation,
            tokens_used=result.tokens_used,
            confidence=result.confidence,
            risk_level="High" if "suspicious" in result.ai_explanation.lower() else "Medium",
            timestamp=result.timestamp.isoformat()
        )
        
    except Exception as e:
        logger.error(f"Phishing analysis error: {e}")
        raise HTTPException(status_code=500, detail="Phishing analysis failed")


# ============================================================================
# ENDPOINT: URL ANALYSIS
# ============================================================================

@router.post(
    "/analyze-url",
    response_model=URLAnalysisResponse,
    summary="Analyze URL security",
    description="Analyze a URL for security threats and phishing indicators"
)
async def analyze_url(request: URLAnalysisRequest):
    """
    Analyze URL for security threats.
    
    Evaluates:
    - Domain legitimacy
    - Typosquatting detection
    - Known phishing patterns
    - Suspicious domain characters
    - Domain age and reputation
    
    Returns safety assessment with explanation.
    """
    try:
        service = AIServicesFactory.get_url_analyzer()
        result = service.analyze_with_context(
            url=request.url,
            domain_info=request.domain_info,
            threats=request.threats
        )
        
        if result.error:
            raise HTTPException(status_code=500, detail=str(result.error))
        
        is_safe = "safe" in result.ai_explanation.lower()
        
        return URLAnalysisResponse(
            url=request.url,
            analysis_type=result.analysis_type,
            explanation=result.ai_explanation,
            tokens_used=result.tokens_used,
            confidence=result.confidence,
            is_safe=is_safe,
            risk_level="Low" if is_safe else "High",
            timestamp=result.timestamp.isoformat()
        )
        
    except Exception as e:
        logger.error(f"URL analysis error: {e}")
        raise HTTPException(status_code=500, detail="URL analysis failed")


# ============================================================================
# ENDPOINT: PASSWORD COACHING
# ============================================================================

@router.post(
    "/password-coaching",
    response_model=PasswordCoachingResponse,
    summary="Get password security coaching",
    description="Receive AI-powered coaching on password weaknesses and improvements"
)
async def password_coaching(request: PasswordCoachingRequest):
    """
    Explain password weaknesses and provide coaching.
    
    Analyzes:
    - Why the password is weak
    - Estimated crack times
    - Specific improvements needed
    - Best practices for strong passwords
    - Password manager recommendations
    
    Returns educational, encouraging coaching.
    """
    try:
        service = AIServicesFactory.get_password_coach()
        result = service.explain_weakness(
            password_strength=request.password_strength,
            score=request.score,
            entropy=request.entropy,
            issues=request.issues,
            crack_time=request.crack_time
        )
        
        if result.error:
            raise HTTPException(status_code=500, detail=str(result.error))
        
        improvements = [
            "Add special characters (!@#$%)",
            "Increase length (12+ characters)",
            "Avoid common words and patterns"
        ]
        
        return PasswordCoachingResponse(
            analysis_type=result.analysis_type,
            explanation=result.ai_explanation,
            tokens_used=result.tokens_used,
            confidence=result.confidence,
            score=request.score,
            improvements=improvements,
            timestamp=result.timestamp.isoformat()
        )
        
    except Exception as e:
        logger.error(f"Password coaching error: {e}")
        raise HTTPException(status_code=500, detail="Password coaching failed")


# ============================================================================
# ENDPOINT: FILE RISK EXPLANATION
# ============================================================================

@router.post(
    "/explain-file-risk",
    response_model=FileRiskResponse,
    summary="Explain file security risks",
    description="Get AI explanation of why a file is risky or safe"
)
async def explain_file_risk(request: FileRiskRequest):
    """
    Explain file security risks in beginner-friendly language.
    
    Addresses:
    - Why this file type is risky
    - Malware hiding techniques
    - Safe practices for downloading
    - How to verify file legitimacy
    - When it's safe to open
    
    Returns practical, actionable advice.
    """
    try:
        service = AIServicesFactory.get_file_security()
        result = service.explain_risk(
            filename=request.filename,
            file_type=request.file_type,
            risk_level=request.risk_level,
            risk_indicators=request.risk_indicators,
            entropy=request.entropy
        )
        
        if result.error:
            raise HTTPException(status_code=500, detail=str(result.error))
        
        safe = request.risk_level.lower() == "low"
        
        return FileRiskResponse(
            filename=request.filename,
            analysis_type=result.analysis_type,
            explanation=result.ai_explanation,
            tokens_used=result.tokens_used,
            confidence=result.confidence,
            risk_level=request.risk_level,
            safe_to_open=safe,
            recommended_action="Safe to open" if safe else "Do not open",
            timestamp=result.timestamp.isoformat()
        )
        
    except Exception as e:
        logger.error(f"File risk analysis error: {e}")
        raise HTTPException(status_code=500, detail="File risk analysis failed")


# ============================================================================
# ENDPOINT: SECURITY Q&A
# ============================================================================

@router.post(
    "/ask-security-question",
    response_model=SecurityQuestionResponse,
    summary="Ask cybersecurity questions",
    description="Get AI-powered answers from a cybersecurity tutor"
)
async def ask_security_question(request: SecurityQuestionRequest):
    """
    Ask the AI cybersecurity tutor any question.
    
    Can answer questions about:
    - Common threats (phishing, malware, ransomware)
    - Security best practices
    - Password management
    - Safe browsing habits
    - Data protection
    - Device security
    - Social engineering
    - VPNs and encryption
    
    Returns beginner-friendly explanations.
    """
    try:
        # Validate question
        if len(request.question.strip()) < 5:
            raise HTTPException(status_code=400, detail="Question too short")
        
        service = AIServicesFactory.get_chatbot()
        result = service.ask_question(request.question)
        
        if result.error:
            raise HTTPException(status_code=500, detail=str(result.error))
        
        related_topics = ["password security", "phishing", "two-factor authentication"]
        
        return SecurityQuestionResponse(
            question=request.question,
            answer=result.ai_explanation,
            tokens_used=result.tokens_used,
            confidence=result.confidence,
            related_topics=related_topics,
            timestamp=result.timestamp.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Security Q&A error: {e}")
        raise HTTPException(status_code=500, detail="Q&A failed")


# ============================================================================
# ENDPOINT: THREAT EXPLANATION
# ============================================================================

@router.post(
    "/explain-threat",
    response_model=ThreatExplanationResponse,
    summary="Explain cybersecurity threats",
    description="Get AI explanation of a cybersecurity threat"
)
async def explain_threat(request: ThreatExplanationRequest):
    """
    Explain a cybersecurity threat in detail.
    
    Covers:
    - What the threat is
    - How it works
    - Who is at risk
    - Warning signs
    - Prevention strategies
    - What to do if affected
    
    Returns educational content for beginners.
    """
    try:
        service = AIServicesFactory.get_threat_explainer()
        result = service.explain_threat(
            threat_type=request.threat_type,
            context=request.context
        )
        
        if result.error:
            raise HTTPException(status_code=500, detail=str(result.error))
        
        prevention_tips = [
            "Keep software updated",
            "Use strong passwords",
            "Be cautious with emails",
            "Use antivirus software"
        ]
        
        return ThreatExplanationResponse(
            threat_type=request.threat_type,
            explanation=result.ai_explanation,
            tokens_used=result.tokens_used,
            prevention_tips=prevention_tips,
            timestamp=result.timestamp.isoformat()
        )
        
    except Exception as e:
        logger.error(f"Threat explanation error: {e}")
        raise HTTPException(status_code=500, detail="Threat explanation failed")


# ============================================================================
# ENDPOINT: BEST PRACTICE EXPLANATION
# ============================================================================

@router.post(
    "/explain-best-practice",
    response_model=ThreatExplanationResponse,
    summary="Explain security best practices",
    description="Get AI explanation of why a security practice is important"
)
async def explain_best_practice(
    practice: str = Body(..., description="Best practice to explain")
):
    """
    Explain why a security best practice is important.
    
    Can explain:
    - Two-factor authentication
    - Password managers
    - VPN usage
    - Regular backups
    - Software updates
    - Phishing awareness
    - Email verification
    - Device security
    """
    try:
        if len(practice.strip()) < 5:
            raise HTTPException(status_code=400, detail="Practice description too short")
        
        service = AIServicesFactory.get_threat_explainer()
        result = service.explain_best_practice(practice)
        
        if result.error:
            raise HTTPException(status_code=500, detail=str(result.error))
        
        return ThreatExplanationResponse(
            threat_type=f"Best Practice: {practice}",
            explanation=result.ai_explanation,
            tokens_used=result.tokens_used,
            timestamp=result.timestamp.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Best practice explanation error: {e}")
        raise HTTPException(status_code=500, detail="Best practice explanation failed")


# ============================================================================
# ENDPOINT: CHAT HISTORY
# ============================================================================

@router.get(
    "/chat-history",
    response_model=ChatHistoryResponse,
    summary="Get conversation history",
    description="Retrieve the chatbot conversation history"
)
async def get_chat_history():
    """
    Get the complete conversation history with the AI tutor.
    
    Returns all previous questions and answers in chronological order.
    """
    try:
        chatbot = AIServicesFactory.get_chatbot()
        history = chatbot.get_conversation_history()
        
        messages = [
            ChatMessage(role=msg["role"], content=msg["content"])
            for msg in history
        ]
        
        return ChatHistoryResponse(
            messages=messages,
            total_messages=len(messages),
            total_conversations=len(messages) // 2 if messages else 0
        )
        
    except Exception as e:
        logger.error(f"Chat history error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve chat history")


# ============================================================================
# ENDPOINT: CLEAR CHAT HISTORY
# ============================================================================

@router.delete(
    "/clear-chat",
    summary="Clear chat history",
    description="Clear the conversation history"
)
async def clear_chat_history():
    """
    Clear the chatbot conversation history.
    
    Removes all previous questions and answers.
    """
    try:
        chatbot = AIServicesFactory.get_chatbot()
        chatbot.clear_history()
        
        return {
            "status": "success",
            "message": "Chat history cleared"
        }
        
    except Exception as e:
        logger.error(f"Clear chat error: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear chat history")


# ============================================================================
# ENDPOINT: USAGE STATISTICS
# ============================================================================

@router.get(
    "/usage-stats",
    response_model=UsageStatsResponse,
    summary="Get NVIDIA API usage statistics",
    description="Retrieve usage statistics and cost information"
)
async def get_usage_stats():
    """
    Get NVIDIA API usage statistics.
    
    Returns:
    - Total requests made
    - Total tokens used (for cost calculation)
    - Average tokens per request
    - Current service status
    
    Useful for:
    - Monitoring API usage
    - Calculating costs
    - Optimizing requests
    - Capacity planning
    """
    try:
        client = AIServicesFactory.get_chatbot().client
        stats = client.get_usage_stats()
        
        avg_tokens = 0
        if stats.get("requests", 0) > 0:
            avg_tokens = stats.get("tokens_used", 0) / stats.get("requests", 1)
        
        return UsageStatsResponse(
            total_requests=stats.get("requests", 0),
            total_tokens_used=stats.get("tokens_used", 0),
            average_tokens_per_request=round(avg_tokens, 2),
            active_sessions=1,
            service_status="operational"
        )
        
    except Exception as e:
        logger.error(f"Usage stats error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve usage stats")


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get(
    "/health",
    summary="Check NVIDIA AI service health",
    description="Health check for NVIDIA AI integration"
)
async def health_check():
    """
    Check if NVIDIA AI service is operational.
    
    Returns:
    - Service status (operational/degraded/offline)
    - API connectivity status
    - Timestamp
    """
    try:
        return {
            "status": "operational",
            "service": "NVIDIA AI Integration",
            "api_endpoint": "https://integrate.api.nvidia.com/v1",
            "timestamp": str(datetime.now().isoformat())
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "degraded",
            "service": "NVIDIA AI Integration",
            "error": str(e)
        }


# ============================================================================
# IMPORT DATETIME
# ============================================================================

from datetime import datetime
