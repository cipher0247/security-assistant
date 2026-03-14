@echo off
REM Quick Start Script for Security Assistant Platform (Windows)
REM This script helps you set up the development environment quickly

setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════
echo 🛡️  Security Assistant Platform - Quick Start Setup (Windows)
echo ════════════════════════════════════════════════════════════
echo.

REM Check prerequisites
echo 🔍 Checking prerequisites...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python 3.9+ not found. Please install Python from python.org
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% found

REM Check Node
node --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Node.js 18+ not found. Please install Node.js from nodejs.org
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo ✓ Node.js %NODE_VERSION% found

REM Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo ✗ npm not found. Please install npm
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('npm --version') do set NPM_VERSION=%%i
echo ✓ npm %NPM_VERSION% found

REM Check Docker (optional)
docker --version >nul 2>&1
if errorlevel 1 (
    echo - Docker not found ^(optional for containerization^)
) else (
    for /f "tokens=*" %%i in ('docker --version') do set DOCKER_VERSION=%%i
    echo ✓ %DOCKER_VERSION% found
)
echo.

REM Setup Backend
echo 🔧 Setting up backend environment...
cd backend

if not exist "venv" (
    echo   Creating Python virtual environment...
    python -m venv venv
    echo   ✓ Virtual environment created
)

echo   Activating virtual environment...
call venv\Scripts\activate.bat
echo   ✓ Virtual environment activated

echo   Upgrading pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
echo   ✓ pip upgraded

echo   Installing Python dependencies ^(this may take a minute^)...
if exist "requirements.txt" (
    pip install -r requirements.txt >nul 2>&1
    echo   ✓ Dependencies installed
) else (
    echo   ✗ requirements.txt not found
)

REM Create .env file if not exists
if not exist ".env" (
    echo   Creating .env file...
    (
        echo # FastAPI Configuration
        echo ENVIRONMENT=development
        echo DEBUG=True
        echo LOG_LEVEL=INFO
        echo.
        echo # Database Configuration
        echo DATABASE_URL=postgresql://user:password@localhost:5432/security_assistant
        echo.
        echo # Redis Configuration
        echo REDIS_URL=redis://localhost:6379/0
        echo.
        echo # API Configuration
        echo API_HOST=0.0.0.0
        echo API_PORT=8000
        echo.
        echo # LLM Configuration ^(optional - uses fallback if not set^)
        echo # OPENAI_API_KEY=sk-...
        echo # ANTHROPIC_API_KEY=sk-ant-...
        echo LLM_PROVIDER=fallback
        echo.
        echo # Security
        echo SECRET_KEY=your-secret-key-here-minimum-32-characters
        echo ALGORITHM=HS256
    ) > .env
    echo   ✓ .env file created
    echo   → Update .env with your actual configuration
)

cd ..
echo.

REM Setup Frontend
echo 🎨 Setting up frontend environment...
cd frontend

echo   Installing npm dependencies ^(this may take a minute^)...
call npm install >nul 2>&1
echo   ✓ npm dependencies installed

REM Create .env file if not exists
if not exist ".env" (
    echo   Creating .env file...
    (
        echo # API Configuration
        echo REACT_APP_API_URL=http://localhost:8000/api
        echo REACT_APP_API_TIMEOUT=30000
        echo.
        echo # Feature Flags
        echo REACT_APP_ENABLE_LABS=true
        echo REACT_APP_ENABLE_SOCIAL=true
    ) > .env
    echo   ✓ .env file created
)

cd ..
echo.

REM Ask about Docker
set /p DOCKER_SETUP="Do you want to set up Docker? (y/n): "
if /i "%DOCKER_SETUP%"=="y" (
    docker --version >nul 2>&1
    if errorlevel 1 (
        echo ✗ Docker not installed. Please install Docker Desktop for Windows
    ) else (
        echo 🐳 Building Docker images...
        docker build -t security-backend:dev -f backend/Dockerfile ./backend
        echo ✓ Backend image built
        docker build -t security-frontend:dev -f frontend/Dockerfile ./frontend
        echo ✓ Frontend image built
    )
)
echo.

REM Print next steps
echo.
echo ════════════════════════════════════════════════════════════
echo 🎉 Setup Complete!
echo ════════════════════════════════════════════════════════════
echo.
echo Next Steps:
echo.
echo 1. 📖 Read Documentation:
echo    - README_UPGRADE.md ^(overview^)
echo    - ARCHITECTURE.md ^(system design^)
echo    - IMPLEMENTATION_GUIDE.md ^(how to build^)
echo.
echo 2. 🗄️ Setup Database ^(if using PostgreSQL^):
echo    docker run -d -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:15
echo    ^(Update DATABASE_URL in backend\.env^)
echo.
echo 3. 🔴 Setup Redis ^(if using caching^):
echo    docker run -d -p 6379:6379 redis:7-alpine
echo.
echo 4. 🚀 Start Backend Development Server:
echo    cd backend
echo    venv\Scripts\activate.bat
echo    uvicorn app.main:app --reload
echo    ^(API will be at http://localhost:8000^)
echo.
echo 5. ⚛️  Start Frontend Development Server ^(in new terminal^):
echo    cd frontend
echo    npm start
echo    ^(React app will be at http://localhost:3000^)
echo.
echo 6. 🧪 Run Tests:
echo    cd backend
echo    pytest tests/ --cov=.
echo.
echo 7. 🐳 Or use Docker Compose ^(all-in-one^):
echo    docker-compose up -d
echo.
echo Key Files:
echo   ✓ backend\llm_engine.py - AI integration ^(800+ lines^)
echo   ✓ frontend\src\App.jsx - React app shell ^(250+ lines^)
echo   ✓ backend\requirements.txt - Python dependencies
echo   ✓ frontend\package.json - Node dependencies
echo.
echo Important URLs:
echo   - API Docs: http://localhost:8000/docs
echo   - Frontend: http://localhost:3000
echo.
echo ════════════════════════════════════════════════════════════
echo.

pause
