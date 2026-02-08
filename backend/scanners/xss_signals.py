import re

class XssSignalDetector:
    def __init__(self):
        self.dangerous_sinks = [
            r"innerHTML",
            r"document\.write",
            r"eval\(",
            r"setTimeout\(.*var",
            r"setInterval\(.*var",
            r"execScript",
            r"crypto\.generateCRMFRequest" # Just an example sink
        ]

    def check_signals(self, response_text: str, headers: dict):
        signals = []
        risk_level = "LOW"
        
        # Check 1: Missing CSP (already checked in UrlScan, but refined here)
        csp = headers.get("content-security-policy", "")
        if not csp:
            signals.append("No Content-Security-Policy (CSP) header found")
            risk_level = "MEDIUM"
        elif "unsafe-inline" in csp:
            signals.append("CSP allows 'unsafe-inline' (weakness)")
        
        # Check 2: Dangerous JS Sinks in source
        # This is very noisy on modern sites (react, etc), so we must be careful.
        # We flag it as informational or low risk unless correlated.
        found_sinks = 0
        for sink in self.dangerous_sinks:
            if re.search(sink, response_text):
                found_sinks += 1
                if found_sinks <= 3: # Limit noise
                    signals.append(f"Potential Dangerous JS Sink found: {sink}")
        
        if found_sinks > 0 and risk_level == "LOW":
            risk_level = "LOW" # Sinks alone are not High risk without input
            
        # Check 3: Reflected Input (Hypothetical - requires input knowledge)
        # If we knew the input was "xyz", we'd check if "xyz" is in response.
        # Since we are passive, we skip active reflection checks unless we parse the URL params.
        
        return {
            "xss_signals": signals,
            "xss_risk": risk_level
        }
