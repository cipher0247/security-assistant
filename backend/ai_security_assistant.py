"""
AI Security Assistant - LLM-Powered Explanations
Provides conversational security guidance and threat explanations
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class AssistantResponse:
    message: str
    confidence: float
    category: str  # threat_explanation, security_question, threat_detection
    references: List[str]
    follow_up_questions: List[str]


class SecurityAssistant:
    """AI-powered security assistant for user guidance"""
    
    # Knowledge base for common threats
    THREAT_KB = {
        'phishing': {
            'definition': 'Phishing is a cyberattack technique where attackers send deceptive messages (emails, texts, links) pretending to be legitimate organizations to trick you into revealing sensitive information.',
            'indicators': [
                'Urgent requests for personal information',
                'Suspicious sender domains or email addresses', 
                'Links that don\'t match the company name',
                'Poor grammar and spelling',
                'Requests to confirm password or account details'
            ],
            'prevention': [
                'Don\'t click links in suspicious emails - go to the website directly',
                'Hover over links to see the real URL before clicking',
                'Verify sender through official contact information',
                'Never share passwords via email',
                'Use multi-factor authentication'
            ]
        },
        'malware': {
            'definition': 'Malware is malicious software designed to damage, disrupt, or gain unauthorized access to computer systems.',
            'types': ['Virus', 'Worm', 'Trojan', 'Ransomware', 'Spyware', 'Rootkit'],
            'indicators': [
                'Slow computer performance',
                'Unexpected pop-ups',
                'Unauthorized account access',
                'Modified files or settings',
                'Unexpected network activity'
            ],
            'prevention': [
                'Keep software and OS updated',
                'Use antivirus and anti-malware software',
                'Don\'t download from untrusted sources',
                'Be cautious with email attachments',
                'Use strong passwords'
            ]
        },
        'social_engineering': {
            'definition': 'Social engineering uses psychological manipulation to trick people into divulging confidential information or performing security-compromising actions.',
            'tactics': [
                'Pretexting: Creating fake scenarios',
                'Baiting: Offering something enticing',
                'Tailgating: Following authorized person',
                'Phishing: Deceptive messages',
                'Quid pro quo: Trading for information'
            ],
            'prevention': [
                'Verify identities before sharing information',
                'Be skeptical of unexpected requests',
                'Don\'t share passwords with anyone',
                'Report suspicious interactions',
                'Get security training'
            ]
        },
        'weak_password': {
            'definition': 'A weak password is easy to guess or crack, making accounts vulnerable to unauthorized access.',
            'risk': 'Hackers can guess weak passwords in seconds using automated tools.',
            'characteristics': [
                'Too short (less than 8 characters)',
                'Common words (password, name, dates)',
                'Only lowercase or uppercase',
                'No numbers or special characters',
                'Reused across multiple accounts'
            ],
            'strong_password': {
                'length': 'At least 12-16 characters',
                'mix': 'Uppercase, lowercase, numbers, special characters',
                'unique': 'Different for each important account',
                'storage': 'Use password manager, not written down'
            }
        },
        'man_in_the_middle': {
            'definition': 'A man-in-the-middle (MITM) attack intercepts communication between two parties to steal or modify data.',
            'risks': [
                'Credential theft',
                'Data interception',
                'Session hijacking',
                'Website spoofing'
            ],
            'prevention': [
                'Use HTTPS (look for padlock in address bar)',
                'Avoid public WiFi for sensitive transactions',
                'Use VPN on public networks',
                'Verify SSL certificates',
                'Keep software updated'
            ]
        },
        'ransomware': {
            'definition': 'Ransomware encrypts your files and demands payment to restore access.',
            'danger': 'Can occur rapidly and disable entire systems.',
            'prevention': [
                'Regular backups (offline)',
                'Keep software updated',
                'Don\'t open suspicious attachments',
                'Use trusted antivirus',
                'Employee training'
            ],
            'if_infected': [
                'Disconnect from network immediately',
                'Don\'t pay ransom',
                'Report to authorities',
                'Contact cybersecurity professionals',
                'Restore from backups'
            ]
        }
    }
    
    # Security glossary terms
    GLOSSARY = {
        'encryption': 'Converting data into code to prevent unauthorized access. Only someone with the decryption key can read it.',
        'firewall': 'A security system that monitors and controls network traffic, blocking suspicious connections.',
        'two_factor_authentication': 'A security method requiring two types of verification (e.g., password + phone code) to access an account.',
        'vpn': 'Virtual Private Network - encrypts your internet connection and hides your IP address.',
        'https': 'Secure version of HTTP - uses encryption to protect data between your browser and website.',
        'ssl_certificate': 'A digital certificate that proves a website\'s identity and enables HTTPS encryption.',
        'hash': 'A fixed-length code generated from data. Useful for verifying data hasn\'t been changed.',
        'cyber_threat': 'Any malicious attack or activity designed to compromise computer systems or steal data.',
        'privilege_escalation': 'Gaining higher-level access than originally granted, often through exploiting vulnerabilities.',
        'zero_day': 'A security vulnerability unknown to the software vendor, making it impossible to patch immediately.',
    }
    
    def __init__(self):
        self.conversation_history = []
        self.user_level = 'beginner'  # Track user knowledge level
    
    def process_query(self, user_message: str) -> AssistantResponse:
        """Process user query and provide security guidance"""
        
        # Add to conversation history
        self.conversation_history.append({
            'type': 'user',
            'message': user_message,
            'timestamp': datetime.now()
        })
        
        # Classify the query
        category = self._classify_query(user_message)
        
        # Generate response based on category and user level
        if category == 'threat_detection':
            response = self._handle_threat_detection(user_message)
        elif category == 'glossary_term':
            response = self._handle_glossary_query(user_message)
        elif category == 'threat_explanation':
            response = self._handle_threat_explanation(user_message)
        elif category == 'password_advice':
            response = self._handle_password_advice(user_message)
        elif category == 'best_practice':
            response = self._handle_best_practice(user_message)
        else:
            response = self._handle_general_security(user_message)
        
        # Add response to history
        self.conversation_history.append({
            'type': 'assistant',
            'message': response.message,
            'timestamp': datetime.now()
        })
        
        return response
    
    def _classify_query(self, message: str) -> str:
        """Classify user query type"""
        message_lower = message.lower()
        
        # Threat detection
        if any(word in message_lower for word in ['is this', 'is it', 'looks like', 'could this be', 'seems like']):
            if any(word in message_lower for word in ['phishing', 'malware', 'virus', 'threat', 'dangerous', 'safe']):
                return 'threat_detection'
        
        # Glossary terms
        if 'what is' in message_lower or 'what does' in message_lower or 'define' in message_lower:
            return 'glossary_term'
        
        # Threat explanation
        if any(word in message_lower for word in ['explain', 'tell me about', 'how does', 'works']):
            if any(word in message_lower for word in ['phishing', 'malware', 'hacking', 'ransomware']):
                return 'threat_explanation'
        
        # Password advice
        if any(word in message_lower for word in ['password', 'strong', 'secure', 'weak']):
            return 'password_advice'
        
        # Best practices
        if any(word in message_lower for word in ['how to', 'how can i', 'should i', 'recommended', 'best']):
            return 'best_practice'
        
        return 'general'
    
    def _handle_threat_detection(self, message: str) -> AssistantResponse:
        """Handle threat detection queries"""
        
        # Analyze the threat description
        threats = self._detect_mentioned_threats(message)
        
        analysis = f"Based on your description, I've identified potential security concerns:\n\n"
        
        for threat in threats:
            if threat in self.THREAT_KB:
                kb = self.THREAT_KB[threat]
                analysis += f"THREAT: {threat.upper()}\n"
                analysis += f"Description: {kb['definition']}\n\n"
        
        analysis += "RECOMMENDATIONS:\n"
        analysis += "1. DO NOT click on suspicious links\n"
        analysis += "2. DO NOT enter personal information\n"
        analysis += "3. Report to your email provider\n"
        analysis += "4. Report to relevant authorities if needed\n"
        
        follow_ups = [
            f"Do you need more details about any of these threats?",
            f"Would you like to know how to protect yourself?",
            f"Do you want to analyze this content further?"
        ]
        
        return AssistantResponse(
            message=analysis,
            confidence=0.85,
            category='threat_detection',
            references=[threat.capitalize() for threat in threats],
            follow_up_questions=follow_ups
        )
    
    def _handle_glossary_query(self, message: str) -> AssistantResponse:
        """Handle glossary/terminology queries"""
        
        term = self._extract_term(message)
        term_key = term.lower().replace(' ', '_')
        
        if term_key in self.GLOSSARY:
            definition = self.GLOSSARY[term_key]
            response = f"**{term.upper()}**\n\n{definition}\n\n"
            response += "In simple terms: This is an important security concept. Understanding it helps you stay safe online."
            
            follow_ups = [
                f"How is {term} used in real security?",
                f"Can you give me an example of {term}?",
                f"What's the benefit of {term}?"
            ]
        else:
            response = f"I don't have a definition for '{term}' in my knowledge base, but it sounds like a security-related topic. "
            response += "Can you provide more context so I can help better?"
            follow_ups = ["What context is this term used in?"]
        
        return AssistantResponse(
            message=response,
            confidence=0.9 if term_key in self.GLOSSARY else 0.5,
            category='glossary_term',
            references=[term],
            follow_up_questions=follow_ups
        )
    
    def _handle_threat_explanation(self, message: str) -> AssistantResponse:
        """Explain common threats"""
        
        threat = self._extract_threat(message)
        threat_key = threat.lower().replace(' ', '_')
        
        if threat_key in self.THREAT_KB:
            kb = self.THREAT_KB[threat_key]
            
            explanation = f"**{threat.upper()}**\n\n"
            explanation += f"{kb['definition']}\n\n"
            
            if 'indicators' in kb:
                explanation += "SIGNS TO WATCH FOR:\n"
                for indicator in kb['indicators'][:3]:
                    explanation += f"• {indicator}\n"
                explanation += "\n"
            
            if 'prevention' in kb:
                explanation += "HOW TO PROTECT YOURSELF:\n"
                for prevention in kb['prevention'][:3]:
                    explanation += f"• {prevention}\n"
            
            follow_ups = [
                f"How can I detect {threat}?",
                f"What should I do if I suspect {threat}?",
                f"Are there tools to prevent {threat}?"
            ]
        else:
            explanation = f"I don't have detailed information about '{threat}', but it's a cybersecurity concern. "
            explanation += "Can you provide more specifics?"
            follow_ups = []
        
        return AssistantResponse(
            message=explanation,
            confidence=0.85,
            category='threat_explanation',
            references=[threat],
            follow_up_questions=follow_ups
        )
    
    def _handle_password_advice(self, message: str) -> AssistantResponse:
        """Provide password security advice"""
        
        pwd_kb = self.THREAT_KB['weak_password']
        
        advice = "**PASSWORD SECURITY ADVICE**\n\n"
        advice += "A strong password is your first line of defense:\n\n"
        
        advice += "CHARACTERISTICS OF A STRONG PASSWORD:\n"
        advice += f"• Length: {pwd_kb['strong_password']['length']}\n"
        advice += f"• Mix: {pwd_kb['strong_password']['mix']}\n"
        advice += f"• Unique: {pwd_kb['strong_password']['unique']}\n"
        advice += f"• Storage: {pwd_kb['strong_password']['storage']}\n\n"
        
        advice += "AVOID THESE MISTAKES:\n"
        for char in pwd_kb['characteristics'][:3]:
            advice += f"• {char}\n"
        
        advice += "\nBEST PRACTICE: Use a password manager to generate and store complex passwords safely."
        
        follow_ups = [
            "How can I check if my current password is strong?",
            "What's a good password manager?",
            "How often should I change passwords?"
        ]
        
        return AssistantResponse(
            message=advice,
            confidence=0.95,
            category='password_advice',
            references=['Password Security'],
            follow_up_questions=follow_ups
        )
    
    def _handle_best_practice(self, message: str) -> AssistantResponse:
        """Provide cybersecurity best practices"""
        
        practice = "**CYBERSECURITY BEST PRACTICES**\n\n"
        practice += "Here are essential steps to stay safer online:\n\n"
        
        practice += "🔒 ACCOUNT SECURITY:\n"
        practice += "• Use strong, unique passwords for each account\n"
        practice += "• Enable two-factor authentication (2FA)\n"
        practice += "• Regularly change passwords for important accounts\n\n"
        
        practice += "🛡️ NETWORK SECURITY:\n"
        practice += "• Always use HTTPS websites (look for padlock)\n"
        practice += "• Avoid public WiFi without VPN\n"
        practice += "• Keep your router firmware updated\n\n"
        
        practice += "🚨 AWARENESS:\n"
        practice += "• Don't click suspicious links\n"
        practice += "• Verify sender before sharing information\n"
        practice += "• Keep software and OS updated\n\n"
        
        practice += "💾 DATA PROTECTION:\n"
        practice += "• Back up important data regularly\n"
        practice += "• Use encryption for sensitive files\n"
        practice += "• Be careful what you share online\n"
        
        follow_ups = [
            "Which of these should I prioritize?",
            "How do I implement two-factor authentication?",
            "What's the best backup strategy?"
        ]
        
        return AssistantResponse(
            message=practice,
            confidence=0.9,
            category='best_practice',
            references=['Cybersecurity Best Practices'],
            follow_up_questions=follow_ups
        )
    
    def _handle_general_security(self, message: str) -> AssistantResponse:
        """Handle general security questions"""
        
        response = "I understand you're asking about security. Here are some key points:\n\n"
        response += "• Security is everyone's responsibility\n"
        response += "• Most threats can be prevented with awareness\n"
        response += "• Don't hesitate to ask for help\n"
        response += "• Keep learning about cybersecurity\n\n"
        response += "Can you be more specific about what you'd like to know?"
        
        follow_ups = [
            "What security topic interests you?",
            "Do you have a specific concern?",
            "Would you like a security assessment?"
        ]
        
        return AssistantResponse(
            message=response,
            confidence=0.5,
            category='general',
            references=[],
            follow_up_questions=follow_ups
        )
    
    def _detect_mentioned_threats(self, message: str) -> List[str]:
        """Extract threat types mentioned in message"""
        threats = []
        message_lower = message.lower()
        
        for threat_type in self.THREAT_KB.keys():
            if threat_type.replace('_', ' ') in message_lower:
                threats.append(threat_type)
        
        return threats if threats else ['unknown_threat']
    
    def _extract_threat(self, message: str) -> str:
        """Extract threat name from message"""
        for threat in self.THREAT_KB.keys():
            if threat.replace('_', ' ') in message.lower():
                return threat.replace('_', ' ').title()
        return "Security Threat"
    
    def _extract_term(self, message: str) -> str:
        """Extract term from query"""
        # Simple extraction - could be more sophisticated
        words = message.split()
        if 'what' in message.lower():
            # Get words after 'is' or 'does'
            if 'is' in message.lower():
                idx = message.lower().index('is') + 2
                return message[idx:].strip()
        return 'unknown'


# Example usage
if __name__ == "__main__":
    assistant = SecurityAssistant()
    
    test_queries = [
        "Is this email safe? It asks me to verify my PayPal password.",
        "What is phishing?",
        "How can I create a strong password?",
        "What are the best security practices?",
        "Define HTTPS for me"
    ]
    
    for query in test_queries:
        print(f"\nUSER: {query}")
        response = assistant.process_query(query)
        print(f"ASSISTANT: {response.message}")
        print(f"Confidence: {response.confidence:.0%}")
        print(f"Follow-up questions: {response.follow_up_questions[0]}")
        print("-" * 60)
