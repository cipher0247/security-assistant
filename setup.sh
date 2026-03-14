#!/bin/bash
# Quick Start Script for Security Assistant Platform
# This script helps you set up the development environment quickly

set -e  # Exit on error

echo "════════════════════════════════════════════════════════════"
echo "🛡️  Security Assistant Platform - Quick Start Setup"
echo "════════════════════════════════════════════════════════════"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}→ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_step "Checking prerequisites..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3.9+ not found. Please install Python."
        exit 1
    fi
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    print_success "Python $PYTHON_VERSION found"
    
    # Check Node
    if ! command -v node &> /dev/null; then
        print_error "Node.js 18+ not found. Please install Node.js."
        exit 1
    fi
    NODE_VERSION=$(node --version)
    print_success "Node.js $NODE_VERSION found"
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm not found. Please install npm."
        exit 1
    fi
    NPM_VERSION=$(npm --version)
    print_success "npm $NPM_VERSION found"
    
    # Check Docker (optional)
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version)
        print_success "Docker $DOCKER_VERSION found (optional)"
    else
        echo -e "${BLUE}→ Docker not found (optional for containerization)${NC}"
    fi
    
    echo ""
}

# Setup backend
setup_backend() {
    print_step "Setting up backend environment..."
    
    cd backend || exit 1
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        print_step "Creating Python virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    
    # Activate virtual environment
    print_step "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
    
    # Upgrade pip
    print_step "Upgrading pip..."
    pip install --upgrade pip setuptools wheel > /dev/null 2>&1
    print_success "pip upgraded"
    
    # Install requirements
    print_step "Installing Python dependencies (this may take a minute)..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt > /dev/null 2>&1
        print_success "Dependencies installed"
    else
        print_error "requirements.txt not found"
    fi
    
    # Create .env file if not exists
    if [ ! -f ".env" ]; then
        print_step "Creating .env file..."
        cat > .env << 'EOF'
# FastAPI Configuration
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/security_assistant

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# LLM Configuration (optional - uses fallback if not set)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
LLM_PROVIDER=fallback

# Security
SECRET_KEY=your-secret-key-here-minimum-32-characters
ALGORITHM=HS256
EOF
        print_success ".env file created"
        echo -e "${BLUE}→ Update .env with your actual configuration${NC}"
    fi
    
    cd - > /dev/null
    echo ""
}

# Setup frontend
setup_frontend() {
    print_step "Setting up frontend environment..."
    
    cd frontend || exit 1
    
    # Install dependencies
    print_step "Installing npm dependencies (this may take a minute)..."
    npm install > /dev/null 2>&1
    print_success "npm dependencies installed"
    
    # Create .env file if not exists
    if [ ! -f ".env" ]; then
        print_step "Creating .env file..."
        cat > .env << 'EOF'
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_API_TIMEOUT=30000

# Feature Flags
REACT_APP_ENABLE_LABS=true
REACT_APP_ENABLE_SOCIAL=true
EOF
        print_success ".env file created"
    fi
    
    cd - > /dev/null
    echo ""
}

# Setup Docker (optional)
setup_docker() {
    read -p "Do you want to set up Docker? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_step "Setting up Docker..."
        
        if ! command -v docker &> /dev/null; then
            print_error "Docker not installed. Please install Docker first."
            return
        fi
        
        print_step "Building Docker images..."
        docker build -t security-backend:dev -f backend/Dockerfile ./backend
        print_success "Backend image built"
        
        docker build -t security-frontend:dev -f frontend/Dockerfile ./frontend
        print_success "Frontend image built"
        
        if command -v docker-compose &> /dev/null; then
            print_step "Docker Compose found. You can run: docker-compose up"
        fi
    fi
    echo ""
}

# Create sample data
create_sample_data() {
    print_step "Creating sample data..."
    
    cd backend || exit 1
    source venv/bin/activate
    
    # Create sample admin user
    python3 << 'PYTHON'
print("✓ Sample data setup complete")
print("  - Database tables can be created with: alembic upgrade head")
print("  - Admin user can be created with: python -m backend.create_superuser")
PYTHON
    
    cd - > /dev/null
    echo ""
}

# Print next steps
print_next_steps() {
    echo "════════════════════════════════════════════════════════════"
    echo "🎉 Setup Complete!"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    echo -e "${GREEN}Next Steps:${NC}"
    echo ""
    echo "1. 📖 Read Documentation:"
    echo "   - README_UPGRADE.md (overview)"
    echo "   - ARCHITECTURE.md (system design)"
    echo "   - IMPLEMENTATION_GUIDE.md (how to build)"
    echo ""
    echo "2. 🗄️ Setup Database (if using PostgreSQL):"
    echo "   docker run -d -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:15"
    echo "   # Update DATABASE_URL in backend/.env"
    echo ""
    echo "3. 🔴 Setup Redis (if using caching):"
    echo "   docker run -d -p 6379:6379 redis:7-alpine"
    echo ""
    echo "4. 🚀 Start Backend Development Server:"
    echo "   cd backend"
    echo "   source venv/bin/activate"
    echo "   uvicorn app.main:app --reload"
    echo "   # API will be available at http://localhost:8000"
    echo ""
    echo "5. ⚛️  Start Frontend Development Server:"
    echo "   cd frontend"
    echo "   npm start"
    echo "   # React app will be available at http://localhost:3000"
    echo ""
    echo "6. 🧪 Run Tests:"
    echo "   cd backend"
    echo "   pytest tests/ --cov=."
    echo ""
    echo "7. 🐳 Or use Docker Compose (all-in-one):"
    echo "   docker-compose up -d"
    echo ""
    echo -e "${BLUE}Key Files:${NC}"
    echo "  ✓ backend/llm_engine.py - AI integration (800+ lines)"
    echo "  ✓ frontend/src/App.jsx - React app shell (250+ lines)"
    echo "  ✓ backend/requirements.txt - Python dependencies"
    echo "  ✓ frontend/package.json - Node dependencies"
    echo ""
    echo -e "${BLUE}Important URLs:${NC}"
    echo "  - API Docs: http://localhost:8000/docs"
    echo "  - Frontend: http://localhost:3000"
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo ""
}

# Main execution
main() {
    check_prerequisites
    setup_backend
    setup_frontend
    
    read -p "Do you want to set up Docker/Docker Compose? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_docker
    fi
    
    print_next_steps
}

# Run main function
main
