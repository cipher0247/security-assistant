@echo off
REM ==============================================================================
REM Security Assistant - NVIDIA AI Integration Setup Script (Windows)
REM ==============================================================================
REM This script automates the setup of NVIDIA AI integration for the backend.
REM
REM Usage:
REM   setup_nvidia_ai.bat
REM
REM Prerequisites:
REM   - Python 3.8+
REM   - pip
REM ==============================================================================

setlocal enabledelayedexpansion

REM Colors (Windows 10+ Terminal)
set GREEN=[92m
set YELLOW=[93m
set RED=[91m
set BLUE=[94m
set RESET=[0m

echo %BLUE%
echo ==============================================================================
echo   Security Assistant - NVIDIA AI Integration Setup
echo   Version 1.0
echo ==============================================================================
echo %RESET%

REM ==============================================================================
REM Step 1: Check Prerequisites
REM ==============================================================================

echo.
echo %YELLOW%Step 1: Checking Prerequisites...%RESET%

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%× Python not found. Please install Python 3.8 or higher.%RESET%
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo %GREEN%✓ Python %PYTHON_VERSION% found%RESET%

REM Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo %RED%× pip not found. Please install pip.%RESET%
    pause
    exit /b 1
)

echo %GREEN%✓ pip found%RESET%

REM ==============================================================================
REM Step 2: Create Virtual Environment (Optional)
REM ==============================================================================

echo.
echo %YELLOW%Step 2: Virtual Environment Setup%RESET%

set /p CREATE_VENV="Create a Python virtual environment? (y/n): "

if /i "%CREATE_VENV%"=="y" (
    if not exist "venv\" (
        echo Creating virtual environment...
        python -m venv venv
        echo %GREEN%✓ Virtual environment created%RESET%
    ) else (
        echo %YELLOW%Virtual environment already exists%RESET%
    )
    
    REM Activate virtual environment
    call venv\Scripts\activate.bat
    echo %GREEN%✓ Virtual environment activated%RESET%
)

REM ==============================================================================
REM Step 3: Install Dependencies
REM ==============================================================================

echo.
echo %YELLOW%Step 3: Installing Dependencies...%RESET%

if exist "requirements.txt" (
    echo Installing packages from requirements.txt...
    pip install -q -r requirements.txt
    if errorlevel 0 (
        echo %GREEN%✓ Dependencies installed%RESET%
    ) else (
        echo %YELLOW%⚠ Some packages may have failed to install%RESET%
    )
) else (
    echo %RED%× requirements.txt not found%RESET%
    pause
    exit /b 1
)

REM ==============================================================================
REM Step 4: Environment Configuration
REM ==============================================================================

echo.
echo %YELLOW%Step 4: Environment Configuration%RESET%

if not exist ".env" (
    if exist ".env.example" (
        echo Creating .env from template...
        copy ".env.example" ".env" >nul
        echo %GREEN%✓ .env created from .env.example%RESET%
    ) else (
        echo %YELLOW%⚠ Neither .env nor .env.example found%RESET%
        pause
        exit /b 1
    )
) else (
    echo %GREEN%✓ .env file exists%RESET%
)

REM Check if API key is configured
findstr /M "nvapi-your-api-key-here" ".env" >nul
if errorlevel 0 (
    echo %YELLOW%⚠ NVIDIA API key not configured%RESET%
    echo.
    echo To get an API key:
    echo   1. Visit https://build.nvidia.com
    echo   2. Sign in with your NVIDIA account
    echo   3. Go to API Keys section
    echo   4. Generate a new key
    echo   5. Copy the key (format: nvapi-xxxx...)
    echo.
    
    set /p API_KEY="Enter your NVIDIA API key (or press Enter to skip): "
    
    if not "!API_KEY!"=="" (
        REM Simple validation - check if it starts with nvapi-
        if "!API_KEY:~0,6!"=="nvapi-" (
            REM Replace in .env file using PowerShell
            powershell -Command "(Get-Content '.env') -replace 'nvapi-your-api-key-here', '!API_KEY!' | Set-Content '.env'"
            echo %GREEN%✓ API key configured%RESET%
        ) else (
            echo %RED%× Invalid API key format (must start with nvapi-)%RESET%
        )
    ) else (
        echo %YELLOW%⚠ Skipping API key configuration%RESET%
    )
) else (
    echo %GREEN%✓ NVIDIA API key configured%RESET%
)

REM ==============================================================================
REM Step 5: Verify Installation
REM ==============================================================================

echo.
echo %YELLOW%Step 5: Verifying Installation...%RESET%

REM Check Python packages
python -c "import openai; print(f'OpenAI SDK version: {openai.__version__}')" >nul 2>&1
if errorlevel 0 (
    echo %GREEN%✓ OpenAI SDK installed%RESET%
) else (
    echo %YELLOW%⚠ OpenAI SDK check failed%RESET%
)

python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')" >nul 2>&1
if errorlevel 0 (
    echo %GREEN%✓ FastAPI installed%RESET%
) else (
    echo %YELLOW%⚠ FastAPI check failed%RESET%
)

python -c "import pydantic; print(f'Pydantic version: {pydantic.__version__}')" >nul 2>&1
if errorlevel 0 (
    echo %GREEN%✓ Pydantic installed%RESET%
) else (
    echo %YELLOW%⚠ Pydantic check failed%RESET%
)

python -c "import dotenv; print('python-dotenv installed')" >nul 2>&1
if errorlevel 0 (
    echo %GREEN%✓ python-dotenv installed%RESET%
) else (
    echo %YELLOW%⚠ python-dotenv check failed%RESET%
)

REM Check NVIDIA integration files
echo Checking NVIDIA integration files...
set FILES_OK=1

if not exist "nvidia_ai_integration.py" (
    set FILES_OK=0
)
if not exist "ai_services.py" (
    set FILES_OK=0
)
if not exist "routes_nvidia_ai.py" (
    set FILES_OK=0
)

if %FILES_OK%==1 (
    echo %GREEN%✓ All NVIDIA integration files present%RESET%
) else (
    echo %RED%× Some integration files missing%RESET%
)

REM ==============================================================================
REM Step 6: Display Configuration
REM ==============================================================================

echo.
echo %YELLOW%Step 6: Configuration Summary%RESET%

echo.
echo Environment Configuration:
echo   .env file: .env
echo.
echo Backend Files:
echo   - nvidia_ai_integration.py (NVIDIA AI Client)
echo   - ai_services.py (Service Layer)
echo   - routes_nvidia_ai.py (API Endpoints)
echo.
echo Frontend Files should be copied to frontend\ directory:
echo   - nvaidaService.js
echo   - IntegrationExamples.jsx
echo.
echo Documentation:
echo   - NVIDIA_SETUP_GUIDE.md
echo   - FRONTEND_INTEGRATION_GUIDE.md
echo   - NVIDIA_QUICK_REFERENCE.md
echo   - NVIDIA_IMPLEMENTATION_COMPLETE.md

REM ==============================================================================
REM Step 7: Test Configuration
REM ==============================================================================

echo.
echo %YELLOW%Step 7: Testing Configuration%RESET%

echo Testing Python imports...

python << 'EOF'
import os
import sys

try:
    import nvidia_ai_integration
    print("✓ nvidia_ai_integration imported successfully")
except Exception as e:
    print(f"× Failed to import nvidia_ai_integration: {e}")
    sys.exit(1)

try:
    import ai_services
    print("✓ ai_services imported successfully")
except Exception as e:
    print(f"× Failed to import ai_services: {e}")
    sys.exit(1)

try:
    import routes_nvidia_ai
    print("✓ routes_nvidia_ai imported successfully")
except Exception as e:
    print(f"× Failed to import routes_nvidia_ai: {e}")
    sys.exit(1)

# Check API key
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('NVIDIA_API_KEY')
if api_key and api_key.startswith('nvapi-'):
    print("✓ NVIDIA API key is configured")
else:
    print("⚠ NVIDIA API key not configured or invalid")

print("\nAll imports successful!")
EOF

echo %GREEN%✓ Configuration test complete%RESET%

REM ==============================================================================
REM Step 8: Next Steps
REM ==============================================================================

echo.
echo %GREEN%
echo ==============================================================================
echo   Setup Complete!
echo ==============================================================================
echo %RESET%

echo.
echo %BLUE%Next Steps:%RESET%
echo.
echo 1. Update main.py to include NVIDIA routes:
echo    from routes_nvidia_ai import router as nvidia_router
echo    app.include_router(nvidia_router)
echo.
echo 2. Start the backend server:
echo    uvicorn main:app --reload --port 8000
echo.
echo 3. Test an endpoint:
echo    curl -X POST http://localhost:8000/api/security/nvidia/health
echo.
echo 4. Integrate frontend files:
echo    - Copy nvaidaService.js to frontend\
echo    - Copy IntegrationExamples.jsx to frontend\
echo.
echo 5. Update React components to use aiService
echo.
echo %BLUE%Documentation:%RESET%
echo   - Setup details: See NVIDIA_SETUP_GUIDE.md
echo   - Frontend integration: See FRONTEND_INTEGRATION_GUIDE.md
echo   - Quick reference: See NVIDIA_QUICK_REFERENCE.md
echo.
echo %BLUE%Helpful Commands:%RESET%
echo   uvicorn main:app --reload      - Start backend
echo   pip install -r requirements.txt - Install dependencies
echo.

pause

REM ==============================================================================
REM Final Confirmation
REM ==============================================================================

set /p START_SERVER="Would you like to start the backend server now? (y/n): "

if /i "%START_SERVER%"=="y" (
    echo %YELLOW%Starting backend server...%RESET%
    echo Press Ctrl+C to stop the server
    echo.
    uvicorn main:app --reload --port 8000
) else (
    echo %GREEN%Setup complete! Run 'uvicorn main:app --reload --port 8000' to start the server.%RESET%
    pause
)

endlocal
