# ⚡ QUICK REFERENCE - Common Commands

## 🚀 Quick Start

### Windows
```batch
setup.bat
```

### macOS/Linux
```bash
bash setup.sh
```

---

## 📦 Backend Commands

### Setup Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Create Environment File
```bash
# Copy template and edit
cp .env.example .env
# Edit .env with your settings
```

### Run Backend Server
```bash
# Development (with auto-reload)
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "add new table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run specific test
pytest tests/test_api.py::test_login
```

### Linting & Code Quality
```bash
# Format code
black backend/

# Check style
flake8 backend/

# Security check
bandit -r backend/

# Type checking
mypy backend/
```

### Create Superuser
```bash
python -m backend.create_superuser
```

### Access API Documentation
```
http://localhost:8000/docs       # Swagger UI
http://localhost:8000/redoc      # ReDoc
```

---

## ⚛️ Frontend Commands

### Setup Environment
```bash
cd frontend
npm install
```

### Development Server
```bash
npm start
# Opens http://localhost:3000
```

### Build for Production
```bash
npm run build
# Creates optimized build in dist/
```

### Testing
```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

### Linting
```bash
npm run lint
npm run lint -- --fix  # Auto-fix issues
```

### Build Size Analysis
```bash
npm run build
npm run analyze  # If webpack-bundle-analyzer is installed
```

---

## 🐳 Docker Commands

### Build Images
```bash
# Backend
docker build -t security-backend:dev -f backend/Dockerfile ./backend

# Frontend
docker build -t security-frontend:dev -f frontend/Dockerfile ./frontend
```

### Run Containers
```bash
# Backend
docker run -d \
  --name security-backend \
  -p 8000:8000 \
  --env-file backend/.env \
  security-backend:dev

# Frontend
docker run -d \
  --name security-frontend \
  -p 3000:3000 \
  security-frontend:dev
```

### View Logs
```bash
docker logs security-backend -f
docker logs security-frontend -f
```

### Stop & Remove
```bash
docker stop security-backend security-frontend
docker rm security-backend security-frontend
```

### Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up -d --build

# Run migrations
docker-compose exec backend alembic upgrade head
```

---

## ☸️ Kubernetes Commands

### Create Resources
```bash
# Create namespace
kubectl create namespace security-ns

# Create secrets
kubectl create secret generic db-config \
  --from-literal=DATABASE_URL=postgresql://... \
  -n security-ns

# Apply manifests
kubectl apply -f k8s/ -n security-ns
```

### Check Status
```bash
# View pods
kubectl get pods -n security-ns

# View services
kubectl get svc -n security-ns

# View deployments
kubectl get deployments -n security-ns
```

### Monitoring
```bash
# View logs
kubectl logs -f deployment/security-backend -n security-ns

# View pod details
kubectl describe pod <pod-name> -n security-ns

# Watch real-time
kubectl get pods -n security-ns -w
```

### Scaling
```bash
# Scale deployment
kubectl scale deployment security-backend --replicas=5 -n security-ns

# Autoscale
kubectl autoscale deployment security-backend \
  --min=2 --max=10 --cpu-percent=80 -n security-ns
```

### Delete Resources
```bash
# Delete namespace (deletes all resources)
kubectl delete namespace security-ns
```

---

## 🔧 Database Commands

### PostgreSQL
```bash
# Connect to database
psql postgresql://user:password@localhost:5432/security_assistant

# List databases
\l

# Choose database
\c security_assistant

# List tables
\dt

# Exit
\q
```

### Create Database
```bash
createdb -U postgres security_assistant

# Or with docker
docker run -d \
  -e POSTGRES_USER=security_user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=security_assistant \
  -p 5432:5432 \
  postgres:15
```

### Backup & Restore
```bash
# Backup
pg_dump postgresql://user:password@localhost:5432/security_assistant > backup.sql

# Restore
psql postgresql://user:password@localhost:5432/security_assistant < backup.sql
```

---

## 🔐 Security Commands

### Generate Secret Key
```bash
# Python
python -c "import secrets; print(secrets.token_hex(32))"

# OpenSSL
openssl rand -hex 32
```

### JWT Token
```python
# Generate token
from app.auth import create_access_token
token = create_access_token({"sub": "user_id"})

# Decode token
from app.auth import decode_token
payload = decode_token(token)
```

### Hash Password
```python
from app.security import hash_password, verify_password

hashed = hash_password("mypassword")
is_valid = verify_password("mypassword", hashed)
```

---

## 📊 Git Commands

### Workflow
```bash
# Clone repo
git clone <repository-url>
cd security_assistant

# Create feature branch
git checkout -b feature/my-feature

# Stage changes
git add .

# Commit
git commit -m "Add new feature"

# Push
git push origin feature/my-feature

# Create pull request on GitHub
```

### Common Tasks
```bash
# View status
git status

# View changes
git diff

# View commit log
git log --oneline

# Undo changes
git reset --hard HEAD

# Stash changes
git stash

# Switch branch
git checkout main
```

---

## 🚀 Deployment Commands

### Docker Deployment
```bash
# Build and push to registry
docker tag security-backend:dev myregistry/security-backend:v1.0
docker push myregistry/security-backend:v1.0

# Deploy
docker run -d myregistry/security-backend:v1.0
```

### Kubernetes Deployment
```bash
# Deploy
kubectl apply -f k8s/

# Check status
kubectl get pods -n security-ns

# View service
kubectl get svc -n security-ns

# Port forward
kubectl port-forward svc/backend-service 8000:8000 -n security-ns
```

### Cloud Deployment

**AWS:**
```bash
# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
docker tag security-backend:dev <account>.dkr.ecr.<region>.amazonaws.com/security-backend:v1.0
docker push <account>.dkr.ecr.<region>.amazonaws.com/security-backend:v1.0
```

**Google Cloud:**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/security-backend ./backend
gcloud run deploy security-backend --image gcr.io/PROJECT_ID/security-backend
```

**Azure:**
```bash
az acr build --registry myregistry --image security-backend:v1.0 ./backend
az container create --image myregistry.azurecr.io/security-backend:v1.0
```

---

## 📈 Performance Testing

### Load Testing
```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8000/api/health

# Using wrk
wrk -t4 -c100 -d30s http://localhost:8000/api/health
```

### Profiling
```python
# Python profiling
python -m cProfile -s cumulative app/main.py

# Memory profiling
pip install memory-profiler
python -m memory_profiler app/main.py
```

---

## 📚 Useful Links

### Documentation
- FastAPI: https://fastapi.tiangolo.com
- React: https://react.dev
- PostgreSQL: https://postgresql.org/docs
- Docker: https://docs.docker.com
- Kubernetes: https://kubernetes.io/docs

### Tools
- Swagger Editor: https://editor.swagger.io
- Postman: https://postman.com
- VS Code: https://code.visualstudio.com
- DBeaver: https://dbeaver.io (Database GUI)

### APIs
- OpenAI: https://platform.openai.com
- Anthropic: https://console.anthropic.com
- GitHub: https://github.com

---

## 🆘 Troubleshooting Quick Fixes

### "Module not found" error
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### Port already in use
```bash
# Find process using port
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows
```

### Database connection error
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Start PostgreSQL
docker run -d -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:15

# Test connection
psql postgresql://user:password@localhost:5432/security_assistant -c "SELECT 1"
```

### Clear Python cache
```bash
# Remove __pycache__
find . -type d -name __pycache__ -exec rm -r {} +

# Remove .pyc files
find . -type f -name "*.pyc" -delete
```

### Reset Frontend
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

---

## ⏱️ Expected Runtimes

| Task | Time |
|------|------|
| Initial Setup | 10-15 min |
| Backend Start | 5 sec |
| Frontend Start | 10 sec |
| Database Migration | 30 sec |
| API Request | <100ms |
| Tests (backend) | 30-60 sec |
| Build (frontend) | 2-3 min |
| Docker Build | 5-10 min |

---

## 📋 Pre-Launch Checklist

- [ ] All tests passing
- [ ] No console errors
- [ ] API docs accessible
- [ ] Database connected
- [ ] LLM configured (or fallback enabled)
- [ ] HTTPS configured
- [ ] Environment variables set
- [ ] Logs monitored
- [ ] Backups configured
- [ ] Documentation reviewed

---

**Save this file for quick reference during development!**

Last Updated: March 2024
