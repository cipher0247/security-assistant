import re
from urllib.parse import urlparse, parse_qs

class SqliSignalDetector:
    def __init__(self):
        # Common SQL error patterns (passive detection in response)
        self.error_patterns = [
            r"Syntax error in SQL statement",
            r"You have an error in your SQL syntax",
            r"Unclosed quotation mark after the character string",
            r"Warning: mysql_",
            r"function\.mysql",
            r"PostgreSQL.*ERROR",
            r"Driver.* SQL[\-\_]*Server",
            r"ORA-[0-9][0-9][0-9][0-9]",
            r"Microsoft Access Driver",
            r"Unclosed quotation mark"
        ]

    def check_signals(self, url: str, response_text: str):
        signals = []
        risk_level = "NONE"
        
        # Check 1: URL Parameters
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        if params:
            signals.append("URL contains parameters (entry points)")
            risk_level = "LOW"
            
        # Check 2: Error Leakage in Response
        for pattern in self.error_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                signals.append(f"Potential SQL error message detected: {pattern}")
                risk_level = "HIGH"
                break # High risk confirmed
        
        # Check 3: "id=" pattern (heuristic)
        if "id=" in parsed.query.lower():
            if risk_level == "LOW":
                signals.append("Numerical ID parameter detected (common target)")
                # weak signal, doesn't escalate to MEDIUM/HIGH alone usually, but interesting
        
        return {
            "sqli_signals": signals,
            "sqli_risk": risk_level
        }
