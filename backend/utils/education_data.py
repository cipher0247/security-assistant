glossary_data = [
    {
        "term": "SQL Injection (SQLi)",
        "definition": "A vulnerability where an attacker interferes with the queries an application makes to its database. This can verify data access or unauthorized modifications.",
        "prevention": "Use Prepared Statements (parameterized queries) and input validation.",
        "category": "Web Security",
        "related_terms": ["Database", "Input Validation", "Prepared Statements"],
        "examples": ["' OR 1=1 --", "admin' --"],
        "video": "https://www.youtube.com/embed/ciNHn38EyRc",
        "diagram": "sql_injection_flow"
    },
    {
        "term": "Cross-Site Scripting (XSS)",
        "definition": "A vulnerability that allows attackers to inject malicious scripts into web pages viewed by other users.",
        "prevention": "Context-aware output encoding and Content Security Policy (CSP).",
        "category": "Web Security",
        "related_terms": ["CSP", "Input Validation", "Cookie"],
        "examples": ["<script>alert('XSS')</script>", "<img src=x onerror=alert(1)>"],
        "video": "https://www.youtube.com/embed/EoaDgUgS6QA",
        "diagram": "xss_attack_flow"
    },
    {
        "term": "High Entropy",
        "definition": "In file analysis, high entropy often indicates packed or encrypted coding, which is a common characteristic of malware trying to hide its logic.",
        "prevention": "N/A (Detection metric)",
        "category": "Malware Analysis",
        "related_terms": ["Packing", "Encryption", "Obfuscation"],
        "examples": ["Packed executables", "Encrypted zip files"],
        "video": "",
        "diagram": ""
    },
    {
        "term": "HSTS",
        "definition": "HTTP Strict Transport Security. A header that tells browsers to ONLY access the site via HTTPS.",
        "prevention": "Enable the 'Strict-Transport-Security' header on your web server.",
        "category": "Network Security",
        "related_terms": ["HTTPS", "SSL/TLS", "Man-in-the-Middle (MitM)"],
        "examples": ["Strict-Transport-Security: max-age=31536000"],
        "video": "",
        "diagram": ""
    },
    {
        "term": "CSP",
        "definition": "Content Security Policy. A header that restricts the sources from which content (scripts, images) can be loaded.",
        "prevention": "Configure the 'Content-Security-Policy' header.",
        "category": "Web Security",
        "related_terms": ["Cross-Site Scripting (XSS)", "HTTP Headers"],
        "examples": ["default-src 'self'; script-src https://trusted.com"],
        "video": "",
        "diagram": ""
    },
    {
        "term": "Secure Cookie",
        "definition": "A cookie attribute that ensures the cookie is only sent over encrypted (HTTPS) connections.",
        "prevention": "Set the 'Secure' flag when creating cookies.",
        "category": "Web Security",
        "related_terms": ["HttpOnly Cookie", "HTTPS", "Session Hijacking"],
        "examples": ["Set-Cookie: session=123; Secure"],
        "video": "",
        "diagram": ""
    },
    {
        "term": "HttpOnly Cookie",
        "definition": "A cookie attribute that prevents JavaScript from accessing the cookie, protecting it from XSS attacks.",
        "prevention": "Set the 'HttpOnly' flag when creating cookies.",
        "category": "Web Security",
        "related_terms": ["Cross-Site Scripting (XSS)", "Secure Cookie"],
        "examples": ["Set-Cookie: session=123; HttpOnly"],
        "video": "",
        "diagram": ""
    },
    {
        "term": "Phishing",
        "definition": "A social engineering attack used to steal user data, including login credentials and credit card numbers.",
        "prevention": "Verify URL domains, check for spelling errors, and use MFA.",
        "category": "Social Engineering",
        "related_terms": ["Social Engineering", "Email Security", "Typosquatting"],
        "examples": ["Fake Netflix login email", "CEO Fraud"],
        "video": "https://www.youtube.com/embed/XBkzBrpZEqA",
        "diagram": "phishing_lifecycle"
    },
    {
        "term": "Ransomware",
        "definition": "Malware that encrypts a victim's files, with the attacker demanding a ransom to restore access.",
        "prevention": "Regular backups, endpoint protection, and avoid suspicious links.",
        "category": "Malware Analysis",
        "related_terms": ["Malware", "Encryption", "Phishing"],
        "examples": ["WannaCry", "Ryuk"],
        "video": "",
        "diagram": ""
    },
    {
        "term": "DDoS",
        "definition": "Distributed Denial of Service. An attack that floods a server with traffic to make it inaccessible to users.",
        "prevention": "Rate limiting, traffic analysis, and CDN usage.",
        "category": "Network Security",
        "related_terms": ["Botnet", "Availability", "Rate Limiting"],
        "examples": ["SYN Flood", "UDP Flood"],
        "video": "",
        "diagram": ""
    },
    {
        "term": "Zero-Day Exploit",
        "definition": "A cyber attack that occurs on the same day a weakness is discovered in software, before a fix is released.",
        "prevention": "Behavioral analysis and keeping software updated immediately upon patch release.",
        "category": "General Concepts",
        "related_terms": ["Vulnerability", "Patch Management", "Exploit"],
        "examples": ["Log4Shell (initially)", "EternalBlue"],
        "video": "",
        "diagram": ""
    },
    {
        "term": "Man-in-the-Middle (MitM)",
        "definition": "An attack where the attacker secretly relays and possibly alters the communications between two parties.",
        "prevention": "Use HTTPS/TLS and VPNs on public networks.",
        "category": "Network Security",
        "related_terms": ["Encryption", "HTTPS", "Wi-Fi Security"],
        "examples": ["ARP Spoofing", "Evil Twin Wi-Fi"],
        "video": "",
        "diagram": ""
    },
    {
        "term": "Brute Force",
        "definition": "An attack that consists of an attacker submitting many passwords or passphrases with the hope of eventually guessing correctly.",
        "prevention": "Account lockout policies, strong passwords, and rate limiting.",
        "category": "Authentication",
        "related_terms": ["Password Cracking", "Rate Limiting", "MFA"],
        "examples": ["Dictionary Attack", "Credential Stuffing"],
        "video": "",
        "diagram": ""
    },
    {
        "term": "Salting",
        "definition": "Adding random data to a password before hashing it to ensure that the same password does not result in the same hash.",
        "prevention": "N/A (Defensive Technique)",
        "category": "Cryptography",
        "related_terms": ["Hashing", "Rainbow Tables", "Password Storage"],
        "examples": ["hash(password + salt)"],
        "video": "",
        "diagram": ""
    },
    {
        "term": "Symmetric Encryption",
        "definition": "Encryption where the same key is used for both encryption and decryption (e.g., AES).",
        "prevention": "Secure key management.",
        "category": "Cryptography",
        "related_terms": ["Asymmetric Encryption", "AES", "Key Management"],
        "examples": ["AES-256", "ChaCha20"],
        "video": "",
        "diagram": ""
    },
    {
        "term": "Asymmetric Encryption",
        "definition": "Encryption that uses a pair of keys: a public key for encryption and a private key for decryption (e.g., RSA).",
        "prevention": "Authority validation (PKI).",
        "category": "Cryptography",
        "related_terms": ["Symmetric Encryption", "RSA", "Public Key Infrastructure (PKI)"],
        "examples": ["RSA", "ECC"],
        "video": "",
        "diagram": ""
    },
    # New Terms
    {
        "term": "OSI Model",
        "definition": "The Open Systems Interconnection model describes seven layers that computer systems use to communicate over a network.",
        "prevention": "N/A (Conceptual Model)",
        "category": "Network Security",
        "related_terms": ["TCP/IP", "Network Security", "Application Layer"],
        "examples": ["Physical, Data Link, Network, Transport, Session, Presentation, Application"],
        "video": "https://www.youtube.com/embed/nFa9FkN19_U",
        "diagram": "osi_model"
    },
    {
        "term": "CIA Triad",
        "definition": "The three pillars of information security: Confidentiality, Integrity, and Availability.",
        "prevention": "N/A (Security Model)",
        "category": "General Concepts",
        "related_terms": ["Confidentiality", "Integrity", "Availability"],
        "examples": ["Confidentiality: Encryption", "Integrity: Hashing", "Availability: Redundancy"],
        "video": "",
        "diagram": ""
    },
    {
        "term": "Multi-Factor Authentication (MFA)",
        "definition": "An authentication method that requires the user to provide two or more verification factors to gain access.",
        "prevention": "Implement MFA on all sensitive accounts.",
        "category": "Authentication",
        "related_terms": ["Two-Factor Authentication (2FA)", "Authentication", "Brute Force"],
        "examples": ["Password + SMS code", "Password + Authenticator App", "Biometrics"],
        "video": "",
        "diagram": ""
    },
    {
        "term": "Botnet",
        "definition": "A network of private computers infected with malicious software and controlled as a group without the owners' knowledge.",
        "prevention": "Endpoint protection, firewalls, and keeping software updated.",
        "category": "Malware Analysis",
        "related_terms": ["DDoS", "Command and Control (C2)", "Malware"],
        "examples": ["Mirai", "Emotet"],
        "video": "",
        "diagram": ""
    },
    {
        "term": "Social Engineering",
        "definition": "The art of manipulating people so they give up confidential information.",
        "prevention": "Security awareness training and verifying requests.",
        "category": "Social Engineering",
        "related_terms": ["Phishing", "Pretexting", "Vishing"],
        "examples": ["Phishing emails", "Tailgating", "Tech support scams"],
        "video": "",
        "diagram": ""
    }
]
