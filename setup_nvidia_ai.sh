#!/bin/bash

################################################################################
# Security Assistant - NVIDIA AI Integration Setup Script
# =========================================================
# This script automates the setup of NVIDIA AI integration for the backend.
# 
# Usage:
#   chmod +x setup_nvidia_ai.sh
#   ./setup_nvidia_ai.sh
#
# Prerequisites:
#   - Python 3.8+
#   - pip
#   - Git (optional)
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║  Security Assistant - NVIDIA AI Integration Setup                  ║"
echo "║  Version 1.0                                                       ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ============================================================================
# Step 1: Check Prerequisites
# ============================================================================

echo -e "\n${YELLOW}Step 1: Checking Prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}✗ pip not found. Please install pip.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ pip found${NC}"

# ============================================================================
# Step 2: Create Virtual Environment (Optional)
# ============================================================================

echo -e "\n${YELLOW}Step 2: Virtual Environment Setup${NC}"

read -p "Create a Python virtual environment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ ! -d "$PROJECT_ROOT/venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv "$PROJECT_ROOT/venv"
        echo -e "${GREEN}✓ Virtual environment created${NC}"
    else
        echo -e "${YELLOW}Virtual environment already exists${NC}"
    fi
    
    # Activate virtual environment
    source "$PROJECT_ROOT/venv/bin/activate"
    echo -e "${GREEN}✓ Virtual environment activated${NC}"
fi

# ============================================================================
# Step 3: Install Dependencies
# ============================================================================

echo -e "\n${YELLOW}Step 3: Installing Dependencies...${NC}"

cd "$SCRIPT_DIR"

if [ -f "requirements.txt" ]; then
    echo "Installing packages from requirements.txt..."
    pip3 install -q -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}✗ requirements.txt not found${NC}"
    exit 1
fi

# ============================================================================
# Step 4: Check .env File
# ============================================================================

echo -e "\n${YELLOW}Step 4: Environment Configuration${NC}"

ENV_FILE="$PROJECT_ROOT/.env"
ENV_EXAMPLE="$PROJECT_ROOT/.env.example"

if [ ! -f "$ENV_FILE" ]; then
    if [ -f "$ENV_EXAMPLE" ]; then
        echo "Creating .env from template..."
        cp "$ENV_EXAMPLE" "$ENV_FILE"
        echo -e "${GREEN}✓ .env created from .env.example${NC}"
    else
        echo -e "${YELLOW}⚠ Neither .env nor .env.example found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

# Check if API key is configured
if grep -q "nvapi-your-api-key-here" "$ENV_FILE"; then
    echo -e "${YELLOW}⚠ NVIDIA API key not configured${NC}"
    echo ""
    echo "To get an API key:"
    echo "  1. Visit https://build.nvidia.com"
    echo "  2. Sign in with your NVIDIA account"
    echo "  3. Go to API Keys section"
    echo "  4. Generate a new key"
    echo "  5. Copy the key (format: nvapi-xxxx...)"
    echo ""
    read -p "Enter your NVIDIA API key (or skip to continue): " API_KEY
    
    if [ ! -z "$API_KEY" ]; then
        if [[ $API_KEY == nvapi-* ]]; then
            sed -i.bak "s/nvapi-your-api-key-here/$API_KEY/" "$ENV_FILE"
            echo -e "${GREEN}✓ API key configured${NC}"
        else
            echo -e "${RED}✗ Invalid API key format (must start with nvapi-)${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ Skipping API key configuration${NC}"
    fi
else
    echo -e "${GREEN}✓ NVIDIA API key configured${NC}"
fi

# ============================================================================
# Step 5: Verify Installation
# ============================================================================

echo -e "\n${YELLOW}Step 5: Verifying Installation...${NC}"

# Check Python packages
python3 -c "import openai; print(f'OpenAI SDK version: {openai.__version__}')" 2>/dev/null && \
    echo -e "${GREEN}✓ OpenAI SDK installed${NC}" || \
    echo -e "${YELLOW}⚠ OpenAI SDK check failed${NC}"

python3 -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')" 2>/dev/null && \
    echo -e "${GREEN}✓ FastAPI installed${NC}" || \
    echo -e "${YELLOW}⚠ FastAPI check failed${NC}"

python3 -c "import pydantic; print(f'Pydantic version: {pydantic.__version__}')" 2>/dev/null && \
    echo -e "${GREEN}✓ Pydantic installed${NC}" || \
    echo -e "${YELLOW}⚠ Pydantic check failed${NC}"

python3 -c "import dotenv; print('python-dotenv installed')" 2>/dev/null && \
    echo -e "${GREEN}✓ python-dotenv installed${NC}" || \
    echo -e "${YELLOW}⚠ python-dotenv check failed${NC}"

# Check NVIDIA integration files
echo -n "Checking NVIDIA integration files..."

[ -f "nvidia_ai_integration.py" ] && echo -n "." || echo -n "✗"
[ -f "ai_services.py" ] && echo -n "." || echo -n "✗"
[ -f "routes_nvidia_ai.py" ] && echo "." || echo "✗"

if [ -f "nvidia_ai_integration.py" ] && [ -f "ai_services.py" ] && [ -f "routes_nvidia_ai.py" ]; then
    echo -e "${GREEN}✓ All NVIDIA integration files present${NC}"
else
    echo -e "${RED}✗ Some integration files missing${NC}"
fi

# ============================================================================
# Step 6: Display Configuration
# ============================================================================

echo -e "\n${YELLOW}Step 6: Configuration Summary${NC}"

echo ""
echo "Environment Configuration:"
echo "  .env file: $ENV_FILE"
echo ""
echo "Backend Files:"
echo "  - nvidia_ai_integration.py (NVIDIA AI Client)"
echo "  - ai_services.py (Service Layer)"
echo "  - routes_nvidia_ai.py (API Endpoints)"
echo ""
echo "Frontend Files should be copied to frontend/ directory:"
echo "  - nvaidaService.js"
echo "  - IntegrationExamples.jsx"
echo ""
echo "Documentation:"
echo "  - NVIDIA_SETUP_GUIDE.md"
echo "  - FRONTEND_INTEGRATION_GUIDE.md"
echo "  - NVIDIA_QUICK_REFERENCE.md"
echo "  - NVIDIA_IMPLEMENTATION_COMPLETE.md"

# ============================================================================
# Step 7: Test Configuration
# ============================================================================

echo -e "\n${YELLOW}Step 7: Testing Configuration${NC}"

# Test if we can import the modules
echo "Testing Python imports..."

python3 << 'EOF'
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path.cwd()
sys.path.insert(0, str(backend_path))

try:
    # Test imports
    import nvidia_ai_integration
    print("✓ nvidia_ai_integration imported successfully")
except Exception as e:
    print(f"✗ Failed to import nvidia_ai_integration: {e}")
    sys.exit(1)

try:
    import ai_services
    print("✓ ai_services imported successfully")
except Exception as e:
    print(f"✗ Failed to import ai_services: {e}")
    sys.exit(1)

try:
    import routes_nvidia_ai
    print("✓ routes_nvidia_ai imported successfully")
except Exception as e:
    print(f"✗ Failed to import routes_nvidia_ai: {e}")
    sys.exit(1)

# Check API key
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('NVIDIA_API_KEY')
if api_key and api_key.startswith('nvapi-'):
    print("✓ NVIDIA API key is configured")
else:
    print("⚠ NVIDIA API key not configured or invalid")
    sys.exit(1)

print("\nAll imports successful!")
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All imports successful${NC}"
else
    echo -e "${RED}✗ Import test failed${NC}"
    exit 1
fi

# ============================================================================
# Step 8: Next Steps
# ============================================================================

echo -e "\n${GREEN}"
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║  Setup Complete!                                                   ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "\n${BLUE}Next Steps:${NC}"
echo ""
echo "1. Update main.py to include NVIDIA routes:"
echo "   from routes_nvidia_ai import router as nvidia_router"
echo "   app.include_router(nvidia_router)"
echo ""
echo "2. Start the backend server:"
echo "   uvicorn main:app --reload --port 8000"
echo ""
echo "3. Test an endpoint:"
echo "   curl -X POST http://localhost:8000/api/security/nvidia/health"
echo ""
echo "4. Integrate frontend files:"
echo "   - Copy nvaidaService.js to frontend/"
echo "   - Copy IntegrationExamples.jsx to frontend/"
echo ""
echo "5. Update React components to use aiService"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "  - Setup details: See NVIDIA_SETUP_GUIDE.md"
echo "  - Frontend integration: See FRONTEND_INTEGRATION_GUIDE.md"
echo "  - Quick reference: See NVIDIA_QUICK_REFERENCE.md"
echo ""
echo -e "${BLUE}Helpful Commands:${NC}"
echo "  uvicorn main:app --reload           # Start backend"
echo "  pip install -r requirements.txt     # Install dependencies"
echo "  python main.py                      # Or run main.py directly"
echo ""

# ============================================================================
# Final Confirmation
# ============================================================================

read -p "Would you like to start the backend server now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Starting backend server...${NC}"
    echo "Press Ctrl+C to stop the server"
    echo ""
    uvicorn main:app --reload --port 8000
else
    echo -e "${GREEN}Setup complete! Run 'uvicorn main:app --reload --port 8000' to start the server.${NC}"
fi
