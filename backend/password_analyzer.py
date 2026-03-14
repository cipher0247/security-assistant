"""
Advanced Password Analyzer Module
Analyzes password strength with multiple metrics and crack time estimation
"""

import math
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class PasswordAnalysis:
    strength: str
    score: int
    entropy: float
    crack_time: Dict[str, str]
    character_variety: Dict[str, bool]
    issues: List[str]
    suggestions: List[str]
    common_pattern: bool


class PasswordAnalyzer:
    """Advanced password analysis with entropy and crack time estimation"""
    
    # Common password patterns
    COMMON_PASSWORDS = {
        'password', 'password123', '123456', 'qwerty', 'abc123',
        'sunshine', 'dragon', 'letmein', 'admin', 'welcome'
    }
    
    # Character sets
    CHARSET_LOWERCASE = set('abcdefghijklmnopqrstuvwxyz')
    CHARSET_UPPERCASE = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    CHARSET_DIGITS = set('0123456789')
    CHARSET_SPECIAL = set('!@#$%^&*()_+-=[]{}|;:,.<>?')
    
    # Crack time by attack mode (guesses per second)
    CRACK_SPEEDS = {
        'online': 1,                    # 1 guess/sec (rate limited)
        'offline_gpu': 1e10,            # 10 billion/sec
        'supercomputer': 1e12           # 1 trillion/sec
    }
    
    def __init__(self, password: str):
        self.password = password
        self.length = len(password)
    
    def analyze(self) -> PasswordAnalysis:
        """Perform complete password analysis"""
        entropy = self.calculate_entropy()
        score = self._calculate_score(entropy)
        strength = self._get_strength_level(score)
        issues = self._detect_issues()
        suggestions = self._get_suggestions(issues)
        crack_time = self._estimate_crack_time(entropy, score)
        character_variety = self._analyze_character_variety()
        common_pattern = self.password.lower() in self.COMMON_PASSWORDS
        
        return PasswordAnalysis(
            strength=strength,
            score=score,
            entropy=entropy,
            crack_time=crack_time,
            character_variety=character_variety,
            issues=issues,
            suggestions=suggestions,
            common_pattern=common_pattern
        )
    
    def calculate_entropy(self) -> float:
        """Calculate Shannon entropy of password"""
        charset_size = self._get_charset_size()
        if charset_size == 0:
            return 0.0
        
        # Entropy = log2(charset_size) * length
        entropy = math.log2(charset_size) * self.length
        return round(entropy, 2)
    
    def _get_charset_size(self) -> int:
        """Calculate effective charset size"""
        charset_size = 0
        
        if any(c in self.CHARSET_LOWERCASE for c in self.password):
            charset_size += 26
        if any(c in self.CHARSET_UPPERCASE for c in self.password):
            charset_size += 26
        if any(c in self.CHARSET_DIGITS for c in self.password):
            charset_size += 10
        if any(c in self.CHARSET_SPECIAL for c in self.password):
            charset_size += 32
        
        return charset_size
    
    def _calculate_score(self, entropy: float) -> int:
        """Calculate password strength score (0-100)"""
        score = 0
        
        # Length score (up to 40 points)
        length_score = min(self.length * 2, 40)
        score += length_score
        
        # Entropy score (up to 40 points)
        entropy_score = min(entropy / 2, 40)
        score += entropy_score
        
        # Character variety score (up to 20 points)
        variety_count = sum([
            any(c in self.CHARSET_LOWERCASE for c in self.password),
            any(c in self.CHARSET_UPPERCASE for c in self.password),
            any(c in self.CHARSET_DIGITS for c in self.password),
            any(c in self.CHARSET_SPECIAL for c in self.password)
        ])
        score += variety_count * 5
        
        # Deductions
        if self.password.lower() in self.COMMON_PASSWORDS:
            score -= 30
        if self._has_sequential_chars():
            score -= 10
        if self._has_repeated_chars():
            score -= 10
        
        return max(0, min(100, int(score)))
    
    def _get_strength_level(self, score: int) -> str:
        """Get strength level from score"""
        if score >= 85:
            return "Very Strong"
        elif score >= 70:
            return "Strong"
        elif score >= 50:
            return "Fair"
        elif score >= 30:
            return "Weak"
        else:
            return "Very Weak"
    
    def _detect_issues(self) -> List[str]:
        """Detect password issues"""
        issues = []
        
        if self.length < 8:
            issues.append("Too short (less than 8 characters)")
        if self.length < 12:
            issues.append("Should be at least 12 characters for better security")
        
        if not any(c in self.CHARSET_UPPERCASE for c in self.password):
            issues.append("No uppercase letters")
        
        if not any(c in self.CHARSET_DIGITS for c in self.password):
            issues.append("No numbers")
        
        if not any(c in self.CHARSET_SPECIAL for c in self.password):
            issues.append("No special characters")
        
        if self.password.lower() in self.COMMON_PASSWORDS:
            issues.append("This is a commonly used password")
        
        if self._has_sequential_chars():
            issues.append("Contains sequential characters (abc, 123)")
        
        if self._has_repeated_chars():
            issues.append("Contains repeated characters (aaa, 111)")
        
        if re.search(r'[a-z]{2,}', self.password) and \
           re.search(r'[A-Z]{2,}', self.password):
            pass  # Good mix
        
        return issues
    
    def _get_suggestions(self, issues: List[str]) -> List[str]:
        """Get improvement suggestions"""
        suggestions = []
        
        if "No uppercase letters" in issues:
            suggestions.append("Add uppercase letters (A-Z)")
        
        if "No numbers" in issues:
            suggestions.append("Add numbers (0-9)")
        
        if "No special characters" in issues:
            suggestions.append("Add special characters (!@#$%)")
        
        if "Too short" in issues:
            suggestions.append("Increase length to at least 12-16 characters")
        
        if "commonly used" in str(issues):
            suggestions.append("Choose a more unique password")
        
        suggestions.append("Use a passphrase with mixed characters")
        suggestions.append("Consider using a password manager")
        
        return suggestions[:3]  # Return top 3
    
    def _estimate_crack_time(self, entropy: float, score: int) -> Dict[str, str]:
        """Estimate crack time for different attack scenarios"""
        crack_times = {}
        
        total_possibilities = 2 ** entropy
        
        for mode, guesses_per_sec in self.CRACK_SPEEDS.items():
            seconds = total_possibilities / guesses_per_sec
            crack_times[mode] = self._format_time(seconds)
        
        return crack_times
    
    @staticmethod
    def _format_time(seconds: float) -> str:
        """Format time in human-readable format"""
        if seconds < 1:
            return "Instant"
        
        units = [
            ("year", 31536000),
            ("month", 2592000),
            ("week", 604800),
            ("day", 86400),
            ("hour", 3600),
            ("minute", 60),
            ("second", 1)
        ]
        
        for unit, divisor in units:
            if seconds >= divisor:
                value = int(seconds / divisor)
                return f"{value} {unit}{'s' if value > 1 else ''}"
        
        return "Instant"
    
    def _has_sequential_chars(self) -> bool:
        """Check for sequential characters like abc or 123"""
        for i in range(len(self.password) - 2):
            if (ord(self.password[i]) + 1 == ord(self.password[i+1]) and
                ord(self.password[i+1]) + 1 == ord(self.password[i+2])):
                return True
        return False
    
    def _has_repeated_chars(self) -> bool:
        """Check for repeated characters like aaa or 111"""
        for i in range(len(self.password) - 2):
            if (self.password[i] == self.password[i+1] ==
                self.password[i+2]):
                return True
        return False
    
    def _analyze_character_variety(self) -> Dict[str, bool]:
        """Analyze character variety in password"""
        return {
            'has_lowercase': any(c in self.CHARSET_LOWERCASE for c in self.password),
            'has_uppercase': any(c in self.CHARSET_UPPERCASE for c in self.password),
            'has_digits': any(c in self.CHARSET_DIGITS for c in self.password),
            'has_special': any(c in self.CHARSET_SPECIAL for c in self.password),
            'length_12_plus': self.length >= 12,
            'length_16_plus': self.length >= 16
        }


# Example usage
if __name__ == "__main__":
    test_passwords = [
        "password123",
        "MyP@ssw0rd!Secure",
        "qwerty",
        "Tr0p1cal@Sunshine#2024"
    ]
    
    for pwd in test_passwords:
        analyzer = PasswordAnalyzer(pwd)
        result = analyzer.analyze()
        
        print(f"\nPassword: {'*' * len(pwd)}")
        print(f"Strength: {result.strength}")
        print(f"Score: {result.score}/100")
        print(f"Entropy: {result.entropy}")
        print(f"Crack Time:")
        print(f"  - Online: {result.crack_time['online']}")
        print(f"  - GPU: {result.crack_time['offline_gpu']}")
        print(f"Issues: {', '.join(result.issues) if result.issues else 'None'}")
        print(f"Common pattern: {result.common_pattern}")
