import re
import math
try:
    from sklearn.ensemble import RandomForestClassifier
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

class PhishingDetector:
    def __init__(self):
        self.ml_model = None
        self.suspicious_keywords = ["login", "signin", "bank", "verify", "account", "update", "confirm", "security"]
        self.top_targets = ["google", "paypal", "apple", "microsoft", "facebook", "netflix"]
        
        if SKLEARN_AVAILABLE:
            self._train_mini_model()

    def _train_mini_model(self):
        # Mini-dataset of Features: [length, num_dots, num_hyphens, has_ip, num_suspicious_words]
        # Label: 0 = Benign, 1 = Phishing
        X = [
            [20, 2, 0, 0, 0], [25, 2, 0, 0, 0], [30, 3, 0, 0, 0], [18, 2, 0, 0, 0], # Benign (google.com, etc)
            [55, 4, 2, 0, 2], [60, 5, 3, 0, 3], [45, 3, 1, 1, 1], [70, 6, 2, 0, 2]  # Phishing
        ]
        y = [0, 0, 0, 0, 1, 1, 1, 1]
        
        self.ml_model = RandomForestClassifier(n_estimators=10, random_state=42)
        self.ml_model.fit(X, y)

    def _extract_url_features(self, url: str):
        # Simplified Feature Extraction
        features = []
        features.append(len(url))
        features.append(url.count('.'))
        features.append(url.count('-'))
        features.append(1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) else 0)
        
        cnt = 0
        loss_cur = url.lower()
        for kw in self.suspicious_keywords:
            if kw in loss_cur:
                 cnt += 1
        features.append(cnt)
        return features

    def scan_url_ml(self, url: str):
        if not self.ml_model:
            return {"risk": "UNKNOWN", "confidence": 0, "reason": "ML Module not active"}
            
        features = self._extract_url_features(url)
        prediction = self.ml_model.predict([features])[0]
        prob = self.ml_model.predict_proba([features])[0][1]
        
        risk = "HIGH" if prediction == 1 else "LOW"
        reason = "ML Model detected phishing patterns" if prediction == 1 else "ML Model classifies as benign"
        
        return {
            "risk": risk,
            "confidence": round(prob * 100, 2),
            "reason": reason,
            "features_analyzed": features
        }

    def scan_email(self, subject: str, body: str):
        score = 0
        triggers = []
        
        # Urgency Triggers
        urgency_words = ["urgent", "immediate", "suspend", "24 hours", "lock", "unauthorized"]
        for w in urgency_words:
            if w in subject.lower() or w in body.lower():
                score += 2
                triggers.append(f"Urgency keyword: '{w}'")

        # Sensitive Requests
        sensitive_words = ["password", "credit card", "ssn", "social security", "bank account"]
        for w in sensitive_words:
            if w in body.lower():
                score += 3
                triggers.append(f"Sensitive information request: '{w}'")
                
        # Link Analysis (Simple)
        links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
        for link in links:
            if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', link):
                score += 2
                triggers.append("IP-based URL detected")
                
        risk = "LOW"
        if score >= 2: risk = "MEDIUM"
        if score >= 4: risk = "HIGH"
        
        return {
            "risk": risk,
            "score": score,
            "triggers": triggers,
            "link_count": len(links)
        }
