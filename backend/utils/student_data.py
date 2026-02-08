import random

# Large pool of questions
quiz_pool = [
    {
        "id": 1,
        "question": "You receive an email from 'Netflix Support' asking you to update your payment details via a link. What should you do?",
        "options": ["Click immediately", "Reply asking if real", "Go strictly to Netflix.com", "Forward to friends"],
        "correct": 2,
        "explanation": "Always go directly to the service provider's website. Phishing links often look convincing.",
        "difficulty": "Easy"
    },
    {
        "id": 2,
        "question": "Which of these is a strong password?",
        "options": ["Password123", "Tr0ub4dor&3", "correct horse battery staple", "admin"],
        "correct": 2,
        "explanation": "Passphrases (long strings of random words) are secure and easier to remember than short complex codes.",
        "difficulty": "Easy"
    },
    {
        "id": 3,
        "question": "What does HTTPS indicate?",
        "options": ["Site is 100% safe", "Connection is encrypted", "Hosted by Google", "No viruses"],
        "correct": 1,
        "explanation": "HTTPS encrypts the transit data but does not guarantee the server itself is not malicious.",
        "difficulty": "Easy"
    },
    {
        "id": 4,
        "question": "What is Phishing?",
        "options": ["A sport", "Social engineering via email/SMS", "Hacking Wi-Fi", "A virus type"],
        "correct": 1,
        "explanation": "Phishing involves tricking users into revealing sensitive info via deceptive messages.",
        "difficulty": "Easy"
    },
    {
        "id": 5,
        "question": "Which port is commonly used for SSH?",
        "options": ["80", "443", "22", "21"],
        "correct": 2,
        "explanation": "Port 22 is the standard port for Secure Shell (SSH) traffic.",
        "difficulty": "Medium"
    },
    {
        "id": 6,
        "question": "What does SQL Injection target?",
        "options": ["The Database", "The Wi-Fi", "The Browser", "The CPU"],
        "correct": 0,
        "explanation": "SQLi targets the backend database by injecting malicious queries.",
        "difficulty": "Medium"
    },
    {
        "id": 7,
        "question": "What is 2FA?",
        "options": ["2 Fast Apps", "Two-Factor Authentication", "To For All", "Token Free Access"],
        "correct": 1,
        "explanation": "Two-Factor Authentication adds a second layer of security beyond just a password.",
        "difficulty": "Easy"
    },
    {
        "id": 8,
        "question": "Which is a 'Social Engineering' attack?",
        "options": ["DDoS", "Pretexting", "Buffer Overflow", "Man-in-the-Middle"],
        "correct": 1,
        "explanation": "Pretexting involves creating a fabricated scenario to manipulate a victim (human element).",
        "difficulty": "Medium"
    },
    {
        "id": 9,
        "question": "What does VPN stand for?",
        "options": ["Very Private Network", "Virtual Public Network", "Virtual Private Network", "Virus Protection Net"],
        "correct": 2,
        "explanation": "A Virtual Private Network creates a secure connection over a less secure network.",
        "difficulty": "Easy"
    },
    {
        "id": 10,
        "question": "Ransomware is a type of malware that:",
        "options": ["Steals passwords", "Encrypts files and demands payment", "Mines crypto", "Records keystrokes"],
        "correct": 1,
        "explanation": "Ransomware locks victim data until a ransom is paid.",
        "difficulty": "Easy"
    },
    {
        "id": 11,
        "question": "Which CIA Triad component does Encryption primarily protect?",
        "options": ["Confidentiality", "Integrity", "Availability", "Authorization"],
        "correct": 0,
        "explanation": "Encryption ensures that data remains confidential and unreadable to unauthorized users.",
        "difficulty": "Medium"
    },
    {
        "id": 12,
        "question": "What is a 'Zero-Day' vulnerability?",
        "options": ["A bug open for 0 days", "A flaw known to vendors but not hackers", "A vulnerability unknown to the software vendor", "A virus that deletes data in 0 days"],
        "correct": 2,
        "explanation": "A Zero-Day is a vulnerability that has been disclosed but has no patch available yet.",
        "difficulty": "Hard"
    },
    {
        "id": 13,
        "question": "Which HTTP status code indicates 'Unauthorized'?",
        "options": ["200", "404", "401", "500"],
        "correct": 2,
        "explanation": "401 Unauthorized indicates that the request has not been applied because it lacks valid authentication credentials.",
        "difficulty": "Medium"
    },
    {
        "id": 14,
        "question": "Which command checks network connectivity?",
        "options": ["ls", "ping", "cd", "mkdir"],
        "correct": 1,
        "explanation": "The 'ping' command sends ICMP Echo Request packets to test reachability.",
        "difficulty": "Easy"
    },
    {
        "id": 15,
        "question": "Cross-Site Scripting (XSS) is a vulnerability in...",
        "options": ["Server-side databases", "Client-side web applications", "Network firewalls", "Operating System Kernels"],
        "correct": 1,
        "explanation": "XSS allows attackers to inject malicious scripts into web pages viewed by other users.",
        "difficulty": "Medium"
    },
    {
        "id": 16,
        "question": "What type of attack tries to guess a password by checking every possible combination?",
        "options": ["Phishing", "Brute Force", "SQL Injection", "Man-in-the-Middle"],
        "correct": 1,
        "explanation": "Brute Force attacks systematically check all possible passwords and passphrases until the correct one is found.",
        "difficulty": "Easy"
    }
]

def get_random_quiz(count=5):
    # This might need update to filter by difficulty later in API
    return random.sample(quiz_pool, min(count, len(quiz_pool)))

career_guide = [
    {
        "title": "Phase 1: The Foundation (0-6 Months)",
        "content": "Before breaking things, you must know how they work. Focus on:<br>• <b>Networking:</b> TCP/IP, DNS, HTTP/S, OSI Model. (CompTIA Network+)<br>• <b>Operating Systems:</b> Linux Command Line (Kali/Ubuntu) and Windows Registry/AD.<br>• <b>Coding:</b> Python for scripting, Bash for automation, and basic HTML/JS."
    },
    {
        "title": "Phase 2: Security Core (6-12 Months)",
        "content": "Start learning security concepts and tools.<br>• <b>Concepts:</b> CIA Triad, Access Control, Cryptography basics.<br>• <b>Tools:</b> Nmap (Scanning), Wireshark (Packet Analysis), Burp Suite (Web Proxies).<br>• <b>Practice:</b> Start 'Capture The Flag' (CTF) challenges on sites like TryHackMe or PicoCTF."
    },
    {
        "title": "Phase 3: Specialization (Year 2+)",
        "content": "Choose a path:<br>• <b>Red Team (Offensive):</b> Penetration Testing, Exploit Dev (OSCP logic).<br>• <b>Blue Team (Defensive):</b> SOC Analyst, Incident Response, Malware Analysis.<br>• <b>AppSec:</b> Securing software development lifecycles (DevSecOps)."
    },
    {
        "title": "Phase 4: Professional & Advanced",
        "content": "Validate your skills with certifications.<br>• <b>Entry:</b> CompTIA Security+ (Required by many jobs).<br>• <b>Advanced:</b> OSCP (Hands-on Hacking), CISSP (Management), SANS GIAC.<br>• <b>Community:</b> Attend conferences (DefCon, BSides) and contribute to open source."
    }
]

cheat_sheets = {
    "ports": [
        {"port": "20/21", "service": "FTP", "desc": "File Transfer Protocol"},
        {"port": "22", "service": "SSH", "desc": "Secure Shell (Remote Login)"},
        {"port": "23", "service": "Telnet", "desc": "Unencrypted Text Comm"},
        {"port": "25", "service": "SMTP", "desc": "Simple Mail Transfer"},
        {"port": "53", "service": "DNS", "desc": "Domain Name System"},
        {"port": "80", "service": "HTTP", "desc": "Web Traffic (Unencrypted)"},
        {"port": "443", "service": "HTTPS", "desc": "Web Traffic (Encrypted)"},
        {"port": "3306", "service": "MySQL", "desc": "Database"},
        {"port": "3389", "service": "RDP", "desc": "Remote Desktop"},
        {"port": "5432", "service": "PostgreSQL", "desc": "Database"},
        {"port": "8080", "service": "HTTP-Alt", "desc": "Web Proxy / Alt Web"}
    ],
    "linux": [
        {"cmd": "ls -la", "desc": "List all files (including hidden)"},
        {"cmd": "chmod +x file", "desc": "Make file executable"},
        {"cmd": "grep -r 'text' .", "desc": "Recursive search for text"},
        {"cmd": "ps aux | grep name", "desc": "Find specific process"},
        {"cmd": "netstat -tulnp", "desc": "Show listening ports with PIDs"},
        {"cmd": "whoami", "desc": "Current user info"},
        {"cmd": "sudo systemctl status [service]", "desc": "Check service status"},
        {"cmd": "curl -I [url]", "desc": "Fetch HTTP Headers Only"},
        {"cmd": "tail -f /var/log/syslog", "desc": "Follow system logs"}
    ],
    "owasp": [
        {"vuln": "A01: Broken Access Control", "desc": "Users can act outside of their intended permissions."},
        {"vuln": "A02: Cryptographic Failures", "desc": "Failures leading to sensitive data exposure (e.g. cleartext passwords)."},
        {"vuln": "A03: Injection", "desc": "Untrusted data is sent to an interpreter (SQLi, XSS)."},
        {"vuln": "A04: Insecure Design", "desc": "Missing security controls in the design phase."},
        {"vuln": "A05: Security Misconfiguration", "desc": "Default configs, open cloud storage, verbose error messages."},
        {"vuln": "A06: Vulnerable Components", "desc": "Using libraries/frameworks with known vulnerabilities."},
        {"vuln": "A07: Auth Failures", "desc": "Weak passwords, session management issues."},
        {"vuln": "A08: Integrity Failures", "desc": "Updates/plugins from untrusted sources."},
        {"vuln": "A09: Logging Failures", "desc": "Breaches cannot be detected or investigated due to lack of logs."},
        {"vuln": "A10: SSRF", "desc": "Server-Side Request Forgery - server fetches data from internal/external resources."}
    ],
    "exploits": [
        {"name": "Buffer Overflow", "desc": "Writing more data to a buffer than it can hold, overwriting adjacent memory."},
        {"name": "CSRF", "desc": "Cross-Site Request Forgery - forcing a user to execute unwanted actions."},
        {"name": "Directory Traversal", "desc": "Accessing files and directories outside the web root folder (../)."},
        {"name": "RCE", "desc": "Remote Code Execution - attacker runs arbitrary code on the target machine."},
        {"name": "MITM", "desc": "Man-In-The-Middle - intercepting traffic between two parties."}
    ]
}
