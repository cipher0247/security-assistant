from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import os

from scanners.file_scan import FileScanner
from scanners.url_scan import UrlScanner
from risk_engine import RiskEngine
from scanners.password_strength import PasswordStrengthChecker
from scanners.phishing_detector import PhishingDetector
from utils.hash_tool import HashCalculator
from utils.education_data import glossary_data
from utils.student_data import get_random_quiz, career_guide, cheat_sheets
from utils.tools_extended import PasswordGenerator, SteganographyTool, ExifViewer, NewsFetcher
from fastapi.responses import StreamingResponse
from io import BytesIO

app = FastAPI(
    title="Security Assistant API",
    description="Passive security analysis, risk assessment, and educational tools",
    version="1.2.0"
)

# ... (middle parts unchanged)

password_checker = PasswordStrengthChecker()
phishing_detector = PhishingDetector()

class PasswordRequest(BaseModel):
    password: str
    attack_mode: str = "offline" # online, offline
    hardware: str = "gpu" # cpu, gpu, supercomputer
    hash_type: str = "md5" # md5, sha256, bcrypt

class HashRequest(BaseModel):
    text: str

class EmailScanRequest(BaseModel):
    subject: str
    body: str

class UrlScanRequest(BaseModel):
    url: str

class PasswordGenRequest(BaseModel):
    length: int = 16
    use_symbols: bool = True
    use_numbers: bool = True
    use_upper: bool = True

class StegoRequest(BaseModel):
    text: str

# ... (existing endpoints)

@app.post("/api/tools/phishing/url")
async def scan_phishing_url(request: UrlScanRequest):
    return phishing_detector.scan_url_ml(request.url)

@app.post("/api/tools/phishing/email")
async def scan_phishing_email(request: EmailScanRequest):
    return phishing_detector.scan_email(request.subject, request.body)

@app.get("/api/education/quiz")
async def get_quiz():
    return get_random_quiz(5)

@app.get("/api/education/career")
async def get_career():
    return career_guide

@app.get("/api/education/cheatsheets")
async def get_cheatsheets():
    return cheat_sheets

@app.get("/api/news")
async def get_news():
    return NewsFetcher.get_latest_news()

@app.post("/api/tools/password/generate")
async def generate_password(request: PasswordGenRequest):
    pwd = PasswordGenerator.generate(
        length=request.length,
        use_symbols=request.use_symbols,
        use_numbers=request.use_numbers,
        use_upper=request.use_upper
    )
    # Also check strength of generated
    strength = password_checker.check_strength(pwd)
    return {"password": pwd, "strength": strength}

@app.post("/api/tools/exif")
async def extract_exif(file: UploadFile = File(...)):
    content = await file.read()
    return ExifViewer.get_metadata(content)

@app.post("/api/tools/stego/hide")
async def hide_stego(file: UploadFile = File(...), text: str = ""):
    content = await file.read()
    try:
        new_img_bytes = SteganographyTool.hide_text(content, text)
        return StreamingResponse(BytesIO(new_img_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/tools/stego/extract")
async def extract_stego(file: UploadFile = File(...)):
    content = await file.read()
    try:
        text = SteganographyTool.extract_text(content)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ... (existing endpoints)

@app.post("/api/tools/password")
async def check_password(request: PasswordRequest):
    return password_checker.check_strength(
        request.password, 
        attack_mode=request.attack_mode,
        hardware=request.hardware,
        hash_type=request.hash_type
    )

@app.post("/api/tools/hash")
async def calc_hash(request: HashRequest):
    return HashCalculator.calculate_hashes(request.text)

@app.get("/api/education/glossary")
async def get_glossary():
    return glossary_data

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "*" # Allow all for local file usage if needed, but not necessary with static mount
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Frontend (Static)
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="frontend")

file_scanner = FileScanner()
url_scanner = UrlScanner()


from fastapi.responses import RedirectResponse

@app.get("/")
async def root():
    return RedirectResponse(url="/app")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/scan/file")
async def scan_file(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    content = await file.read()
    scan_result = await file_scanner.scan_file(content, file.filename)
    risk_level = RiskEngine.calculate_file_risk(scan_result)
    scan_result['risk_level'] = risk_level
    
    return scan_result

@app.post("/api/scan/url")
async def scan_url(request: UrlScanRequest):
    scan_result = url_scanner.scan_url(request.url)
    risk_level = RiskEngine.calculate_url_risk(scan_result)
    scan_result['risk_level'] = risk_level
    
    return scan_result
