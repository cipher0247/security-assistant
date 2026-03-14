"""
Advanced URL Safety Analyzer
Analyzes URLs for security threats and provides risk assessment
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs
import socket
import ssl
from datetime import datetime

@dataclass
class URLAnalysisResult:
    url: str
    risk_level: str  # SAFE, SUSPICIOUS, HIGH_RISK
    score: float  # 0-100 (higher = more dangerous)
    domain_info: Dict
    security_checks: Dict
    threats: List[str]
    warnings: List[str]
    ai_explanation: str
    recommendations: List[str]


class URLSafetyAnalyzer:
    """Comprehensive URL safety analysis"""
    
    # Suspicious keywords and patterns
    PHISHING_KEYWORDS = {
        'verify', 'confirm', 'update', 'validate', 'authenticate',
        'login', 'sign in', 'account', 'urgent', 'act now', 'immediate',
        'click here', 'expire', 'expire soon', 'suspended', 'locked',
        'unusual activity', 'confirm identity', 'banking', 'payment'
    }
    
    # Known malicious domain patterns
    SUSPICIOUS_PATTERNS = [
        r'(?:https?://)?(?:www\.)?.*-(?:verification|secure|confirm|update).*\.(?:tk|ml|ga|cf)',
        r'(?:https?://)?(?:www\.)?.*paypa[l1].*\.(?:com|net|co|tk)',  # PayPal lookalikes
        r'(?:https?://)?(?:www\.)?.*amaz[o0]n.*\.(?:com|net|tk)',     # Amazon lookalikes
        r'(?:https?://)?(?:\d+\.){3}\d+(?::\d+)?(?:/.*)?',             # IP-based URLs
    ]
    
    # Dangerous file extensions
    DANGEROUS_EXTENSIONS = {
        '.exe', '.bat', '.cmd', '.scr', '.vbs', '.js', '.jar', '.zip',
        '.rar', '.7z', '.apk', '.dmg', '.iso'
    }
    
    def __init__(self, url: str):
        self.url = url
        self.parsed_url = urlparse(url if url.startswith('http') else f'http://{url}')
        self.domain = self._extract_domain()
    
    def analyze(self) -> URLAnalysisResult:
        """Perform complete URL analysis"""
        domain_info = self._get_domain_info()
        security_checks = self._perform_security_checks()
        threats = self._detect_threats()
        warnings = self._get_warnings()
        score = self._calculate_risk_score(threats, warnings, security_checks)
        risk_level = self._get_risk_level(score)
        explanation = self._generate_explanation(threats, warnings)
        recommendations = self._get_recommendations(threats)
        
        return URLAnalysisResult(
            url=self.url,
            risk_level=risk_level,
            score=score,
            domain_info=domain_info,
            security_checks=security_checks,
            threats=threats,
            warnings=warnings,
            ai_explanation=explanation,
            recommendations=recommendations
        )
    
    def _extract_domain(self) -> str:
        """Extract domain from URL"""
        domain = self.parsed_url.netloc
        # Remove port
        if ':' in domain:
            domain = domain.split(':')[0]
        # Remove www
        domain = domain.replace('www.', '')
        return domain
    
    def _get_domain_info(self) -> Dict:
        """Get domain information"""
        info = {
            'domain': self.domain,
            'protocol': self.parsed_url.scheme or 'http',
            'is_https': self.parsed_url.scheme == 'https',
            'port': self.parsed_url.port or (443 if self.parsed_url.scheme == 'https' else 80),
            'path': self.parsed_url.path or '/',
            'has_query': bool(self.parsed_url.query),
            'is_ip_based': self._is_ip_address(self.domain),
        }
        
        # SSL/TLS info
        if self.parsed_url.scheme == 'https':
            info['ssl_valid'], info['ssl_info'] = self._check_ssl_certificate()
        
        return info
    
    def _is_ip_address(self, domain: str) -> bool:
        """Check if domain is IP address"""
        try:
            socket.inet_aton(domain)
            return True
        except socket.error:
            return False
    
    def _check_ssl_certificate(self) -> Tuple[bool, Dict]:
        """Check SSL certificate validity"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    return True, {
                        'subject': cert.get('subject'),
                        'issuer': cert.get('issuer'),
                        'version': cert.get('version')
                    }
        except Exception as e:
            return False, {'error': str(e)}
    
    def _perform_security_checks(self) -> Dict:
        """Perform security checks"""
        checks = {
            'https_enabled': self.parsed_url.scheme == 'https',
            'suspicious_port': self._check_suspicious_port(),
            'ip_based_url': self._is_ip_address(self.domain),
            'url_shortener': self._detect_url_shortener(),
            'suspicious_structure': self._check_suspicious_structure(),
            'has_credentials': '@' in self.parsed_url.netloc,
            'has_parameters': bool(self.parsed_url.query),
        }
        
        return checks
    
    def _check_suspicious_port(self) -> bool:
        """Check for suspicious or unusual ports"""
        dangerous_ports = {21, 23, 25, 135, 139, 445, 3389, 5900}
        port = self.parsed_url.port
        return port in dangerous_ports if port else False
    
    def _detect_url_shortener(self) -> bool:
        """Detect shortened URLs (bit.ly, tinyurl, etc.)"""
        shorteners = {'bit.ly', 'tinyurl.com', 'short.link', 'ow.ly', 'goo.gl'}
        return self.domain in shorteners
    
    def _check_suspicious_structure(self) -> bool:
        """Check for suspicious URL structure"""
        # Multiple subdomains might be suspicious
        dot_count = self.domain.count('.')
        if dot_count > 3:
            return True
        
        # Very long domains
        if len(self.domain) > 63:
            return True
        
        return False
    
    def _detect_threats(self) -> List[str]:
        """Detect security threats"""
        threats = []
        
        # Check SSL
        if self.parsed_url.scheme == 'https':
            valid, _ = self._check_ssl_certificate()
            if not valid:
                threats.append('Invalid or missing SSL certificate')
        else:
            threats.append('No HTTPS encryption - data transmitted in plain text')
        
        # Check for IP-based URLs
        if self._is_ip_address(self.domain):
            threats.append('URL uses IP address instead of domain name')
        
        # Check for credentials in URL
        if '@' in self.parsed_url.netloc:
            threats.append('Credentials embedded in URL (serious security risk)')
        
        # Check for redirects
        if self._has_redirect_parameters():
            threats.append('URL contains redirect parameters')
        
        # Check suspicious patterns
        for pattern in self.SUSPICIOUS_PATTERNS:
            if re.search(pattern, self.url, re.IGNORECASE):
                threats.append('URL matches known suspicious pattern')
                break
        
        # Check for dangerous extensions
        path = self.parsed_url.path.lower()
        for ext in self.DANGEROUS_EXTENSIONS:
            if ext in path:
                threats.append(f'URL references dangerous file type: {ext}')
        
        return threats
    
    def _has_redirect_parameters(self) -> bool:
        """Check for redirect parameters"""
        redirect_params = {'redirect', 'url', 'return', 'target', 'goto'}
        if self.parsed_url.query:
            params = parse_qs(self.parsed_url.query)
            return bool(redirect_params & set(params.keys()))
        return False
    
    def _get_warnings(self) -> List[str]:
        """Get non-critical warnings"""
        warnings = []
        
        # URL shortener
        if self._detect_url_shortener():
            warnings.append('URL is shortened - final destination unclear')
        
        # Weird structure
        if self._check_suspicious_structure():
            warnings.append('URL has unusual structure with many subdomains')
        
        # Suspicious port
        if self._check_suspicious_port():
            warnings.append('URL uses suspicious port number')
        
        return warnings
    
    def _calculate_risk_score(self, threats: List[str], 
                            warnings: List[str], 
                            checks: Dict) -> float:
        """Calculate overall risk score (0-100)"""
        score = 0
        
        # Start with 10 (baseline)
        score = 10
        
        # Add points for each threat (25 points each)
        score += len(threats) * 25
        
        # Add points for warnings (10 points each)
        score += len(warnings) * 10
        
        # Security checks bonuses/penalties
        if not checks.get('https_enabled'):
            score += 20
        
        if checks.get('url_shortener'):
            score += 15
        
        if checks.get('has_credentials'):
            score += 30
        
        if checks.get('ip_based_url'):
            score += 25
        
        # Bonus for https + valid cert
        if checks.get('https_enabled'):
            score -= 10
        
        return min(100, max(0, score))
    
    def _get_risk_level(self, score: float) -> str:
        """Get risk level from score"""
        if score >= 70:
            return "HIGH_RISK"
        elif score >= 40:
            return "SUSPICIOUS"
        else:
            return "SAFE"
    
    def _generate_explanation(self, threats: List[str], warnings: List[str]) -> str:
        """Generate AI explanation"""
        if not threats and not warnings:
            return "This website appears to be secure. It uses HTTPS encryption and standard security practices."
        
        explanation = f"Found {len(threats)} security threat(s) and {len(warnings)} warning(s):\n"
        
        if threats:
            explanation += "\nTHREATS:\n"
            for threat in threats:
                explanation += f"• {threat}\n"
        
        if warnings:
            explanation += "\nWARNINGS:\n"
            for warning in warnings:
                explanation += f"• {warning}\n"
        
        return explanation.strip()
    
    def _get_recommendations(self, threats: List[str]) -> List[str]:
        """Get security recommendations"""
        recommendations = []
        
        if not threats:
            recommendations.append("Website appears safe to visit")
        else:
            if 'HTTPS' in str(threats):
                recommendations.append("Avoid entering sensitive information on this site")
            if 'IP address' in str(threats):
                recommendations.append("Use caution with IP-based URLs")
            if 'credentials' in str(threats).lower():
                recommendations.append("DO NOT enter personal information")
            if 'redirect' in str(threats).lower():
                recommendations.append("Check where links lead before clicking")
        
        recommendations.append("Verify the URL in the address bar matches what you expected")
        
        return recommendations


# Example usage
if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "http://example.com:8080",
        "https://secure-verify-account.tk/confirm",
        "http://192.168.1.1/admin",
    ]
    
    for url in test_urls:
        analyzer = URLSafetyAnalyzer(url)
        result = analyzer.analyze()
        
        print(f"\nURL: {url}")
        print(f"Risk Level: {result.risk_level}")
        print(f"Risk Score: {result.score}/100")
        print(f"HTTPS: {result.domain_info['is_https']}")
        print(f"Threats: {result.threats}")
        print(f"Explanation: {result.ai_explanation[:100]}...")
