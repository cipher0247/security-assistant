#!/usr/bin/env python3
"""Generate a comprehensive PDF report of the Security Assistant project."""

from datetime import datetime
try:
    from fpdf import FPDF
except ImportError:
    print("Installing fpdf2...")
    import subprocess
    subprocess.run(["pip", "install", "fpdf2"], check=True)
    from fpdf import FPDF

class ProjectReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 20)
        self.cell(0, 10, "Security Assistant", ln=True, align="C")
        self.set_font("Arial", "I", 10)
        self.cell(0, 5, "Project Analysis Report", ln=True, align="C")
        self.set_font("Arial", "", 9)
        now = datetime.now().strftime('%B %d, %Y')
        self.cell(0, 5, "Generated: " + now, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Page " + str(self.page_no()), align="C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 14)
        self.set_fill_color(52, 73, 94)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, title, ln=True, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 5, text)
        self.ln(4)

    def section_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_text_color(52, 73, 94)
        self.cell(0, 8, title, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def bullet_point(self, text):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 5, "+ " + text)

    def add_table_header(self, headers, col_widths):
        self.set_font("Arial", "B", 10)
        self.set_fill_color(52, 73, 94)
        self.set_text_color(255, 255, 255)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 7, header, border=1, fill=True)
        self.ln()
        self.set_text_color(0, 0, 0)

    def add_table_row(self, items, col_widths):
        self.set_font("Arial", "", 9)
        for i, item in enumerate(items):
            self.cell(col_widths[i], 6, str(item), border=1)
        self.ln()

    def add_feature_list(self, items):
        self.set_font("Arial", "", 10)
        for item in items:
            self.bullet_point(item)

# Create PDF
pdf = ProjectReport()
pdf.add_page()

# 1. Executive Summary
pdf.chapter_title("1. Executive Summary")
pdf.chapter_body(
    "Security Assistant is a comprehensive web-based security analysis and education platform. "
    "It provides passive security scanning capabilities, risk assessment tools, and educational resources "
    "for learning cybersecurity concepts. The application features a FastAPI backend with a responsive Tailwind CSS frontend, "
    "designed for easy deployment on Render PaaS."
)

# 2. Project Overview
pdf.chapter_title("2. Project Overview")
pdf.section_title("Purpose")
pdf.chapter_body(
    "Provide passive security analysis, risk assessment, and comprehensive cybersecurity education "
    "through an intuitive web interface without requiring active exploitation or external API dependencies."
)

pdf.section_title("Technology Stack")
pdf.section_title("Backend:")
pdf.add_feature_list([
    "FastAPI 0.109+ - Modern, fast web framework",
    "Uvicorn - ASGI server",
    "Python 3.10+ - Primary language",
    "Pydantic - Data validation",
    "Requests - HTTP client library"
])

pdf.section_title("Frontend:")
pdf.add_feature_list([
    "HTML5 / Vanilla JavaScript",
    "Tailwind CSS - Utility-first styling",
    "jsPDF - Client-side PDF generation"
])

pdf.section_title("Deployment:")
pdf.bullet_point("Render.com - PaaS hosting")
pdf.ln(2)

# 3. Architecture
pdf.chapter_title("3. Architecture Overview")
pdf.section_title("Directory Structure")

files_structure = """security_assistant/
backend/
  main.py (FastAPI app + endpoints)
  risk_engine.py (Risk scoring algorithms)
  requirements.txt (Python dependencies)
  scanners/ (Security analysis modules)
    file_scan.py
    url_scan.py
    phishing_detector.py
    password_strength.py
    sqli_signals.py, xss_signals.py
  utils/ (Utility modules)
    hash_tool.py
    education_data.py
    tools_extended.py
    personal_security.py
frontend/
  index.html (Main UI)
  app.js (Core logic)
  personal_security.js
tests/ (Endpoint verification)
render.yaml (Deployment config)"""

pdf.chapter_body(files_structure)

# 4. Core Features
pdf.chapter_title("4. Core Features & Capabilities")

pdf.section_title("Security Scanning Modules")
pdf.add_feature_list([
    "File Scanner - Analyzes files for suspicious patterns, entropy calculation, dangerous extensions",
    "URL Scanner - HTTPS verification, security headers, SQL injection detection, XSS analysis",
    "Phishing Detector - ML-based detection for phishing URLs and emails",
    "Password Strength Checker - Evaluates passwords with offline/online/supercomputer attack modes",
    "Risk Engine - Calculates overall risk scores (LOW/MEDIUM/HIGH)"
])

pdf.section_title("Security Tools")
pdf.add_feature_list([
    "Password Generator - Creates secure passwords with customizable complexity",
    "Hash Calculator - MD5, SHA256, and multiple hash algorithm support",
    "EXIF Metadata Viewer - Extracts metadata from image files",
    "Steganography Tool - Hide and extract data in files",
    "News Fetcher - Real-time security news aggregation"
])

pdf.section_title("Educational Resources")
pdf.add_feature_list([
    "Interactive Security Quizzes - 5-question random quizzes for learning",
    "Security Glossary - Comprehensive terminology reference",
    "Career Guides - Guidance for cybersecurity career paths",
    "Cheat Sheets - Quick reference materials for security concepts"
])

# 5. API Endpoints
pdf.chapter_title("5. API Endpoints Reference")

pdf.set_font("Arial", "", 9)
endpoints = [
    ["Password Analysis", "POST /api/tools/password", "Check password strength"],
    ["Hash Calculation", "POST /api/tools/hash", "Compute hash values"],
    ["File Scanning", "POST /api/tools/file", "Scan file for threats"],
    ["URL Analysis", "POST /api/tools/url", "Analyze URL security"],
    ["Phishing URL", "POST /api/tools/phishing/url", "Detect phishing URLs"],
    ["Phishing Email", "POST /api/tools/phishing/email", "Detect phishing emails"],
    ["Password Gen", "POST /api/tools/password/generate", "Generate secure password"],
    ["Glossary", "GET /api/education/glossary", "Security terminology"],
    ["Quiz", "GET /api/education/quiz", "Random quiz questions"],
    ["Career Guide", "GET /api/education/career", "Career path information"],
    ["Cheat Sheets", "GET /api/education/cheatsheets", "Quick references"],
    ["Latest News", "GET /api/news", "Security news updates"],
    ["EXIF Data", "POST /api/tools/exif", "Extract image metadata"],
]

pdf.add_table_header(["Feature", "Endpoint", "Description"], [50, 55, 85])
for endpoint in endpoints:
    pdf.add_table_row(endpoint, [50, 55, 85])

# 6. Risk Assessment Engine
pdf.chapter_title("6. Risk Assessment Engine")

pdf.section_title("File Risk Scoring")
pdf.chapter_body(
    "File risk is calculated based on entropy levels and file extension analysis:"
)
pdf.add_feature_list([
    "Suspicious Extension Detection - Adds 4 points to risk score",
    "Entropy Analysis - Entropy > 7.0 adds 3 points",
    "Risk Classification - HIGH (5+), MEDIUM (3+), LOW (0-2)"
])

pdf.section_title("URL Risk Scoring")
pdf.chapter_body(
    "URL risk evaluation considers multiple security factors:"
)
pdf.add_feature_list([
    "HTTPS Verification - Missing HTTPS adds 4 points",
    "Security Headers - 3+ missing headers add 2 points",
    "SQL Injection Risk - HIGH (5pts), MEDIUM (3pts), LOW (1pt)",
    "XSS Vulnerability Risk - HIGH (5pts), MEDIUM/LOW scaled scoring",
    "Server Leaks & Cookie Issues - Each adds to overall risk"
])

# 7. Key Strengths
pdf.chapter_title("7. Key Strengths")
pdf.add_feature_list([
    "Passive Analysis - No active exploitation or intrusive testing",
    "No External Dependencies - Self-contained, doesn't rely on third-party APIs",
    "Educational Focus - Built-in learning resources and explanations",
    "Modern Tech Stack - FastAPI provides high performance and automatic documentation",
    "Client-Side Security - Cryptographic operations perform on user's machine",
    "Easy Deployment - Render.yaml for one-click deployment",
    "Comprehensive Coverage - File, URL, email, password, and metadata analysis",
    "Risk Scoring - Heuristic-based risk assessment for actionable insights"
])

# 8. Potential Enhancements
pdf.chapter_title("8. Potential Enhancements")
pdf.add_feature_list([
    "VirusTotal API Integration - Leverage community threat intelligence",
    "Machine Learning Models - Advanced phishing detection with real datasets",
    "Database Integration - Store scan history and user preferences",
    "Two-Factor Authentication - User account security",
    "Advanced Reporting - Detailed threat analysis reports",
    "Real-time Threat Feeds - Integration with security intelligence sources",
    "Browser Extension - Analyze URLs directly from the browser",
    "API Rate Limiting - Prevent abuse and ensure fair usage"
])

# 9. Deployment
pdf.chapter_title("9. Deployment Configuration")

deployment_info = """Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT
Environment: Python
Plan: Free (Render.com)
Service Name: security-assistant-web"""

pdf.chapter_body(deployment_info)

pdf.section_title("Getting Started Locally")
pdf.add_feature_list([
    "Install dependencies: pip install -r backend/requirements.txt",
    "Run API: python -m uvicorn backend.main:app --reload",
    "Open frontend: Open frontend/index.html in browser or serve with HTTP server",
    "Test endpoints: Refer to tests/ directory for verification scripts"
])

# 10. Security Considerations
pdf.chapter_title("10. Security Considerations")
pdf.add_feature_list([
    "CORS Enabled - Configure allowed origins for production",
    "Input Validation - Pydantic models enforce strict data validation",
    "File Upload Handling - Temporary file storage for uploaded files",
    "No User Data Storage - Stateless operation preserves privacy",
    "Information Disclosure - Avoid exposing sensitive error details in production"
])

# 11. Dependencies Summary
pdf.chapter_title("11. Dependencies Summary")
dependencies = [
    ["fastapi", "Web framework"],
    ["uvicorn", "ASGI server"],
    ["python-multipart", "Form data handling"],
    ["pydantic", "Data validation"],
    ["requests", "HTTP client"],
    ["Pillow", "Image processing"],
    ["feedparser", "RSS/Atom parsing"],
    ["opencv-python-headless", "Image analysis"],
]

pdf.add_table_header(["Package", "Purpose"], [90, 100])
for dep in dependencies:
    pdf.add_table_row(dep, [90, 100])

# 12. Conclusion
pdf.chapter_title("12. Conclusion")
pdf.chapter_body(
    "Security Assistant is a well-structured, feature-rich security education and analysis platform. "
    "It successfully combines practical security scanning capabilities with comprehensive educational resources. "
    "The project demonstrates good software engineering practices with modular design, clear separation of concerns, "
    "and straightforward deployment. With potential enhancements in ML integration and external threat intelligence, "
    "this platform could serve as an excellent resource for security professionals and students alike."
)

pdf.ln(10)
pdf.set_font("Arial", "I", 9)
pdf.cell(0, 10, "End of Report", align="C")

# Save PDF
output_path = r"c:\Users\sivas\OneDrive\Desktop\security_assistant\Security_Assistant_Report.pdf"
pdf.output(output_path)
print("PDF Report generated successfully!")
print("Location: " + output_path)
