# 🚀 DEPLOYMENT GUIDE
> Complete instructions for deploying the Security Assistant platform to production

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Configuration](#environment-configuration)
3. [Docker Deployment](#docker-deployment)
4. [Docker Compose Setup](#docker-compose-setup)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [Cloud Deployment (AWS/GCP/Azure)](#cloud-deployment)
7. [CI/CD Pipeline](#cicd-pipeline)
8. [Monitoring & Logging](#monitoring--logging)
9. [Security Hardening](#security-hardening)
10. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

### Backend Requirements
- [ ] Python 3.9+ installed
- [ ] PostgreSQL 13+ database ready
- [ ] Redis server configured
- [ ] OpenAI/Claude API keys obtained
- [ ] All environment variables set
- [ ] Requirements.txt synchronized
- [ ] Unit tests passing (>90% coverage)
- [ ] Security scan completed (bandit)

### Frontend Requirements
- [ ] Node.js 18+ installed
- [ ] npm/yarn package manager ready
- [ ] React build optimized
- [ ] All API endpoints configured
- [ ] Environment variables for API URL
- [ ] Build tested locally
- [ ] Bundle size analyzed

### Infrastructure Requirements
- [ ] Server capacity planned (CPU, RAM, disk)
- [ ] SSL/TLS certificates obtained
- [ ] Domain name configured
- [ ] CDN setup (optional)
- [ ] Backup strategy defined
- [ ] Monitoring tools selected
- [ ] Log aggregation configured

---

## Environment Configuration

### Backend Environment Variables

Create `.env` file in backend root:

```bash
# FastAPI Configuration
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/security_assistant
SQLALCHEMY_POOL_SIZE=20
SQLALCHEMY_POOL_RECYCLE=3600

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_TTL=3600

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
WORKERS=4
WORKER_CLASS=uvicorn.workers.UvicornWorker

# LLM Configuration
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_FALLBACK=True

# Security Configuration
SECRET_KEY=your-secret-key-here-minimum-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Configuration
ALLOWED_ORIGINS=["https://yourdomain.com", "https://www.yourdomain.com"]
ALLOWED_METHODS=["GET", "POST", "PUT", "DELETE"]
ALLOWED_HEADERS=["*"]

# Monitoring
SENTRY_DSN=https://...@sentry.io/...
NEW_RELIC_LICENSE_KEY=...

# Email Configuration (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=noreply@yourdomain.com
SMTP_PASSWORD=...

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600
```

### Frontend Environment Variables

Create `.env` file in frontend root:

```bash
# API Configuration
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_API_TIMEOUT=30000

# Feature Flags
REACT_APP_ENABLE_LABS=true
REACT_APP_ENABLE_SOCIAL=true

# Analytics
REACT_APP_GA_ID=UA-...
REACT_APP_MIXPANEL_TOKEN=...

# Monitoring
REACT_APP_SENTRY_DSN=https://...@sentry.io/...
```

---

## Docker Deployment

### Dockerfile (Backend)

```dockerfile
# Base image
FROM python:3.11-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Dockerfile (Frontend)

```dockerfile
# Build stage
FROM node:18-alpine as builder

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Build application
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Install serve to run the static build
RUN npm install -g serve

# Copy built application from builder
COPY --from=builder /app/dist ./dist

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000/ || exit 1

# Start application
CMD ["serve", "-s", "dist", "-l", "3000"]
```

### Building and Running

```bash
# Build backend image
docker build -t security-assistant-backend:1.0 -f backend/Dockerfile ./backend

# Build frontend image
docker build -t security-assistant-frontend:1.0 -f frontend/Dockerfile ./frontend

# Run backend
docker run -d \
  --name security-backend \
  -p 8000:8000 \
  --env-file backend/.env \
  --link postgres:postgres \
  --link redis:redis \
  security-assistant-backend:1.0

# Run frontend
docker run -d \
  --name security-frontend \
  -p 3000:3000 \
  --env-file frontend/.env \
  security-assistant-frontend:1.0

# Check logs
docker logs security-backend -f
docker logs security-frontend -f
```

---

## Docker Compose Setup

### docker-compose.yml

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: security-postgres
    environment:
      POSTGRES_USER: security_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: security_assistant
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U security_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: security-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: security-backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://security_user:${DB_PASSWORD}@postgres:5432/security_assistant
      REDIS_URL: redis://redis:6379/0
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      ENVIRONMENT: production
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: >
      sh -c "
      alembic upgrade head &&
      uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
      "

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: security-frontend
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000/api
    depends_on:
      - backend

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: security-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
      - frontend

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    name: security-network
```

### Startup Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild services
docker-compose up -d --build

# Run migrations
docker-compose exec backend alembic upgrade head

# Create superuser
docker-compose exec backend python -m backend.create_superuser
```

---

## Kubernetes Deployment

### Deployment Manifest (backend-deployment.yaml)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: security-backend
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: security-backend
  template:
    metadata:
      labels:
        app: security-backend
    spec:
      containers:
      - name: backend
        image: security-assistant-backend:1.0
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-config
              key: DATABASE_URL
        - name: REDIS_URL
          value: "redis://redis-service:6379/0"
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: OPENAI_API_KEY
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  type: LoadBalancer
  ports:
  - port: 8000
    targetPort: 8000
  selector:
    app: security-backend
```

### Deployment Manifest (frontend-deployment.yaml)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: security-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: security-frontend
  template:
    metadata:
      labels:
        app: security-frontend
    spec:
      containers:
      - name: frontend
        image: security-assistant-frontend:1.0
        ports:
        - containerPort: 3000
        env:
        - name: REACT_APP_API_URL
          value: "http://backend-service:8000/api"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: LoadBalancer
  ports:
  - port: 3000
    targetPort: 3000
  selector:
    app: security-frontend
```

### Kubernetes Deployment Steps

```bash
# Create namespace
kubectl create namespace security-ns

# Create secrets
kubectl create secret generic db-config \
  --from-literal=DATABASE_URL=postgresql://... \
  -n security-ns

kubectl create secret generic api-keys \
  --from-literal=OPENAI_API_KEY=sk-... \
  -n security-ns

# Apply configurations
kubectl apply -f k8s/postgres-statefulset.yaml -n security-ns
kubectl apply -f k8s/redis-deployment.yaml -n security-ns
kubectl apply -f k8s/backend-deployment.yaml -n security-ns
kubectl apply -f k8s/frontend-deployment.yaml -n security-ns

# Check status
kubectl get pods -n security-ns
kubectl get svc -n security-ns

# View logs
kubectl logs -f deployment/security-backend -n security-ns

# Scale deployment
kubectl scale deployment security-backend --replicas=5 -n security-ns
```

---

## Cloud Deployment

### AWS ECS Deployment

```bash
# Create ECR repositories
aws ecr create-repository --repository-name security-assistant-backend
aws ecr create-repository --repository-name security-assistant-frontend

# Push images
docker tag security-assistant-backend:1.0 <account-id>.dkr.ecr.<region>.amazonaws.com/security-assistant-backend:1.0
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/security-assistant-backend:1.0

# Create ECS cluster
aws ecs create-cluster --cluster-name security-assistant

# Create task definitions
aws ecs register-task-definition --cli-input-json file://backend-task-def.json

# Create services
aws ecs create-service --cluster security-assistant \
  --service-name security-backend \
  --task-definition security-backend:1 \
  --desired-count 2
```

### Google Cloud Run Deployment

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/security-backend ./backend
gcloud builds submit --tag gcr.io/PROJECT_ID/security-frontend ./frontend

# Deploy backend
gcloud run deploy security-backend \
  --image gcr.io/PROJECT_ID/security-backend \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --set-env-vars "DATABASE_URL=..." \
  --allow-unauthenticated

# Deploy frontend
gcloud run deploy security-frontend \
  --image gcr.io/PROJECT_ID/security-frontend \
  --platform managed \
  --region us-central1 \
  --memory 256Mi \
  --allow-unauthenticated
```

### Azure Container Instances

```bash
# Login to Azure
az login

# Create container registry
az acr create --resource-group mygroup --name securityreg --sku Basic

# Build and push images
az acr build --registry securityreg --image security-backend:1.0 ./backend
az acr build --registry securityreg --image security-frontend:1.0 ./frontend

# Deploy to ACI
az container create \
  --resource-group mygroup \
  --name security-backend \
  --image securityreg.azurecr.io/security-backend:1.0 \
  --registry-login-server securityreg.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --cpu 1 --memory 1 \
  --ports 8000 \
  --environment-variables DATABASE_URL="..." \
  --ip-address Public \
  --protocol TCP
```

---

## CI/CD Pipeline

### GitHub Actions Workflow (.github/workflows/deploy.yml)

```yaml
name: Deploy Security Assistant

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r backend/requirements.txt
        pip install pytest pytest-cov bandit
    
    - name: Run security scan
      run: bandit -r backend/ -ll
    
    - name: Run tests
      run: |
        cd backend
        pytest tests/ --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push backend
      uses: docker/build-push-action@v4
      with:
        context: ./backend
        push: true
        tags: |
          ${{ secrets.DOCKER_USERNAME }}/security-backend:latest
          ${{ secrets.DOCKER_USERNAME }}/security-backend:${{ github.sha }}
    
    - name: Build and push frontend
      uses: docker/build-push-action@v4
      with:
        context: ./frontend
        push: true
        tags: |
          ${{ secrets.DOCKER_USERNAME }}/security-frontend:latest
          ${{ secrets.DOCKER_USERNAME }}/security-frontend:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        # Deploy using kubectl, docker-compose, or cloud CLI
        kubectl set image deployment/security-backend \
          backend=${{ secrets.DOCKER_USERNAME }}/security-backend:${{ github.sha }} \
          --record
      env:
        KUBE_CONFIG: ${{ secrets.KUBE_CONFIG }}
```

---

## Monitoring & Logging

### Prometheus Scrape Config

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'security-backend'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'

  - job_name: 'postgres'
    static_configs:
      - targets: ['localhost:5432']
```

### ELK Stack Setup (Elasticsearch, Logstash, Kibana)

```bash
# Start ELK stack
docker-compose -f elk/docker-compose.yml up -d

# Configure Logstash input (logstash.conf)
input {
  tcp {
    port => 5000
    codec => json
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "security-logs-%{+YYYY.MM.dd}"
  }
}
```

### Application Monitoring

```python
# In backend/app/main.py

from prometheus_client import Counter, Histogram, start_http_server
import time

# Metrics
request_count = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
request_duration = Histogram('request_duration_seconds', 'Request duration')
analysis_accuracy = Gauge('analysis_accuracy', 'Threat detection accuracy')

@app.middleware("http")
async def track_metrics(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    
    request_count.labels(method=request.method, endpoint=request.url.path).inc()
    request_duration.observe(duration)
    
    return response

# Start Prometheus metrics server
start_http_server(8001)
```

---

## Security Hardening

### SSL/TLS Configuration

```nginx
# nginx.conf

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL certificates
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'" always;

    # Proxy to backend
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Serve frontend
    location / {
        proxy_pass http://frontend:3000;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### Database Backups

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# PostgreSQL backup
pg_dump $DATABASE_URL > "$BACKUP_DIR/backup_$DATE.sql"
gzip "$BACKUP_DIR/backup_$DATE.sql"

# Upload to S3
aws s3 cp "$BACKUP_DIR/backup_$DATE.sql.gz" s3://my-backup-bucket/

# Keep only last 30 days
find $BACKUP_DIR -name "backup_*.gz" -mtime +30 -delete
```

---

## Troubleshooting

### Common Issues

**Issue: Database connection failed**
```bash
# Check database status
docker ps | grep postgres
docker logs security-postgres

# Test connection
psql $DATABASE_URL -c "SELECT 1"
```

**Issue: High memory usage**
```bash
# Check memory limits
docker stats
kubectl top pods

# Increase limits in docker-compose or deployment
# Restart services
```

**Issue: API not responding**
```bash
# Check logs
docker logs security-backend
kubectl logs deployment/security-backend

# Check port availability
netstat -an | grep 8000
sudo lsof -i :8000

# Health check
curl http://localhost:8000/health
```

**Issue: Frontend not connecting to API**
```bash
# Check environment variables
grep REACT_APP_API_URL .env
docker inspect security-frontend | grep ENV

# Check CORS headers
curl -H "Origin: http://localhost:3000" http://localhost:8000/api/health
```

---

## Post-Deployment

### Verification Steps

```bash
# 1. Test backend health
curl https://yourdomain.com/api/health

# 2. Test frontend accessibility
open https://yourdomain.com

# 3. Check database connectivity
psql $DATABASE_URL -c "SELECT version();"

# 4. Verify all services
kubectl get pods -n security-ns
docker ps

# 5. Monitor logs
tail -f /var/log/application.log

# 6. Test key features
# - Create user account
# - Analyze password
# - Check URL safety
# - Detect phishing
```

### Performance Tuning

```bash
# Monitor performance
docker stats
kubectl top pods

# Adjust resource limits if needed
kubectl set resources deployment security-backend \
  --limits=cpu=600m,memory=600Mi \
  --requests=cpu=300m,memory=300Mi
```

---

## Summary

You now have a complete, production-ready deployment strategy for:
✅ Docker containerization
✅ Docker Compose orchestration
✅ Kubernetes deployment
✅ Cloud platforms (AWS/GCP/Azure)
✅ CI/CD automation
✅ Monitoring & logging
✅ Security hardening
✅ Backup & recovery

**Next Steps:**
1. Choose your deployment target (Docker, K8s, Cloud)
2. Follow the specific section for your platform
3. Configure environment variables
4. Deploy and monitor
5. Test all functionality
6. Set up alerting and monitoring

---

## Support

For issues or questions:
- Check application logs: `docker logs <container>`
- Review deployment configs: Verify all YAML files
- Test connectivity: Use curl and network tools
- Consult documentation: Reference ARCHITECTURE.md for system design

**Estimated Deployment Time:** 2-4 hours (depending on platform)

---

*Last Updated: March 2024*  
*Deployment Guide v1.0*
