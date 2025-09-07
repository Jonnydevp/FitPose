# 🚀 Deployment Guide

## 🎯 One-URL Fullstack Deployment (Recommended)

### Option 1: Vercel Unified Deployment

1. **Visit [vercel.com](https://vercel.com)** and sign in with your GitHub account

2. **Import your repository:**
   - Click "New Project"
   - Select this repository: `FitPose`
   - Choose the `src/frontend` folder as the root directory

3. **Configure build settings:**
   - Framework Preset: `Vite`
   - Root Directory: `src/frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **Deploy** - Vercel will automatically:
   - Build and host your React frontend
   - Proxy `/api/*` requests to Railway backend
   - Provide unified access on one domain

**Result**: Your app will be available at one URL with both frontend and backend working seamlessly!

### How it works:
- **Frontend**: Served by Vercel
- **API calls**: Automatically proxied to Railway backend
- **Single domain**: Everything accessible from your Vercel URL

---

## Alternative Deployment Options

### Option 2: Separate Deployments

### Option 2: Separate Deployments

**Frontend (Vercel):**
1. Visit [vercel.com](https://vercel.com)
2. Import repository and select `src/frontend` folder
3. Deploy with Vite preset

**Backend (Railway):**
- Already deployed at `https://web-production-92856.up.railway.app`

### Option 3: Local Development Server

```bash
cd src/frontend
npm run build
python3 serve.py
```

Visit http://localhost:8080

### Option 4: Netlify Deployment

1. **Visit [netlify.com](https://netlify.com)**
2. **Drag and drop** the `src/frontend/dist` folder
3. **Configure redirects** for SPA routing

## Current Status ✅

- **Backend**: Deployed to Railway at `https://web-production-92856.up.railway.app`
- **Frontend**: Ready for unified deployment with API proxy configuration
- **Single URL**: Configured for seamless fullstack deployment on Vercel
- **API Integration**: Frontend uses relative URLs, proxied by Vercel to Railway

## Unified Deployment Architecture

```
Your-Vercel-Domain.vercel.app
├── / (React Frontend)
├── /api/* (Proxied to Railway Backend)
├── /health (Proxied to Railway)
└── /docs (Proxied to Railway API docs)
```

## Environment Variables

Make sure these are set in your Railway dashboard:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Testing the Full Stack

1. Deploy frontend using one of the options above
2. Visit your frontend URL
3. Upload a video file to test the exercise analysis
4. Check that API calls are working correctly

## Local Development

```bash
# Backend (Port 8000)
python main.py

# Frontend (Port 5173)
cd src/frontend
npm run dev
```
