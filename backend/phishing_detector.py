"""
AI-Powered Phishing Detector
Uses NLP and ML to detect phishing attempts in URLs and emails
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class PhishingDetectionResult:
    is_phishing: bool
    confidence: float  # 0.0 to 1.0
    risk_level: str  # LOW, MEDIUM, HIGH
    features_detected: Dict[str, bool]
    warnings: List[str]
    explanation: str
    recommendations: List[str]


class FeatureExtractor:
    """Extract features for phishing detection"""
    
    # Common phishing keywords
    URGENCY_INDICATORS = {
        'urgent', 'act now', 'immediate', 'confirm', 'verify', 'validate',
        'update', 'expire', 'suspended', 'locked', 'unusual activity'
    }
    
    # Impersonation targets
    IMPERSONATION_TARGETS = {
        'paypal', 'amazon', 'google', 'microsoft', 'apple', 'bank',
        'irs', 'ebay', 'linkedin', 'facebook', 'twitter', 'netflix'
    }
    
    # Suspicious domain patterns
    TYPOSQUAT_PATTERNS = [
        r'paypa[l1]',
        r'amaz[o0]n',
        r'microft|microsft',
        r'gogl|googl',
        r'appl'
    ]
    
    @staticmethod
    def extract_url_features(url: str) -> Dict[str, bool]:
        """Extract features from URL"""
        features = {
            'has_shorter_url': FeatureExtractor._check_shortened_url(url),
            'uses_ip': FeatureExtractor._has_ip_address(url),
            'suspicious_domain': FeatureExtractor._check_suspicious_domain(url),
            'multiple_subdomains': FeatureExtractor._has_many_subdomains(url),
            'no_https': not url.startswith('https'),
            'long_url': len(url) > 75,
            'redirect_parameter': FeatureExtractor._has_redirect_param(url),
        }
        return features
    
    @staticmethod
    def extract_email_features(subject: str, body: str) -> Dict[str, bool]:
        """Extract features from email"""
        combined = (subject + ' ' + body).lower()
        
        features = {
            'urgency_language': any(word in combined for word in FeatureExtractor.URGENCY_INDICATORS),
            'impersonation_attempt': any(target in combined for target in FeatureExtractor.IMPERSONATION_TARGETS),
            'login_request': any(word in combined for word in ['login', 'password', 'sign in', 'verify identity']),
            'unusual_sender': FeatureExtractor._check_sender_anomaly(subject, body),
            'poor_grammar': FeatureExtractor._detect_poor_grammar(body),
            'suspicious_links': FeatureExtractor._has_suspicious_links(body),
            'generic_greeting': FeatureExtractor._has_generic_greeting(body),
            'excessive_capitalization': combined.count('!') > 5,
        }
        return features
    
    @staticmethod
    def _check_shortened_url(url: str) -> bool:
        """Check if URL is shortened"""
        shorteners = ['bit.ly', 'tinyurl', 'short.link', 'ow.ly', 'goo.gl']
        return any(short in url for short in shorteners)
    
    @staticmethod
    def _has_ip_address(url: str) -> bool:
        """Check if URL uses IP address"""
        ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'
        return bool(re.search(ip_pattern, url))
    
    @staticmethod
    def _check_suspicious_domain(url: str) -> bool:
        """Check for suspicious domain patterns"""
        for pattern in FeatureExtractor.TYPOSQUAT_PATTERNS:
            if re.search(pattern, url):
                return True
        return False
    
    @staticmethod
    def _has_many_subdomains(url: str) -> bool:
        """Check for many subdomains"""
        subdomain_count = url.count('.')
        return subdomain_count > 3
    
    @staticmethod
    def _has_redirect_param(url: str) -> bool:
        """Check for redirect parameters"""
        redirect_params = ['redirect=', 'url=', 'return=', 'target=', 'goto=']
        return any(param in url for param in redirect_params)
    
    @staticmethod
    def _check_sender_anomaly(subject: str, body: str) -> bool:
        """Check for sender anomalies"""
        # Generic text that might indicate spoofed sender
        anomalies = ['dear customer', 'valued customer', 'dear user']
        combined = (subject + ' ' + body).lower()
        return any(anomaly in combined for anomaly in anomalies)
    
    @staticmethod
    def _detect_poor_grammar(text: str) -> bool:
        """Detect poor grammar/spelling"""
        # Check for common spelling/grammar errors
        errors = ['teh', 'recieve', 'occured', 'bussiness', 'adress']
        text_lower = text.lower()
        return sum(1 for error in errors if error in text_lower) >= 2
    
    @staticmethod
    def _has_suspicious_links(text: str) -> bool:
        """Check for suspicious links"""
        # Find URLs in text
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, text)
        
        # Check if any URLs look suspicious
        for url in urls:
            if 'bit.ly' in url or 'short' in url:
                return True
            if '@' in url:  # @ in URL is very suspicious
                return True
        
        return False
    
    @staticmethod
    def _has_generic_greeting(text: str) -> bool:
        """Check for generic greetings"""
        generic_greetings = ['Hello customer', 'Dear User', 'Dear Customer']
        return any(greeting in text for greeting in generic_greetings)


class PhishingDetector:
    """ML-based phishing detection engine"""
    
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        # In production, load trained ML model here
        self.model = None
    
    def detect_url_phishing(self, url: str) -> PhishingDetectionResult:
        """Detect phishing in URL"""
        features = self.feature_extractor.extract_url_features(url)
        
        # Calculate risk score based on features
        risk_score = self._calculate_url_risk_score(features)
        confidence = min(risk_score / 100.0, 1.0)
        is_phishing = confidence >= 0.6
        risk_level = self._get_risk_level(confidence)
        
        warnings = self._generate_url_warnings(features)
        explanation = self._generate_explanation(is_phishing, confidence, warnings)
        recommendations = self._get_recommendations(is_phishing)
        
        return PhishingDetectionResult(
            is_phishing=is_phishing,
            confidence=confidence,
            risk_level=risk_level,
            features_detected=features,
            warnings=warnings,
            explanation=explanation,
            recommendations=recommendations
        )
    
    def detect_email_phishing(self, subject: str, body: str, 
                            sender: str = "") -> PhishingDetectionResult:
        """Detect phishing in email"""
        features = self.feature_extractor.extract_email_features(subject, body)
        
        # Add sender check
        if sender:
            features['suspicious_sender'] = self._check_sender_domain(sender)
        
        # Calculate risk score
        risk_score = self._calculate_email_risk_score(features)
        confidence = min(risk_score / 100.0, 1.0)
        is_phishing = confidence >= 0.6
        risk_level = self._get_risk_level(confidence)
        
        warnings = self._generate_email_warnings(features)
        explanation = self._generate_explanation(is_phishing, confidence, warnings)
        recommendations = self._get_recommendations(is_phishing, is_email=True)
        
        return PhishingDetectionResult(
            is_phishing=is_phishing,
            confidence=confidence,
            risk_level=risk_level,
            features_detected=features,
            warnings=warnings,
            explanation=explanation,
            recommendations=recommendations
        )
    
    def _calculate_url_risk_score(self, features: Dict[str, bool]) -> float:
        """Calculate risk score for URL"""
        score = 0
        weights = {
            'has_shorter_url': 15,
            'uses_ip': 25,
            'suspicious_domain': 30,
            'multiple_subdomains': 10,
            'no_https': 20,
            'long_url': 5,
            'redirect_parameter': 20,
        }
        
        for feature, weight in weights.items():
            if features.get(feature, False):
                score += weight
        
        return score
    
    def _calculate_email_risk_score(self, features: Dict[str, bool]) -> float:
        """Calculate risk score for email"""
        score = 0
        weights = {
            'urgency_language': 20,
            'impersonation_attempt': 35,
            'login_request': 25,
            'unusual_sender': 20,
            'poor_grammar': 15,
            'suspicious_links': 30,
            'generic_greeting': 10,
            'excessive_capitalization': 5,
            'suspicious_sender': 30,
        }
        
        for feature, weight in weights.items():
            if features.get(feature, False):
                score += weight
        
        return score
    
    def _check_sender_domain(self, sender: str) -> bool:
        """Check if sender domain looks suspicious"""
        # Extract domain from email
        if '@' not in sender:
            return True
        
        domain = sender.split('@')[1].lower()
        
        # Check for free email providers (sometimes suspicious)
        free_providers = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
        
        # Check for spoofed domains
        common_targets = {'paypal', 'amazon', 'google', 'microsoft', 'apple', 'bank'}
        for target in common_targets:
            if target in domain:
                # If it's not the official domain, it's suspicious
                if domain != f"{target}.com":
                    return True
        
        return False
    
    def _get_risk_level(self, confidence: float) -> str:
        """Get risk level from confidence"""
        if confidence >= 0.8:
            return "HIGH"
        elif confidence >= 0.6:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_url_warnings(self, features: Dict[str, bool]) -> List[str]:
        """Generate warnings for URL"""
        warnings = []
        
        if features.get('has_shorter_url'):
            warnings.append("URL is shortened - actual destination unclear")
        if features.get('uses_ip'):
            warnings.append("URL uses IP address instead of domain")
        if features.get('suspicious_domain'):
            warnings.append("Domain appears to be a typosquat/lookalike")
        if features.get('no_https'):
            warnings.append("No HTTPS encryption - data transmitted in plain text")
        if features.get('redirect_parameter'):
            warnings.append("URL contains redirect to another site")
        
        return warnings
    
    def _generate_email_warnings(self, features: Dict[str, bool]) -> List[str]:
        """Generate warnings for email"""
        warnings = []
        
        if features.get('urgency_language'):
            warnings.append("Email uses urgent/threatening language")
        if features.get('impersonation_attempt'):
            warnings.append("Email impersonates known company")
        if features.get('login_request'):
            warnings.append("Email requests login credentials")
        if features.get('poor_grammar'):
            warnings.append("Email contains spelling/grammar errors")
        if features.get('suspicious_links'):
            warnings.append("Email contains shortened or suspicious links")
        if features.get('generic_greeting'):
            warnings.append("Email uses generic greeting (not personalized)")
        if features.get('suspicious_sender'):
            warnings.append("Sender domain appears spoofed")
        
        return warnings
    
    def _generate_explanation(self, is_phishing: bool, 
                            confidence: float, warnings: List[str]) -> str:
        """Generate human-readable explanation"""
        if is_phishing:
            explanation = f"This appears to be a PHISHING attempt (confidence: {confidence*100:.0f}%).\n\n"
            explanation += "RED FLAGS:\n"
            for i, warning in enumerate(warnings, 1):
                explanation += f"{i}. {warning}\n"
            explanation += "\nDO NOT:\n"
            explanation += "- Click on links\n"
            explanation += "- Enter personal information\n"
            explanation += "- Download attachments\n"
            explanation += "- Call any provided phone numbers\n"
        else:
            if confidence > 0.3:
                explanation = f"This message has some suspicious characteristics (risk: {confidence*100:.0f}%), but may not be phishing.\n\n"
            else:
                explanation = f"This appears to be LEGITIMATE. It has low phishing indicators."
            
            if warnings:
                explanation += "\nCautionary flags:\n"
                for flag in warnings:
                    explanation += f"- {flag}\n"
        
        return explanation
    
    def _get_recommendations(self, is_phishing: bool, is_email: bool = False) -> List[str]:
        """Get security recommendations"""
        recommendations = []
        
        if is_phishing:
            if is_email:
                recommendations.append("Report to your email provider as phishing")
                recommendations.append("Delete the email")
                recommendations.append("Block the sender")
            else:
                recommendations.append("Do not visit this website")
                recommendations.append("Report URL to Google Safe Browsing")
        else:
            recommendations.append("Use caution and verify sender through other means")
            recommendations.append("Watch for requests for sensitive information")
        
        recommendations.append("Never click links from suspicious messages")
        recommendations.append("Visit websites by typing URL directly in address bar")
        
        return recommendations


# Example usage
if __name__ == "__main__":
    detector = PhishingDetector()
    
    # Test URL
    print("=== URL Phishing Test ===")
    url_result = detector.detect_url_phishing("http://192.168.1.1/verify-account/paypal")
    print(f"Is Phishing: {url_result.is_phishing}")
    print(f"Confidence: {url_result.confidence:.2%}")
    print(f"Warnings: {url_result.warnings}")
    print(f"Explanation: {url_result.explanation}\n")
    
    # Test Email
    print("=== Email Phishing Test ===")
    subject = "URGENT: Verify Your PayPal Account"
    body = """Dear Customer,

Your PayPal account has unusual activity. Click here to confirm your identity immediately!

http://bit.ly/verify-paypal

Do not ignore this message!
"""
    
    email_result = detector.detect_email_phishing(subject, body, "service@paypa1.com")
    print(f"Is Phishing: {email_result.is_phishing}")
    print(f"Confidence: {email_result.confidence:.2%}")
    print(f"Warnings: {email_result.warnings}")
    print(f"Explanation: {email_result.explanation}")
