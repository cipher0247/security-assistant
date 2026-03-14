#!/usr/bin/env python3
"""Generate a comprehensive user guide for the Security Assistant."""

from datetime import datetime
try:
    from fpdf import FPDF
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "fpdf2"], check=True)
    from fpdf import FPDF

class UserGuide(FPDF):
    def header(self):
        self.set_font("Arial", "B", 22)
        self.cell(0, 12, "Security Assistant", ln=True, align="C")
        self.set_font("Arial", "I", 12)
        self.cell(0, 6, "User Guide & Features", ln=True, align="C")
        self.set_font("Arial", "", 8)
        now = datetime.now().strftime('%B %d, %Y')
        self.cell(0, 4, "Generated: " + now, ln=True, align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Page " + str(self.page_no()), align="C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 15)
        self.set_fill_color(52, 73, 94)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, title, ln=True, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def section_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_text_color(52, 73, 94)
        self.cell(0, 8, title, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def subsection_title(self, title):
        self.set_font("Arial", "B", 11)
        self.set_text_color(100, 100, 100)
        self.cell(0, 7, title, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def body_text(self, text):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bullet_point(self, text, indent=5):
        self.set_font("Arial", "", 9)
        self.multi_cell(0, 4, "> " + text, 0)

    def code_block(self, text):
        self.set_font("Courier", "", 8)
        self.set_fill_color(240, 240, 240)
        self.multi_cell(0, 4, text, border=1, fill=True)
        self.ln(2)

    def feature_box(self, title, description):
        self.set_font("Arial", "B", 10)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(70, 130, 180)
        self.cell(0, 7, title, ln=True, fill=True)
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", "", 9)
        self.multi_cell(0, 4, description)
        self.ln(2)

# Create PDF
pdf = UserGuide()
pdf.add_page()

# ===== INTRODUCTION =====
pdf.chapter_title("1. WELCOME TO SECURITY ASSISTANT")
pdf.body_text(
    "Security Assistant is your personal cybersecurity companion, designed to help you understand, "
    "analyze, and protect against common security threats. Whether you are a student learning about security, "
    "a professional evaluating risk, or just curious about digital safety, this tool provides comprehensive "
    "analysis and educational resources."
)
pdf.body_text(
    "This guide will walk you through all features and show you exactly how to use each one."
)

# ===== GETTING STARTED =====
pdf.chapter_title("2. GETTING STARTED")

pdf.section_title("System Requirements")
pdf.bullet_point("Modern web browser (Chrome, Firefox, Safari, Edge)")
pdf.bullet_point("Internet connection (for some features)")
pdf.bullet_point("No special software installation required")
pdf.ln(2)

pdf.section_title("Accessing the Application")
pdf.body_text("The Security Assistant has a clean, user-friendly interface organized into three main areas:")
pdf.bullet_point("Top Navigation Bar - Quick access to all features")
pdf.bullet_point("Main Dashboard - Feature cards for quick access")
pdf.bullet_point("Settings Panel - Customize your preferences")
pdf.ln(2)

# ===== FEATURES OVERVIEW =====
pdf.chapter_title("3. FEATURES OVERVIEW")

pdf.section_title("Security Analysis Tools")
pdf.feature_box("Password Strength Analyzer", 
    "Evaluate how strong your passwords are and get suggestions for improvement.")
pdf.feature_box("File Security Scanner", 
    "Analyze uploaded files for suspicious patterns, entropy levels, and dangerous characteristics.")
pdf.feature_box("URL Safety Checker", 
    "Scan website URLs to identify HTTPS issues, missing security headers, and injection vulnerabilities.")
pdf.feature_box("Phishing Detector", 
    "Check if URLs or emails are likely phishing attempts using ML-based detection.")
pdf.feature_box("Hash Calculator", 
    "Generate hash values (MD5, SHA256, etc.) for files and text verification.")
pdf.feature_box("Metadata Viewer", 
    "Extract EXIF data and hidden metadata from images.")
pdf.feature_box("Password Generator", 
    "Create strong, random passwords with customizable settings.")
pdf.feature_box("Security News Feed", 
    "Stay updated with latest cybersecurity news and threats.")
pdf.ln(2)

pdf.section_title("Educational Resources")
pdf.feature_box("Security Glossary", 
    "Learn security terminology and concepts in simple, easy-to-understand language.")
pdf.feature_box("Interactive Quizzes", 
    "Test your knowledge with randomly generated security questions.")
pdf.feature_box("Career Guides", 
    "Explore cybersecurity career paths and requirements.")
pdf.feature_box("Cheat Sheets", 
    "Quick reference materials for common security topics.")
pdf.ln(2)

# ===== FEATURE USAGE =====
pdf.chapter_title("4. HOW TO USE EACH FEATURE")

# Feature 1: Password Strength Analyzer
pdf.section_title("4.1 Password Strength Analyzer")
pdf.subsection_title("What It Does")
pdf.body_text(
    "Analyzes your password and rates how strong it is. Shows vulnerabilities and suggestions "
    "for making it stronger. Works completely offline on your device."
)
pdf.subsection_title("Step-by-Step Instructions")
pdf.bullet_point("1. Click on 'Password Strength' in the dashboard")
pdf.bullet_point("2. Enter your password in the input field (not stored anywhere)")
pdf.bullet_point("3. Select attack mode: Offline (default), Online, or Supercomputer")
pdf.bullet_point("4. Choose hash type (MD5, SHA256, bcrypt)")
pdf.bullet_point("5. Click 'Analyze Password'")
pdf.bullet_point("6. View results: Rating, Score, and specific feedback")
pdf.subsection_title("Interpreting Results")
pdf.bullet_point("Rating: Weak, Fair, Good, Strong, Very Strong")
pdf.bullet_point("Score: Numeric value 0-100")
pdf.bullet_point("Feedback: Specific recommendations for improvement")
pdf.subsection_title("Example")
pdf.code_block("Input: 'password123'\nRating: Weak (Common word + simple pattern)\nSuggestion: Use uppercase, numbers, special characters")
pdf.ln(3)

# Feature 2: File Security Scanner
pdf.section_title("4.2 File Security Scanner")
pdf.subsection_title("What It Does")
pdf.body_text(
    "Scans uploaded files for security threats. Analyzes file entropy (randomness), detects dangerous "
    "extensions, and calculates an overall risk score."
)
pdf.subsection_title("Step-by-Step Instructions")
pdf.bullet_point("1. Click 'File Scanner' in the dashboard")
pdf.bullet_point("2. Click 'Choose File' or drag-and-drop a file")
pdf.bullet_point("3. System analyzes the file (max size varies)")
pdf.bullet_point("4. View results: Risk Level, Entropy, Extensions, Recommendations")
pdf.subsection_title("Risk Levels")
pdf.bullet_point("GREEN (Low): Appears safe, typical file characteristics")
pdf.bullet_point("YELLOW (Medium): Some suspicious indicators, exercise caution")
pdf.bullet_point("RED (High): Multiple red flags, do not execute or trust")
pdf.subsection_title("What Triggers Risk")
pdf.bullet_point("Dangerous file extensions (.exe, .bat, .scr)")
pdf.bullet_point("High entropy (random-looking data, possible encryption)")
pdf.bullet_point("Suspicious file signatures")
pdf.ln(3)

# Feature 3: URL Safety Checker
pdf.section_title("4.3 URL Safety Checker")
pdf.subsection_title("What It Does")
pdf.body_text(
    "Evaluates website URLs for security issues. Checks HTTPS, security headers, and potential "
    "SQL injection or XSS vulnerabilities."
)
pdf.subsection_title("Step-by-Step Instructions")
pdf.bullet_point("1. Click 'URL Scanner' in the dashboard")
pdf.bullet_point("2. Paste the full URL (e.g., https://example.com)")
pdf.bullet_point("3. Click 'Scan URL'")
pdf.bullet_point("4. Review results: Overall Risk, HTTPS Status, Security Headers, Vulnerabilities")
pdf.subsection_title("What Gets Checked")
pdf.bullet_point("HTTPS Encryption: Is the connection secure?")
pdf.bullet_point("Security Headers: Missing protective headers?")
pdf.bullet_point("SQL Injection Signals: Vulnerable input fields?")
pdf.bullet_point("XSS Vulnerabilities: Potential JavaScript injection?")
pdf.bullet_point("Server Information Leaks: Does server expose version info?")
pdf.ln(3)

# Feature 4: Phishing Detector
pdf.section_title("4.4 Phishing Detector")
pdf.subsection_title("What It Does")
pdf.body_text(
    "Uses machine learning to detect phishing URLs and suspicious email content. Helps you avoid "
    "scams and fake websites designed to steal your information."
)
pdf.subsection_title("Check Phishing URL")
pdf.bullet_point("1. Click 'Phishing Detector' menu")
pdf.bullet_point("2. Select 'Check URL' tab")
pdf.bullet_point("3. Paste the suspicious URL")
pdf.bullet_point("4. Click 'Scan for Phishing'")
pdf.bullet_point("5. Result shows: Phishing Risk (Yes/No), Confidence Score")
pdf.subsection_title("Check Phishing Email")
pdf.bullet_point("1. Select 'Check Email' tab")
pdf.bullet_point("2. Enter email subject line")
pdf.bullet_point("3. Paste email body text")
pdf.bullet_point("4. Click 'Analyze Email'")
pdf.bullet_point("5. Review risk indicators identified")
pdf.ln(2)

# Feature 5: Hash Calculator
pdf.section_title("4.5 Hash Calculator")
pdf.subsection_title("What It Does")
pdf.body_text(
    "Generates cryptographic hash values for text or files. Useful for verifying file integrity "
    "and creating checksums. Supports MD5, SHA-1, SHA-256, SHA-512."
)
pdf.subsection_title("For Text")
pdf.bullet_point("1. Click 'Hash Calculator'")
pdf.bullet_point("2. Enter your text in the input field")
pdf.bullet_point("3. Select hash algorithm (default: MD5)")
pdf.bullet_point("4. Click 'Calculate Hash'")
pdf.bullet_point("5. Copy hash value from results")
pdf.subsection_title("Why Use Hashes?")
pdf.bullet_point("Verify file authenticity - Compare with official checksums")
pdf.bullet_point("Detect tampering - Changed files produce different hashes")
pdf.bullet_point("Store securely - Hash passwords instead of plain text")
pdf.ln(2)

# Feature 6: Metadata Viewer
pdf.section_title("4.6 Metadata Viewer (EXIF Data)")
pdf.subsection_title("What It Does")
pdf.body_text(
    "Extracts hidden metadata from images, including camera info, GPS location, timestamps, "
    "and other embedded information that might reveal private details."
)
pdf.subsection_title("Instructions")
pdf.bullet_point("1. Click 'EXIF Viewer'")
pdf.bullet_point("2. Upload an image (JPG, PNG, etc.)")
pdf.bullet_point("3. View extracted metadata")
pdf.subsection_title("What Information Is Found?")
pdf.bullet_point("Camera Model - What device took the photo")
pdf.bullet_point("GPS Coordinates - Exact location where photo was taken")
pdf.bullet_point("Date/Time - When the photo was taken")
pdf.bullet_point("Software - What editing tools were used")
pdf.bullet_point("Copyright - Creator information")
pdf.subsection_title("Privacy Tip")
pdf.body_text(
    "Always remove EXIF data before sharing photos online to protect your privacy and location."
)
pdf.ln(2)

# Feature 7: Password Generator
pdf.section_title("4.7 Password Generator")
pdf.subsection_title("What It Does")
pdf.body_text(
    "Creates strong, random passwords with your exact specifications. Generated passwords are "
    "automatically checked for strength."
)
pdf.subsection_title("Instructions")
pdf.bullet_point("1. Click 'Password Generator'")
pdf.bullet_point("2. Set desired length (8-128 characters)")
pdf.bullet_point("3. Toggle options: Uppercase, Numbers, Symbols")
pdf.bullet_point("4. Click 'Generate'")
pdf.bullet_point("5. Copy the generated password")
pdf.bullet_point("6. View strength rating")
pdf.subsection_title("Best Practices")
pdf.bullet_point("Use 12+ characters for important accounts")
pdf.bullet_point("Always include uppercase, numbers, and symbols")
pdf.bullet_point("Use different passwords for each site")
pdf.bullet_point("Store passwords in a password manager")
pdf.ln(2)

# Feature 8: Security News
pdf.section_title("4.8 Security News Feed")
pdf.subsection_title("What It Does")
pdf.body_text(
    "Automatically fetches latest cybersecurity news and threat information from trusted sources. "
    "Stay informed about new vulnerabilities and security trends."
)
pdf.subsection_title("How to Use")
pdf.bullet_point("1. Click 'News' or 'Threat Feed'")
pdf.bullet_point("2. Browse latest articles")
pdf.bullet_point("3. Click article title to read full content")
pdf.ln(2)

# ===== EDUCATIONAL FEATURES =====
pdf.chapter_title("5. LEARNING & EDUCATION")

pdf.section_title("Security Glossary")
pdf.body_text(
    "Access security terminology explanations:"
)
pdf.bullet_point("1. Click 'Glossary' in Education menu")
pdf.bullet_point("2. Search for a term or browse all")
pdf.bullet_point("3. Read simple explanations")
pdf.bullet_point("4. See real-world examples")
pdf.ln(2)

pdf.section_title("Interactive Quizzes")
pdf.body_text(
    "Test your security knowledge:"
)
pdf.bullet_point("1. Click 'Quiz'")
pdf.bullet_point("2. Answer 5 randomly selected questions")
pdf.bullet_point("3. View your score")
pdf.bullet_point("4. See explanations for correct answers")
pdf.ln(2)

pdf.section_title("Career Guides")
pdf.body_text(
    "Explore security careers:"
)
pdf.bullet_point("1. Click 'Career Paths'")
pdf.bullet_point("2. Browse available positions")
pdf.bullet_point("3. View requirements and skills needed")
pdf.bullet_point("4. See salary ranges and job outlook")
pdf.ln(2)

pdf.section_title("Cheat Sheets")
pdf.body_text(
    "Quick reference guides:"
)
pdf.bullet_point("1. Click 'Cheat Sheets'")
pdf.bullet_point("2. Select topic")
pdf.bullet_point("3. Download or view reference material")
pdf.ln(2)

# ===== COMMON SCENARIOS =====
pdf.chapter_title("6. COMMON SCENARIOS & SOLUTIONS")

pdf.section_title("Scenario 1: Suspicious Email Received")
pdf.body_text("What to do:")
pdf.bullet_point("1. DO NOT click links or download attachments")
pdf.bullet_point("2. Copy the sender's email address")
pdf.bullet_point("3. Use Phishing Detector on the URL (if present)")
pdf.bullet_point("4. Check email content with Phishing Email scanner")
pdf.bullet_point("5. If confirmed phishing, report to email provider")
pdf.ln(2)

pdf.section_title("Scenario 2: Creating Accounts on Multiple Sites")
pdf.body_text("Recommended process:")
pdf.bullet_point("1. Use Password Generator to create strong passwords")
pdf.bullet_point("2. Check password strength with Password Analyzer")
pdf.bullet_point("3. Store in password manager (not browser)")
pdf.bullet_point("4. Use different password for each site")
pdf.ln(2)

pdf.section_title("Scenario 3: Sharing Photos Online")
pdf.body_text("Security checklist:")
pdf.bullet_point("1. Upload photo to EXIF Viewer")
pdf.bullet_point("2. Check what metadata is present")
pdf.bullet_point("3. Note GPS location data")
pdf.bullet_point("4. Remove EXIF using online tool before posting")
pdf.bullet_point("5. Check privacy settings on social media")
pdf.ln(2)

pdf.section_title("Scenario 4: Downloaded a File - Is It Safe?")
pdf.body_text("Security check:")
pdf.bullet_point("1. Upload file to File Scanner")
pdf.bullet_point("2. Review risk assessment")
pdf.bullet_point("3. If risk is HIGH - delete immediately")
pdf.bullet_point("4. If risk is MEDIUM - isolate file, don't execute")
pdf.bullet_point("5. If risk is LOW - can likely use safely")
pdf.ln(2)

# ===== PRIVACY & SECURITY =====
pdf.chapter_title("7. YOUR PRIVACY & SECURITY")

pdf.section_title("Data Privacy Guarantee")
pdf.bullet_point("No passwords are stored - All analysis is done on your device")
pdf.bullet_point("No uploads retained - Files are deleted immediately after scanning")
pdf.bullet_point("No account required - Use tools without creating account")
pdf.bullet_point("No tracking - Your activity is not monitored or recorded")
pdf.bullet_point("No ads - Free to use without advertisements")
pdf.ln(2)

pdf.section_title("Security Best Practices While Using")
pdf.bullet_point("Use on trusted computers only")
pdf.bullet_point("Keep your browser and OS updated")
pdf.bullet_point("Don't paste real passwords (use for testing only)")
pdf.bullet_point("Use HTTPS connection (shown in address bar)")
pdf.bullet_point("Log out after sensitive operations")
pdf.ln(2)

# ===== TIPS & TRICKS =====
pdf.chapter_title("8. TIPS & TRICKS")

pdf.bullet_point("Speed Tip: Bookmark frequently used tools for quick access")
pdf.bullet_point("Learning: Complete all glossary terms for comprehensive knowledge")
pdf.bullet_point("Testing: Use Password Generator to create test passwords for analysis")
pdf.bullet_point("Reference: Download and save cheat sheets for offline access")
pdf.bullet_point("News: Check security news weekly to stay current on threats")
pdf.bullet_point("Sharing: URL Scanner before clicking suspicious links from messages")
pdf.bullet_point("Safety: Always verify URLs in address bar match what you expect")
pdf.ln(3)

# ===== FAQ =====
pdf.chapter_title("9. FREQUENTLY ASKED QUESTIONS")

pdf.section_title("Q: Is this tool free?")
pdf.body_text("A: Yes! All features are completely free. No premium version or hidden costs.")
pdf.ln(2)

pdf.section_title("Q: Do you store my passwords?")
pdf.body_text("A: No. All password analysis happens locally on your device. Nothing is sent to servers.")
pdf.ln(2)

pdf.section_title("Q: Can I use this on mobile?")
pdf.body_text("A: Yes. The interface is responsive and works on phones, tablets, and desktops.")
pdf.ln(2)

pdf.section_title("Q: What if I find a file with HIGH risk?")
pdf.body_text("A: Delete it immediately. Do not execute or open it. Contact your IT support if in doubt.")
pdf.ln(2)

pdf.section_title("Q: Are the educational materials certified?")
pdf.body_text("A: Content is researched and vetted but designed for general learning. Consult official resources for certifications.")
pdf.ln(2)

pdf.section_title("Q: How often is security news updated?")
pdf.body_text("A: News is fetched in real-time from security sources, updated throughout the day.")
pdf.ln(2)

pdf.section_title("Q: Can I report a bug or suggest features?")
pdf.body_text("A: Yes. Look for the feedback option in settings or contact developers through GitHub.")
pdf.ln(2)

# ===== GETTING HELP =====
pdf.chapter_title("10. GETTING HELP")

pdf.section_title("Resources")
pdf.bullet_point("In-app Help: Hover over icons for tooltips and descriptions")
pdf.bullet_point("This Guide: Keep this PDF handy for reference")
pdf.bullet_point("Security News: Read latest threats and best practices")
pdf.bullet_point("Glossary: Look up unfamiliar security terms")
pdf.bullet_point("Quizzes: Test understanding of concepts")
pdf.ln(2)

pdf.section_title("Contact & Support")
pdf.bullet_point("GitHub Issues: Report bugs or request features")
pdf.bullet_point("Documentation: Read API docs for technical questions")
pdf.ln(3)

pdf.set_font("Arial", "I", 9)
pdf.cell(0, 10, "Thank you for using Security Assistant!", align="C")

# Save PDF
output_path = r"c:\Users\sivas\OneDrive\Desktop\security_assistant\Security_Assistant_User_Guide.pdf"
pdf.output(output_path)
print("User Guide generated successfully!")
print("Location: " + output_path)
