# FitPose Deployment Guide

Deploy FitPose to production using Railway (backend) and Vercel (frontend).

## Prerequisites

- GitHub account with FitPose repository
- Railway account
- Vercel account  
- OpenAI API key

## Backend Deployment (Railway)

### 1. Automatic Deployment

1. **Connect Repository**
   - Go to [Railway](https://railway.app)
   - Click "Deploy from GitHub repo"
   - Select FitPose repository

2. **Environment Variables**
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ENVIRONMENT=production
   ```

3. **Deploy**
   - Railway auto-builds using `railway.toml` and `nixpacks.toml`
   - Monitor deployment logs
   - Note your Railway URL (e.g., `web-production-XXXXX.up.railway.app`)

### 2. Manual Deployment

Use the included script:
```bash
chmod +x deploy-railway.sh
./deploy-railway.sh
```

### 3. Verify Deployment

```bash
curl https://your-railway-url.up.railway.app/health
```

## Frontend Deployment (Vercel)

### 1. Automatic Deployment

1. **Connect Repository**
   - Go to [Vercel](https://vercel.com)
   - Import FitPose repository

2. **Build Settings**
   - Framework: `Vite`
   - Root Directory: `src/frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. **Environment Variables**
   - Option A (recommended: single URL via Vercel rewrite)
     - Set `VITE_API_URL=""` in Vercel Project → Settings → Environment Variables
     - Add Rewrite in Vercel Project → Settings → Routing → Rewrites:
       - Source: `/api/(.*)` → Destination: `https://your-railway-url.up.railway.app/api/$1`
     - Frontend will call relative `/api/...`, Vercel proxies to Railway

   - Option B (direct calls to Railway)
     - Set `VITE_API_URL=https://your-railway-url.up.railway.app`
     - Ensure CORS on backend allows your Vercel domain

### 2. Configuration

The included `vercel.json` handles routing automatically.

### 3. Configure API URL

Preferred: set a project env var in Vercel so you can change the backend without code changes:

Use Option A (rewrite) or Option B (direct) from above. The app reads `VITE_API_URL` at build time.

## Configuration Files

### railway.toml
```toml
[build]
builder = "NIXPACKS"

[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 300
```

### nixpacks.toml  
```toml
[phases.setup]
cmds = ["apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

### vercel.json
```json
{
  "version": 2,
  "builds": [{"src": "src/frontend/package.json", "use": "@vercel/static-build"}],
  "routes": [{"src": "/(.*)", "dest": "/src/frontend/dist/$1"}]
}
```

## CORS Configuration

In `main.py`, ensure CORS allows your frontend domain:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-app.vercel.app",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Environment Variables

### Production
```env
# Railway (Backend)
OPENAI_API_KEY=your_openai_api_key_here
ENVIRONMENT=production
PORT=8000

# Vercel (Frontend) - Optional
VITE_API_URL=https://your-railway-url.up.railway.app
```

## Health Checks

### Automated Health Check
```bash
chmod +x health-check.sh
./health-check.sh https://your-railway-url.up.railway.app
```

### Manual Testing
```bash
# Test backend
curl https://your-railway-url.up.railway.app/health

# Test API docs
curl https://your-railway-url.up.railway.app/docs
```

## Troubleshooting

### Common Issues

**Railway Build Fails**
- Check `nixpacks.toml` system dependencies
- Verify `requirements.txt` includes all packages
- Monitor Railway build logs

**Vercel Build Fails**  
- Ensure `package.json` is in `src/frontend/`
- Check build commands in Vercel settings
- Verify no import errors

**CORS Errors**
- Update CORS origins in `main.py`
- Include your Vercel domain
- Check frontend API URL configuration

**API Connection Issues**
- Verify Railway backend is running (`/health`)
- Check frontend API URL matches Railway URL
- Test API endpoints directly

## Production URLs

Once deployed:
- **Frontend**: `https://your-app.vercel.app`  
- **Backend**: `https://your-railway-url.up.railway.app`
- **API Docs**: `https://your-railway-url.up.railway.app/docs`

## CI/CD

The project includes GitHub Actions workflow in `.github/workflows/ci-cd.yml` for automated testing and deployment.

---

For detailed configuration, see the included deployment scripts and configuration files.
