class RiskEngine:
    @staticmethod
    def calculate_file_risk(scan_result: dict) -> str:
        # Simple heuristic
        # If VirusTotal API was connected, we'd use that.
        # Here we use entropy + extension.
        
        risk_score = 0
        if scan_result.get('suspicious_extension'):
            risk_score += 4
        if scan_result.get('entropy', 0) > 7.0:
            risk_score += 3
            
        if risk_score >= 5:
            return "HIGH"
        elif risk_score >= 3:
            return "MEDIUM"
        else:
            return "LOW"

    @staticmethod
    def calculate_url_risk(scan_result: dict) -> str:
        if "error" in scan_result:
            return "UNKNOWN"
            
        missing = len(scan_result.get('missing_security_headers', []))
        https = scan_result.get('https', False)
        sqli_risk = scan_result.get('sqli_analysis', {}).get('sqli_risk', 'NONE')
        xss_risk = scan_result.get('xss_analysis', {}).get('xss_risk', 'LOW')
        server_leaks = len(scan_result.get('server_leaks', []))
        cookie_issues = len(scan_result.get('cookie_issues', []))
        
        score = 0
        
        # Base checks
        if not https:
            score += 4 
        if missing >= 3:
            score += 2
            
        # Specific Signal Risks
        if sqli_risk == "HIGH":
            score += 5
        elif sqli_risk == "MEDIUM":
            score += 3
        elif sqli_risk == "LOW":
            score += 1
            
        if xss_risk == "HIGH":
            score += 5
        elif xss_risk == "MEDIUM":
            score += 3
            
        # Info Leaks & Cookies
        if server_leaks > 0:
            score += 1
        if cookie_issues > 0:
            score += 1
            
        # Determine Level
        if score >= 6:
            return "HIGH"
        elif score >= 3:
            return "MEDIUM"
        else:
            return "LOW"
