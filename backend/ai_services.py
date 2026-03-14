"""
AI Services Layer
=================
Modular services for different cybersecurity capabilities.
Each service uses NVIDIA AI for intelligent analysis and explanations.

Services:
- Phishing Analyzer
- URL Safety Analyzer
- File Risk Explainer
- Password Coach
- Cybersecurity Q&A
- Threat Explanations
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

from nvidia_ai_integration import (
    NVIDIAAIClient, 
    AIResponse, 
    NVIDIAAPIError,
    get_nvidia_client
)


logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    """Standard result format for all AI analyses"""
    analysis_type: str
    question: str
    ai_explanation: str
    tokens_used: int
    confidence: float = 0.85
    error: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "analysis_type": self.analysis_type,
            "question": self.question,
            "explanation": self.ai_explanation,
            "tokens_used": self.tokens_used,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat(),
            "error": self.error
        }


class PhishingAnalyzerService:
    """Analyzes emails and URLs for phishing indicators."""
    
    def __init__(self, client: Optional[NVIDIAAIClient] = None):
        self.client = client or get_nvidia_client()
    
    def analyze_email(
        self, 
        email_content: str, 
        subject: str = "",
        sender: str = ""
    ) -> AnalysisResult:
        """
        Analyze email for phishing indicators.
        
        Args:
            email_content: Full email body
            subject: Email subject line
            sender: Sender email address
        
        Returns:
            AnalysisResult with AI explanation
        """
        try:
            question = f"Analyze this email for phishing:\nFrom: {sender}\nSubject: {subject}\n\n{email_content}"
            
            response = self.client.explain_phishing(
                email_content=email_content,
                subject=subject
            )
            
            return AnalysisResult(
                analysis_type="phishing_email",
                question=question,
                ai_explanation=response.content,
                tokens_used=response.tokens_used,
                confidence=0.85
            )
            
        except NVIDIAAPIError as e:
            logger.error(f"Phishing analysis error: {e}")
            return AnalysisResult(
                analysis_type="phishing_email",
                question=question,
                ai_explanation="",
                tokens_used=0,
                error=str(e)
            )
    
    def analyze_url(self, url: str) -> AnalysisResult:
        """
        Analyze URL for phishing and security risks.
        
        Args:
            url: URL to analyze
        
        Returns:
            AnalysisResult with AI explanation
        """
        try:
            response = self.client.analyze_url_safety(url)
            
            return AnalysisResult(
                analysis_type="phishing_url",
                question=f"Is this URL safe? {url}",
                ai_explanation=response.content,
                tokens_used=response.tokens_used,
                confidence=0.85
            )
            
        except NVIDIAAPIError as e:
            logger.error(f"URL analysis error: {e}")
            return AnalysisResult(
                analysis_type="phishing_url",
                question=f"Is this URL safe? {url}",
                ai_explanation="",
                tokens_used=0,
                error=str(e)
            )


class URLSecurityAnalyzerService:
    """Provides detailed URL security analysis with AI explanations."""
    
    def __init__(self, client: Optional[NVIDIAAIClient] = None):
        self.client = client or get_nvidia_client()
    
    def analyze_with_context(
        self, 
        url: str, 
        domain_info: Optional[Dict[str, str]] = None,
        threats: Optional[List[str]] = None
    ) -> AnalysisResult:
        """
        Analyze URL with additional context information.
        
        Args:
            url: URL to analyze
            domain_info: Domain details (age, reputation, etc.)
            threats: List of detected threats
        
        Returns:
            AnalysisResult with AI explanation
        """
        try:
            context = ""
            if domain_info:
                context += f"Domain info: {domain_info}\n"
            if threats:
                context += f"Detected threats: {', '.join(threats)}\n"
            
            response = self.client.analyze_url_safety(url, context=context)
            
            return AnalysisResult(
                analysis_type="url_security",
                question=f"Analyze URL security: {url}",
                ai_explanation=response.content,
                tokens_used=response.tokens_used,
                confidence=0.88
            )
            
        except NVIDIAAPIError as e:
            logger.error(f"URL security analysis error: {e}")
            return AnalysisResult(
                analysis_type="url_security",
                question=f"Analyze URL security: {url}",
                ai_explanation="",
                tokens_used=0,
                error=str(e)
            )


class PasswordCoachService:
    """Provides password security coaching and improvement suggestions."""
    
    def __init__(self, client: Optional[NVIDIAAIClient] = None):
        self.client = client or get_nvidia_client()
    
    def explain_weakness(
        self,
        password_strength: str,
        score: int,
        entropy: float,
        issues: List[str],
        crack_time: Optional[Dict[str, str]] = None
    ) -> AnalysisResult:
        """
        Explain password weaknesses and provide coaching.
        
        Args:
            password_strength: Strength level (Weak, Fair, Strong, etc.)
            score: Password score (0-100)
            entropy: Shannon entropy value
            issues: List of detected issues
            crack_time: Time to crack estimates
        
        Returns:
            AnalysisResult with coaching
        """
        try:
            analysis = {
                "strength": password_strength,
                "score": score,
                "entropy": entropy,
                "issues": issues,
                "crack_time": crack_time or {}
            }
            
            response = self.client.explain_password_weakness(analysis)
            
            return AnalysisResult(
                analysis_type="password_coaching",
                question="Why is this password weak and how can I improve it?",
                ai_explanation=response.content,
                tokens_used=response.tokens_used,
                confidence=0.90
            )
            
        except NVIDIAAPIError as e:
            logger.error(f"Password coaching error: {e}")
            return AnalysisResult(
                analysis_type="password_coaching",
                question="Why is this password weak and how can I improve it?",
                ai_explanation="",
                tokens_used=0,
                error=str(e)
            )


class FileSecurityService:
    """Analyzes file risks and explains malware indicators."""
    
    def __init__(self, client: Optional[NVIDIAAIClient] = None):
        self.client = client or get_nvidia_client()
    
    def explain_risk(
        self,
        filename: str,
        file_type: str,
        risk_level: str,
        risk_indicators: List[str],
        entropy: Optional[float] = None
    ) -> AnalysisResult:
        """
        Explain file security risks in beginner-friendly language.
        
        Args:
            filename: Name of the file
            file_type: File extension/type
            risk_level: Risk level (High, Medium, Low)
            risk_indicators: List of risk factors
            entropy: File entropy if available
        
        Returns:
            AnalysisResult with explanation
        """
        try:
            analysis = {
                "filename": filename,
                "file_type": file_type,
                "risk_level": risk_level,
                "risk_indicators": risk_indicators,
                "entropy": entropy
            }
            
            response = self.client.explain_file_risk(analysis)
            
            return AnalysisResult(
                analysis_type="file_risk",
                question=f"Why is {filename} risky?",
                ai_explanation=response.content,
                tokens_used=response.tokens_used,
                confidence=0.82
            )
            
        except NVIDIAAPIError as e:
            logger.error(f"File risk analysis error: {e}")
            return AnalysisResult(
                analysis_type="file_risk",
                question=f"Why is {filename} risky?",
                ai_explanation="",
                tokens_used=0,
                error=str(e)
            )


class CybersecurityChatbotService:
    """General-purpose cybersecurity Q&A chatbot."""
    
    def __init__(self, client: Optional[NVIDIAAIClient] = None):
        self.client = client or get_nvidia_client()
        self.conversation_history: List[Dict[str, str]] = []
    
    def ask_question(self, question: str) -> AnalysisResult:
        """
        Ask the cybersecurity chatbot a question.
        
        Args:
            question: Question about cybersecurity
        
        Returns:
            AnalysisResult with answer
        """
        try:
            response = self.client.cybersecurity_qa(question)
            
            # Store in conversation history
            self.conversation_history.append({
                "role": "user",
                "content": question
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": response.content
            })
            
            return AnalysisResult(
                analysis_type="chatbot_qa",
                question=question,
                ai_explanation=response.content,
                tokens_used=response.tokens_used,
                confidence=0.85
            )
            
        except NVIDIAAPIError as e:
            logger.error(f"Chatbot error: {e}")
            return AnalysisResult(
                analysis_type="chatbot_qa",
                question=question,
                ai_explanation="",
                tokens_used=0,
                error=str(e)
            )
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the conversation history."""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []


class ThreatExplainerService:
    """Explains cybersecurity threats in educational detail."""
    
    def __init__(self, client: Optional[NVIDIAAIClient] = None):
        self.client = client or get_nvidia_client()
    
    def explain_threat(self, threat_type: str, context: str = "") -> AnalysisResult:
        """
        Explain a cybersecurity threat.
        
        Args:
            threat_type: Type of threat (phishing, malware, ransomware, etc.)
            context: Additional context about the threat
        
        Returns:
            AnalysisResult with explanation
        """
        try:
            question = f"Explain {threat_type}"
            if context:
                question += f": {context}"
            
            response = self.client.cybersecurity_qa(question)
            
            return AnalysisResult(
                analysis_type="threat_explanation",
                question=question,
                ai_explanation=response.content,
                tokens_used=response.tokens_used,
                confidence=0.87
            )
            
        except NVIDIAAPIError as e:
            logger.error(f"Threat explanation error: {e}")
            return AnalysisResult(
                analysis_type="threat_explanation",
                question=question,
                ai_explanation="",
                tokens_used=0,
                error=str(e)
            )
    
    def explain_best_practice(self, practice: str) -> AnalysisResult:
        """
        Explain a cybersecurity best practice.
        
        Args:
            practice: Best practice to explain
        
        Returns:
            AnalysisResult with explanation
        """
        try:
            question = f"Explain why {practice} is important for cybersecurity"
            response = self.client.cybersecurity_qa(question)
            
            return AnalysisResult(
                analysis_type="best_practice",
                question=question,
                ai_explanation=response.content,
                tokens_used=response.tokens_used,
                confidence=0.86
            )
            
        except NVIDIAAPIError as e:
            logger.error(f"Best practice explanation error: {e}")
            return AnalysisResult(
                analysis_type="best_practice",
                question=question,
                ai_explanation="",
                tokens_used=0,
                error=str(e)
            )


# ============================================================================
# SERVICE FACTORY
# ============================================================================

class AIServicesFactory:
    """Factory for creating AI service instances."""
    
    _client: Optional[NVIDIAAIClient] = None
    _services: Dict[str, Any] = {}
    
    @classmethod
    def set_client(cls, client: NVIDIAAIClient):
        """Set custom NVIDIA AI client."""
        cls._client = client
    
    @classmethod
    def get_phishing_analyzer(cls) -> PhishingAnalyzerService:
        """Get or create phishing analyzer service."""
        if "phishing" not in cls._services:
            cls._services["phishing"] = PhishingAnalyzerService(cls._client)
        return cls._services["phishing"]
    
    @classmethod
    def get_url_analyzer(cls) -> URLSecurityAnalyzerService:
        """Get or create URL analyzer service."""
        if "url" not in cls._services:
            cls._services["url"] = URLSecurityAnalyzerService(cls._client)
        return cls._services["url"]
    
    @classmethod
    def get_password_coach(cls) -> PasswordCoachService:
        """Get or create password coach service."""
        if "password" not in cls._services:
            cls._services["password"] = PasswordCoachService(cls._client)
        return cls._services["password"]
    
    @classmethod
    def get_file_security(cls) -> FileSecurityService:
        """Get or create file security service."""
        if "file" not in cls._services:
            cls._services["file"] = FileSecurityService(cls._client)
        return cls._services["file"]
    
    @classmethod
    def get_chatbot(cls) -> CybersecurityChatbotService:
        """Get or create chatbot service."""
        if "chatbot" not in cls._services:
            cls._services["chatbot"] = CybersecurityChatbotService(cls._client)
        return cls._services["chatbot"]
    
    @classmethod
    def get_threat_explainer(cls) -> ThreatExplainerService:
        """Get or create threat explainer service."""
        if "threat" not in cls._services:
            cls._services["threat"] = ThreatExplainerService(cls._client)
        return cls._services["threat"]


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    import json
    
    print("=" * 70)
    print("AI Services Layer - Examples")
    print("=" * 70)
    print()
    
    try:
        # 1. Phishing Analysis
        print("-" * 70)
        print("1. PHISHING EMAIL ANALYSIS")
        print("-" * 70)
        phishing_service = AIServicesFactory.get_phishing_analyzer()
        
        email = """Subject: Confirm Your Amazon Account
        Please verify your account by clicking the link below immediately.
        http://amaz0n-account-security.com/verify"""
        
        result = phishing_service.analyze_email(
            email_content=email,
            subject="Confirm Your Amazon Account",
            sender="noreply@amazon-security.com"
        )
        
        if result.error:
            print(f"❌ Error: {result.error}")
        else:
            print(result.ai_explanation)
            print(f"\n📊 Tokens: {result.tokens_used}")
        print()
        
        # 2. Password Coaching
        print("-" * 70)
        print("2. PASSWORD COACHING")
        print("-" * 70)
        password_service = AIServicesFactory.get_password_coach()
        
        result = password_service.explain_weakness(
            password_strength="Weak",
            score=35,
            entropy=24.25,
            issues=["Common word", "Predictable numbers", "No special chars"],
            crack_time={"online": "Instantly", "gpu": "Milliseconds"}
        )
        
        if result.error:
            print(f"❌ Error: {result.error}")
        else:
            print(result.ai_explanation)
            print(f"\n📊 Tokens: {result.tokens_used}")
        print()
        
        # 3. Cybersecurity Q&A
        print("-" * 70)
        print("3. CYBERSECURITY CHATBOT")
        print("-" * 70)
        chatbot = AIServicesFactory.get_chatbot()
        
        result = chatbot.ask_question("What is a VPN and why should I use it?")
        
        if result.error:
            print(f"❌ Error: {result.error}")
        else:
            print(result.ai_explanation)
            print(f"\n📊 Tokens: {result.tokens_used}")
        print()
        
        # 4. Threat Explanation
        print("-" * 70)
        print("4. THREAT EXPLANATION")
        print("-" * 70)
        threat_service = AIServicesFactory.get_threat_explainer()
        
        result = threat_service.explain_threat(
            threat_type="Ransomware",
            context="What is it and how do I prevent it?"
        )
        
        if result.error:
            print(f"❌ Error: {result.error}")
        else:
            print(result.ai_explanation)
            print(f"\n📊 Tokens: {result.tokens_used}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
