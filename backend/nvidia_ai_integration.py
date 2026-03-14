"""
NVIDIA AI Integration Module
=============================
Integrates NVIDIA AI models for intelligent cybersecurity analysis and explanations.

Supported Models:
- meta/llama-3.1-70b-instruct (Main AI Assistant - most capable)
- meta/llama-3.1-8b-instruct (Fast Analysis - quick responses)
- nvidia/nv-embedqa-e5-v5 (Embeddings - knowledge search)

Documentation:
https://build.nvidia.com/meta/llama-3-1-70b-instruct

Example API Key Format:
nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""

import os
import json
from typing import Optional, List, Dict, Any, Generator
from dataclasses import dataclass
from datetime import datetime
import logging

# OpenAI SDK is compatible with NVIDIA API
try:
    from openai import OpenAI
except ImportError:
    raise ImportError("Install openai: pip install openai")


logger = logging.getLogger(__name__)


@dataclass
class AIResponse:
    """Structured response from NVIDIA AI"""
    content: str
    model: str
    tokens_used: int
    temperature: float
    timestamp: datetime
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "content": self.content,
            "model": self.model,
            "tokens_used": self.tokens_used,
            "temperature": self.temperature,
            "timestamp": self.timestamp.isoformat(),
        }


class NVIDIAAPIError(Exception):
    """Custom exception for NVIDIA API errors"""
    pass


class NVIDIAAIClient:
    """
    NVIDIA AI Client for interacting with NVIDIA AI Foundation Models.
    
    Uses OpenAI SDK for API compatibility.
    Endpoints: https://integrate.api.nvidia.com/v1
    """
    
    # Available models
    MODEL_MAIN = "meta/llama-3.1-70b-instruct"  # Most capable (70B parameters)
    MODEL_FAST = "meta/llama-3.1-8b-instruct"   # Fast responses (8B parameters)
    MODEL_EMBEDDING = "nvidia/nv-embedqa-e5-v5" # Knowledge search
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize NVIDIA AI client.
        
        Args:
            api_key: NVIDIA API key. If None, reads from NVIDIA_API_KEY env var.
                    Format: nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        
        Raises:
            NVIDIAAPIError: If API key is missing or invalid
        """
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY")
        
        if not self.api_key:
            raise NVIDIAAPIError(
                "NVIDIA API key not found. Set NVIDIA_API_KEY environment variable. "
                "Get your key from: https://build.nvidia.com"
            )
        
        if not self.api_key.startswith("nvapi-"):
            logger.warning("NVIDIA API key should start with 'nvapi-'. Got: %s", self.api_key[:10])
        
        # Initialize OpenAI client with NVIDIA endpoint
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key
        )
        
        self.request_count = 0
        self.total_tokens = 0
    
    def generate(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        top_p: float = 0.7,
        max_tokens: int = 1024,
        stream: bool = False,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        """
        Generate response from NVIDIA AI model.
        
        Args:
            model: Model name (use MODEL_MAIN, MODEL_FAST constants)
            messages: List of message dicts with 'role' and 'content'
            temperature: 0.0-1.0 (0=deterministic, 1=creative)
            top_p: Nucleus sampling parameter
            max_tokens: Maximum response tokens
            stream: Whether to stream response
            system_prompt: Optional system prompt to prepend
        
        Returns:
            AIResponse: The generated response
            
        Raises:
            NVIDIAAPIError: If API call fails
        """
        try:
            # Add system prompt if provided
            if system_prompt:
                messages = [
                    {"role": "system", "content": system_prompt}
                ] + messages
            
            # Call NVIDIA API
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                stream=False  # Use non-streaming for simplicity
            )
            
            # Extract response
            content = completion.choices[0].message.content
            tokens = completion.usage.total_tokens
            
            # Track usage
            self.request_count += 1
            self.total_tokens += tokens
            
            response = AIResponse(
                content=content,
                model=model,
                tokens_used=tokens,
                temperature=temperature,
                timestamp=datetime.now()
            )
            
            logger.info(f"NVIDIA API call successful. Tokens: {tokens}, Total: {self.total_tokens}")
            return response
            
        except Exception as e:
            error_msg = f"NVIDIA API Error: {str(e)}"
            logger.error(error_msg)
            raise NVIDIAAPIError(error_msg) from e
    
    def generate_stream(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        top_p: float = 0.7,
        max_tokens: int = 1024,
        system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        """
        Generate streaming response from NVIDIA AI model.
        
        Yields individual tokens as they're generated.
        
        Args:
            model: Model name
            messages: Chat messages
            temperature: Generation temperature
            top_p: Nucleus sampling
            max_tokens: Max response length
            system_prompt: Optional system prompt
        
        Yields:
            str: Individual response tokens
        """
        try:
            # Add system prompt if provided
            if system_prompt:
                messages = [
                    {"role": "system", "content": system_prompt}
                ] + messages
            
            # Call with streaming
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                stream=True
            )
            
            # Stream tokens
            for chunk in completion:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
            
            self.request_count += 1
            
        except Exception as e:
            error_msg = f"NVIDIA Streaming API Error: {str(e)}"
            logger.error(error_msg)
            raise NVIDIAAPIError(error_msg) from e
    
    def explain_phishing(self, email_content: str, subject: str = "") -> AIResponse:
        """Explain phishing indicators in email."""
        system_prompt = """You are a cybersecurity tutor teaching beginners about phishing attacks.
        
Analyze the provided email and explain:
1. Red flags that indicate this might be phishing
2. Suspicious language or urgency tactics
3. What hackers are trying to trick users into doing
4. How to stay safe

Keep explanations simple and beginner-friendly. Use clear language."""

        messages = [
            {
                "role": "user",
                "content": f"Subject: {subject}\n\nEmail:\n{email_content}\n\nWhat phishing indicators do you see?"
            }
        ]
        
        return self.generate(
            model=self.MODEL_MAIN,
            messages=messages,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=1024
        )
    
    def analyze_url_safety(self, url: str, context: str = "") -> AIResponse:
        """Analyze URL safety and explain risks."""
        system_prompt = """You are a cybersecurity expert explaining URL threats to beginners.

Analyze the URL and explain:
1. Whether the domain name looks suspicious
2. Common phishing tricks (typosquatting, fake lookalikes)
3. Red flags in the URL structure
4. What the user should do

Use simple, clear language suitable for someone new to cybersecurity."""

        messages = [
            {
                "role": "user",
                "content": f"Is this URL safe? {url}{chr(10)}{context if context else ''}\n\nWhat risks does it pose?"
            }
        ]
        
        return self.generate(
            model=self.MODEL_FAST,
            messages=messages,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=512
        )
    
    def explain_password_weakness(self, password_analysis: Dict[str, Any]) -> AIResponse:
        """Explain password weaknesses and provide coaching."""
        system_prompt = """You are a friendly cybersecurity coach teaching password security.

Based on the password analysis, explain:
1. Why this password is weak (if it is)
2. How long it would take hackers to crack it
3. Specific improvements they can make
4. Tips for creating strong passwords

Be encouraging and helpful. Use simple language."""

        analysis_text = json.dumps(password_analysis, indent=2)
        messages = [
            {
                "role": "user",
                "content": f"Analyze this password assessment and explain how to improve it:\n\n{analysis_text}"
            }
        ]
        
        return self.generate(
            model=self.MODEL_MAIN,
            messages=messages,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=1024
        )
    
    def explain_file_risk(self, file_analysis: Dict[str, Any]) -> AIResponse:
        """Explain file security risks."""
        system_prompt = """You are a malware expert explaining file risks to beginners.

Analyze the file assessment and explain:
1. What the risk indicators mean
2. Why certain file types are dangerous
3. How malware can hide in files
4. What the user should do

Use simple, non-technical language."""

        analysis_text = json.dumps(file_analysis, indent=2)
        messages = [
            {
                "role": "user",
                "content": f"Explain the risks shown in this file analysis:\n\n{analysis_text}"
            }
        ]
        
        return self.generate(
            model=self.MODEL_FAST,
            messages=messages,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=512
        )
    
    def cybersecurity_qa(self, question: str) -> AIResponse:
        """Answer cybersecurity questions as a tutor."""
        system_prompt = """You are a friendly cybersecurity tutor teaching beginners about online safety.

Answer questions about:
- Common threats (phishing, malware, hacking)
- Password security
- Safe browsing practices
- Data protection
- Social engineering

Rules:
1. Explain concepts in simple, clear language
2. Use real-world examples
3. Provide practical advice
4. Avoid technical jargon
5. Be encouraging and supportive"""

        messages = [
            {"role": "user", "content": question}
        ]
        
        return self.generate(
            model=self.MODEL_MAIN,
            messages=messages,
            system_prompt=system_prompt,
            temperature=0.4,
            max_tokens=1024
        )
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get API usage statistics."""
        return {
            "total_requests": self.request_count,
            "total_tokens_used": self.total_tokens,
            "average_tokens_per_request": (
                self.total_tokens // self.request_count 
                if self.request_count > 0 else 0
            )
        }


# Global client instance (lazy loaded)
_client_instance = None

def get_nvidia_client() -> NVIDIAAIClient:
    """Get or create NVIDIA AI client (singleton)."""
    global _client_instance
    if _client_instance is None:
        _client_instance = NVIDIAAIClient()
    return _client_instance


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 70)
    print("NVIDIA AI Integration - Examples")
    print("=" * 70)
    print()
    
    try:
        # Initialize client
        client = NVIDIAAIClient()
        print("✓ NVIDIA AI client initialized successfully")
        print(f"✓ Using API: https://integrate.api.nvidia.com/v1")
        print()
        
        # Example 1: Phishing Email Analysis
        print("-" * 70)
        print("1. PHISHING EMAIL ANALYSIS")
        print("-" * 70)
        email = """
        Subject: URGENT: Verify your account immediately
        
        Dear Valued Customer,
        
        Your account has been locked due to suspicious activity. You must verify 
        your credentials immediately by clicking the link below.
        
        Click here: http://secure-paypa1.com/verify
        
        If you don't confirm within 24 hours, your account will be permanently closed.
        
        Best regards,
        PayPal Security Team
        """
        
        try:
            response = client.explain_phishing(email, subject="URGENT: Verify your account")
            print(f"\n{response.content}")
            print(f"\n📊 Tokens used: {response.tokens_used}")
        except NVIDIAAPIError as e:
            print(f"Error: {e}")
        print()
        
        # Example 2: URL Safety Analysis
        print("-" * 70)
        print("2. URL SAFETY ANALYSIS")
        print("-" * 70)
        url = "https://amaz0n-account-verify.com/login"
        
        try:
            response = client.analyze_url_safety(url)
            print(f"\n{response.content}")
            print(f"\n📊 Tokens used: {response.tokens_used}")
        except NVIDIAAPIError as e:
            print(f"Error: {e}")
        print()
        
        # Example 3: Password Coaching
        print("-" * 70)
        print("3. PASSWORD SECURITY COACHING")
        print("-" * 70)
        password_analysis = {
            "password": "password123",
            "strength": "Weak",
            "score": 35,
            "entropy": 24.25,
            "issues": [
                "Common dictionary word",
                "Predictable number pattern",
                "No special characters",
                "No uppercase letters"
            ],
            "crack_time": {
                "online": "Instantly",
                "gpu": "Milliseconds"
            }
        }
        
        try:
            response = client.explain_password_weakness(password_analysis)
            print(f"\n{response.content}")
            print(f"\n📊 Tokens used: {response.tokens_used}")
        except NVIDIAAPIError as e:
            print(f"Error: {e}")
        print()
        
        # Example 4: Cybersecurity Q&A
        print("-" * 70)
        print("4. CYBERSECURITY Q&A")
        print("-" * 70)
        question = "What is two-factor authentication and why is it important?"
        
        try:
            response = client.cybersecurity_qa(question)
            print(f"Question: {question}")
            print(f"\n{response.content}")
            print(f"\n📊 Tokens used: {response.tokens_used}")
        except NVIDIAAPIError as e:
            print(f"Error: {e}")
        print()
        
        # Show usage statistics
        print("-" * 70)
        print("USAGE STATISTICS")
        print("-" * 70)
        stats = client.get_usage_stats()
        print(f"Total requests: {stats['total_requests']}")
        print(f"Total tokens used: {stats['total_tokens_used']}")
        print(f"Avg tokens per request: {stats['average_tokens_per_request']}")
        
    except NVIDIAAPIError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
