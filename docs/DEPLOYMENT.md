# 🚀 FitPose Deployment Guide

This guide covers deployment of FitPose to production environments using Railway (backend) and Vercel (frontend).

## 📋 Prerequisites

- GitHub account with FitPose repository
- Railway account (for backend deployment)
- Vercel account (for frontend deployment)
- OpenAI API key

## 🚂 Backend Deployment (Railway)

### Step 1: Prepare Railway Configuration

The project includes `railway.toml` and `nixpacks.toml` for automatic deployment:

**railway.toml**
```toml
[build]
builder = "NIXPACKS"

[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

**nixpacks.toml**
```toml
[phases.setup]
cmds = [
    "apt-get update",
    "apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1"
]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.build]
cmds = ["echo 'Build complete'"]

[start]
cmd = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

### Step 2: Deploy to Railway

1. **Connect Repository**
   - Go to [Railway](https://railway.app)
   - Click "Deploy from GitHub repo"
   - Select your FitPose repository

2. **Configure Environment Variables**
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ENVIRONMENT=production
   PORT=8000
   ```

3. **Deploy**
   - Railway will automatically build and deploy
   - Monitor logs for successful deployment
   - Note your Railway app URL (e.g., `web-production-92856.up.railway.app`)

### Step 3: Verify Backend Deployment

Test the deployed backend:
```bash
# Health check
curl https://web-production-92856.up.railway.app/health

# API documentation
curl https://web-production-92856.up.railway.app/docs
```

## ⚡ Frontend Deployment (Vercel)

### Step 1: Prepare Vercel Configuration

The project includes `vercel.json` for deployment configuration:

**vercel.json**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "src/frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/src/frontend/dist/$1"
    }
  ],
  "functions": {
    "src/frontend/dist/**": {
      "includeFiles": "src/frontend/dist/**"
    }
  }
}
```

### Step 2: Configure Frontend Environment

Update `src/frontend/src/App.jsx` to use production API URL:
```javascript
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://web-production-92856.up.railway.app'
  : 'http://localhost:8001';
```

### Step 3: Deploy to Vercel

1. **Connect Repository**
   - Go to [Vercel](https://vercel.com)
   - Click "Import Git Repository"
   - Select your FitPose repository

2. **Configure Build Settings**
   - Framework Preset: `Vite`
   - Root Directory: `src/frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

3. **Environment Variables** (if needed)
   ```env
   VITE_API_URL=https://web-production-92856.up.railway.app
   ```

4. **Deploy**
   - Vercel will automatically build and deploy
   - Note your Vercel app URL (e.g., `fit-pose.vercel.app`)

### Step 4: Verify Frontend Deployment

Visit your Vercel URL and test:
- Video upload functionality
- API communication with Railway backend
- Exercise analysis workflow

## 🔗 Cross-Origin Configuration

### Backend CORS Setup

Ensure `main.py` includes proper CORS configuration:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",           # Local development
        "https://fit-pose.vercel.app",     # Production frontend
        "https://*.vercel.app",            # Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🔐 Environment Variables

### Production Environment Variables

**Railway (Backend)**
```env
OPENAI_API_KEY=sk-your-openai-key-here
ENVIRONMENT=production
PORT=8000
FRONTEND_URL=https://fit-pose.vercel.app
```

**Vercel (Frontend)** - Optional
```env
VITE_API_URL=https://web-production-92856.up.railway.app
```

## 📊 Monitoring and Health Checks

### Railway Health Check
Railway automatically monitors the `/health` endpoint:
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
```

### Vercel Analytics
Enable Vercel Analytics for frontend monitoring:
1. Go to Vercel dashboard
2. Select your project
3. Navigate to Analytics tab
4. Enable analytics

## 🚀 CI/CD Pipeline

### GitHub Actions Workflow

The project includes `.github/workflows/ci.yml`:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest
      
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Railway
        run: echo "Deploying to Railway..."
      - name: Deploy to Vercel
        run: echo "Deploying to Vercel..."
```

## 🔧 Troubleshooting

### Common Deployment Issues

**Railway Deployment Fails**
1. Check `nixpacks.toml` system dependencies
2. Verify `requirements.txt` is complete
3. Check environment variables are set
4. Monitor Railway logs for specific errors

**Vercel Build Fails**
1. Ensure `package.json` is in `src/frontend/`
2. Check build commands in Vercel settings
3. Verify no import errors in React components
4. Check Vercel build logs

**CORS Errors**
1. Update CORS origins in `main.py`
2. Include your Vercel domain
3. Check frontend API URL configuration
4. Test with browser dev tools

**API Connection Issues**
1. Verify Railway backend is running (`/health`)
2. Check frontend API URL configuration
3. Test API endpoints directly
4. Monitor network requests in browser

### Performance Optimization

**Backend (Railway)**
- Use gunicorn for production WSGI server
- Enable request compression
- Implement caching for analysis results
- Monitor memory usage

**Frontend (Vercel)**
- Enable Vercel Edge Functions if needed
- Implement code splitting
- Optimize video file handling
- Use Vercel Image Optimization

## 📈 Scaling Considerations

### Horizontal Scaling
- Railway supports automatic scaling
- Consider database addition for user data
- Implement Redis for caching
- Add load balancing for high traffic

### Performance Monitoring
- Railway provides built-in metrics
- Vercel Analytics for frontend performance
- Consider APM tools for detailed monitoring
- Set up alerts for downtime

## 🆘 Support and Maintenance

### Regular Maintenance
- Monitor dependency security updates
- Update OpenAI API integration
- Check Railway and Vercel service updates
- Review and update documentation

### Backup Strategy
- GitHub repository as source backup
- Export environment variables
- Document deployment configurations
- Maintain deployment runbooks

---

**Live Endpoints**:
- Frontend: https://fit-pose.vercel.app
- Backend: https://web-production-92856.up.railway.app
- API Docs: https://web-production-92856.up.railway.app/docs