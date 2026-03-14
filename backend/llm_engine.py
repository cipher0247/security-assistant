"""
LLM Integration Engine
=======================
Integrates OpenAI GPT-4 and Anthropic Claude for threat explanations
and intelligent security guidance.

Features:
- Multi-provider support (OpenAI, Claude, fallback)
- Prompt engineering for security context
- Response caching for performance
- Error handling with graceful fallbacks
- Token counting and cost tracking
"""

import os
import json
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum
from abc import ABC, abstractmethod


class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    CLAUDE = "claude"
    FALLBACK = "fallback"


@dataclass
class LLMResponse:
    """LLM Response wrapper"""
    content: str
    provider: str
    tokens_used: int
    confidence: float = 0.95
    cached: bool = False
    error: Optional[str] = None


class LLMBase(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.tokens_used = 0
        self.cache = {}
    
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 500) -> LLMResponse:
        """Generate response from LLM"""
        pass
    
    def _get_cached(self, prompt: str) -> Optional[str]:
        """Check if response is cached"""
        return self.cache.get(hash(prompt))
    
    def _cache_response(self, prompt: str, response: str):
        """Cache response for future use"""
        self.cache[hash(prompt)] = response


class OpenAIProvider(LLMBase):
    """OpenAI GPT-4 Integration"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.model = "gpt-4"
        self.base_url = "https://api.openai.com/v1"
        
    def generate(self, prompt: str, max_tokens: int = 500) -> LLMResponse:
        """Generate response using OpenAI API"""
        
        # Check cache
        cached = self._get_cached(prompt)
        if cached:
            return LLMResponse(
                content=cached,
                provider="openai",
                tokens_used=0,
                cached=True
            )
        
        try:
            # Import here to handle missing dependency
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert cybersecurity advisor. 
                        Explain security threats and best practices in simple, beginner-friendly language.
                        Be concise but thorough. Always include actionable recommendations."""
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7,
            )
            
            content = response['choices'][0]['message']['content']
            tokens = response['usage']['total_tokens']
            
            # Cache response
            self._cache_response(prompt, content)
            
            return LLMResponse(
                content=content,
                provider="openai",
                tokens_used=tokens,
                confidence=0.95
            )
            
        except Exception as e:
            return LLMResponse(
                content="",
                provider="openai",
                tokens_used=0,
                error=str(e)
            )


class ClaudeProvider(LLMBase):
    """Anthropic Claude Integration"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.model = "claude-3-sonnet-20240229"  # Latest Claude model
        self.base_url = "https://api.anthropic.com/v1"
        
    def generate(self, prompt: str, max_tokens: int = 500) -> LLMResponse:
        """Generate response using Claude API"""
        
        # Check cache
        cached = self._get_cached(prompt)
        if cached:
            return LLMResponse(
                content=cached,
                provider="claude",
                tokens_used=0,
                cached=True
            )
        
        try:
            # Import here to handle missing dependency
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            message = client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system="""You are an expert cybersecurity advisor. 
                Explain security threats and best practices in simple, beginner-friendly language.
                Be concise but thorough. Always include actionable recommendations.""",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = message.content[0].text
            tokens = message.usage.input_tokens + message.usage.output_tokens
            
            # Cache response
            self._cache_response(prompt, content)
            
            return LLMResponse(
                content=content,
                provider="claude",
                tokens_used=tokens,
                confidence=0.96
            )
            
        except Exception as e:
            return LLMResponse(
                content="",
                provider="claude",
                tokens_used=0,
                error=str(e)
            )


class FallbackProvider(LLMBase):
    """Fallback responses when LLM APIs unavailable"""
    
    def __init__(self, api_key: str = ""):
        super().__init__(api_key)
        self.knowledge_base = self._load_knowledge_base()
        
    def _load_knowledge_base(self) -> Dict[str, str]:
        """Load pre-written security guidance"""
        return {
            "phishing": """Phishing is a social engineering attack where attackers impersonate legitimate 
            organizations to trick you into revealing sensitive information like passwords or credit cards.

            Red flags:
            - Urgent language ("Act now!" "Verify immediately!")
            - Generic greetings ("Dear Customer")
            - Requests for personal information
            - Suspicious links or attachments
            - Spelling/grammar errors

            Protection:
            1. Verify sender email address carefully
            2. Never click links in emails - go to official website directly
            3. Use multi-factor authentication
            4. Report suspicious emails
            5. Keep software updated""",
            
            "password": """A strong password is your first line of defense against account takeover.

            Strong password requirements:
            - At least 16 characters (longer is better)
            - Mix of uppercase, lowercase, numbers, symbols
            - No dictionary words or personal information
            - Unique for each account
            - Changed periodically

            Better approach: Use a password manager
            - Bitwarden (free, open-source)
            - 1Password (paid but reliable)
            - KeePass (offline storage)

            Enable two-factor authentication on important accounts.""",
            
            "malware": """Malware (malicious software) includes viruses, worms, trojans that damage your system.

            Common types:
            - Ransomware: Encrypts files and demands payment
            - Spyware: Steals personal information
            - Worms: Self-replicating network attacks
            - Trojans: Disguise as legitimate software

            Protection:
            1. Use reputable antivirus software (Windows Defender, Bitdefender)
            2. Don't download from untrusted sources
            3. Keep OS and software updated
            4. Use firewall
            5. Regular backups of important files
            6. Be cautious of email attachments""",
            
            "2fa": """Two-factor authentication (2FA) requires two forms of ID to access accounts.

            Types of 2FA:
            - SMS codes (text message to phone)
            - Authenticator apps (Google Authenticator, Authy)
            - Hardware keys (YubiKey, more secure)
            - Biometric (fingerprint, face recognition)

            Why it matters:
            - Even if password is stolen, account stays protected
            - Significantly reduces account takeover risk
            - Critical for email, banking, work accounts

            Setup 2FA on: Email, Banking, Social Media, Work accounts""",
            
            "vpn": """A Virtual Private Network (VPN) encrypts your internet traffic and hides your IP address.

            Why use VPN:
            - Protects data on public WiFi (coffee shops, airports)
            - Prevents ISP from tracking browsing
            - Masks your IP address
            - Encrypts sensitive transactions

            Choosing a VPN:
            - Reputable providers (NordVPN, ExpressVPN, ProtonVPN)
            - No-log policy (doesn't store activity)
            - Strong encryption (256-bit)
            - Fast speeds
            - Multi-device support

            Note: VPN doesn't make you anonymous online, use for privacy.""",
        }
    
    def generate(self, prompt: str, max_tokens: int = 500) -> LLMResponse:
        """Generate response from knowledge base"""
        
        # Simple keyword matching
        prompt_lower = prompt.lower()
        
        for keyword, response in self.knowledge_base.items():
            if keyword in prompt_lower:
                return LLMResponse(
                    content=response,
                    provider="fallback",
                    tokens_used=len(response.split()),
                    confidence=0.70
                )
        
        # Generic fallback
        generic_response = """Thank you for your security question. While I don't have a specific response 
        in my knowledge base, here's general guidance:

        1. Be cautious of unknown sources and unexpected requests
        2. Always verify sender identity before sharing information
        3. Use strong, unique passwords for each account
        4. Enable two-factor authentication
        5. Keep software and operating system updated
        6. Use reputable security software
        7. Regular backups protect against ransomware

        For detailed information, consult official resources or contact your IT department."""
        
        return LLMResponse(
            content=generic_response,
            provider="fallback",
            tokens_used=len(generic_response.split()),
            confidence=0.60
        )


class LLMEngine:
    """Main LLM Engine managing provider selection and fallback"""
    
    def __init__(
        self,
        openai_key: Optional[str] = None,
        claude_key: Optional[str] = None,
        prefer_provider: str = "openai"
    ):
        self.openai_key = openai_key or os.getenv("OPENAI_API_KEY")
        self.claude_key = claude_key or os.getenv("ANTHROPIC_API_KEY")
        self.prefer_provider = prefer_provider
        
        self.providers = {
            LLMProvider.OPENAI: OpenAIProvider(self.openai_key) if self.openai_key else None,
            LLMProvider.CLAUDE: ClaudeProvider(self.claude_key) if self.claude_key else None,
            LLMProvider.FALLBACK: FallbackProvider(),
        }
        
        self.total_tokens = 0
        self.total_cost = 0.0
        
    def explain_threat(self, threat_type: str, details: str) -> LLMResponse:
        """Explain a threat with context"""
        prompt = f"""Explain this cybersecurity threat in simple, beginner-friendly language:

        Threat Type: {threat_type}
        Details: {details}

        Please provide:
        1. What is this threat?
        2. How does it work?
        3. Real-world example
        4. How to protect yourself
        5. What to do if you're affected"""
        
        return self.generate(prompt)
    
    def analyze_security_question(self, question: str) -> LLMResponse:
        """Answer a security-related question"""
        prompt = f"""As a cybersecurity expert, answer this question clearly and concisely:

        {question}

        Provide practical, actionable advice suitable for someone new to cybersecurity."""
        
        return self.generate(prompt)
    
    def summarize_analysis(self, analysis_type: str, results: Dict[str, Any]) -> LLMResponse:
        """Summarize security analysis results"""
        results_str = json.dumps(results, indent=2)
        prompt = f"""Summarize these {analysis_type} security analysis results for a non-technical user:

        {results_str}

        Explain what the results mean and what the user should do about any issues found."""
        
        return self.generate(prompt)
    
    def generate(self, prompt: str, max_tokens: int = 500) -> LLMResponse:
        """Generate response using preferred provider with fallback"""
        
        # Try preferred provider first
        prefer_enum = LLMProvider[self.prefer_provider.upper()]
        
        # Try preferred provider
        if self.providers[prefer_enum]:
            response = self.providers[prefer_enum].generate(prompt, max_tokens)
            if not response.error:
                self._track_usage(response)
                return response
        
        # Try other providers
        for provider, instance in self.providers.items():
            if provider == LLMProvider.FALLBACK or provider == prefer_enum:
                continue
            if instance:
                response = instance.generate(prompt, max_tokens)
                if not response.error:
                    self._track_usage(response)
                    return response
        
        # Use fallback
        response = self.providers[LLMProvider.FALLBACK].generate(prompt, max_tokens)
        self._track_usage(response)
        return response
    
    def _track_usage(self, response: LLMResponse):
        """Track token usage and approximate costs"""
        self.total_tokens += response.tokens_used
        
        # Approximate costs per 1K tokens
        costs = {
            "openai": 0.015,  # GPT-4
            "claude": 0.008,  # Claude
            "fallback": 0.0,  # Free
        }
        
        cost_per_1k = costs.get(response.provider, 0.0)
        self.total_cost += (response.tokens_used / 1000) * cost_per_1k
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get token and cost tracking statistics"""
        return {
            "total_tokens": self.total_tokens,
            "total_cost": f"${self.total_cost:.4f}",
            "active_providers": [p.name for p in self.providers if self.providers[p]]
        }


# Example usage
if __name__ == "__main__":
    # Initialize engine
    engine = LLMEngine(prefer_provider="fallback")  # Use fallback for demo
    
    # Test threat explanation
    print("=" * 60)
    print("THREAT EXPLANATION")
    print("=" * 60)
    response = engine.explain_threat(
        threat_type="Phishing",
        details="User received email claiming to be from PayPal asking to verify account"
    )
    print(f"Provider: {response.provider}")
    print(f"Confidence: {response.confidence:.0%}")
    print(f"Response:\n{response.content}")
    print()
    
    # Test security question
    print("=" * 60)
    print("SECURITY QUESTION")
    print("=" * 60)
    response = engine.analyze_security_question(
        "What makes a password strong?"
    )
    print(f"Provider: {response.provider}")
    print(f"Response:\n{response.content}")
    print()
    
    # Test analysis summary
    print("=" * 60)
    print("ANALYSIS SUMMARY")
    print("=" * 60)
    analysis_results = {
        "url": "https://suspicious-paypal.com",
        "risk_level": "HIGH_RISK",
        "threats": ["No HTTPS", "Typosquatted domain", "IP address in URL"],
        "score": 25
    }
    response = engine.summarize_analysis("URL", analysis_results)
    print(f"Provider: {response.provider}")
    print(f"Response:\n{response.content}")
    print()
    
    # Show usage stats
    print("=" * 60)
    print("USAGE STATISTICS")
    print("=" * 60)
    stats = engine.get_usage_stats()
    print(json.dumps(stats, indent=2))
