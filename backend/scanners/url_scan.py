import requests
import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime
from .sqli_signals import SqliSignalDetector
from .xss_signals import XssSignalDetector

class UrlScanner:
    def __init__(self):
        self.sqli_detector = SqliSignalDetector()
        self.xss_detector = XssSignalDetector()

    def scan_url(self, url: str):
        try:
            # Ensure scheme
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            parsed = urlparse(url)
            domain = parsed.netloc

            # Request the page (GET for body analysis)
            try:
                response = requests.get(url, timeout=10, allow_redirects=True)
                headers = {k.lower(): v for k, v in response.headers.items()}
                response_text = response.text
            except Exception as e:
                return {"error": f"Failed to reach URL: {str(e)}", "risk": "High"}

            # Header Analysis
            security_headers = {
                "strict-transport-security": "HSTS (Strict-Transport-Security)",
                "content-security-policy": "CSP (Content-Security-Policy)",
                "x-frame-options": "X-Frame-Options",
                "x-content-type-options": "X-Content-Type-Options"
            }

            missing_headers = []
            present_headers = []

            for header, name in security_headers.items():
                if header in headers:
                    present_headers.append(name)
                else:
                    missing_headers.append(name)

            # Enhanced Check: Server Info Leakage
            server_leaks = []
            if "server" in headers:
                server_leaks.append(f"Server Header exposed: {headers['server']}")
            if "x-powered-by" in headers:
                server_leaks.append(f"X-Powered-By exposed: {headers['x-powered-by']}")

            # Enhanced Check: Cookies
            cookies_issues = []
            for cookie in response.cookies:
                issues = []
                if not cookie.secure:
                    issues.append("Missing 'Secure' flag")
                if not cookie.has_nonstandard_attr('HttpOnly') and not cookie.rest.get('HttpOnly'):
                     # Requests cookies handling for HttpOnly can be tricky, heuristics here
                     pass 
                # Note: 'requests' cookiejar doesn't always expose HttpOnly easily if not sending Set-Cookie raw.
                # We will check raw Set-Cookie header if possible, or stick to basic Cookie object props.
                if issues:
                    cookies_issues.append(f"Cookie '{cookie.name}': {', '.join(issues)}")

            # Signal Detection
            sqli_results = self.sqli_detector.check_signals(url, response_text)
            xss_results = self.xss_detector.check_signals(response_text, headers)

            is_https = url.startswith("https")
            
            return {
                "url": url,
                "domain": domain,
                "https": is_https,
                "status_code": response.status_code,
                "missing_security_headers": missing_headers,
                "present_security_headers": present_headers,
                "server_leaks": server_leaks,
                "cookie_issues": cookies_issues,
                "sqli_analysis": sqli_results,
                "xss_analysis": xss_results
            }

        except Exception as e:
            return {"error": str(e), "risk": "Unknown"}
