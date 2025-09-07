# 🚀 Deployment Guide

## Frontend Deployment Instructions

### Option 1: Manual Vercel Deployment (Recommended)

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

4. **Deploy** - Vercel will automatically build and deploy your frontend

### Option 2: Local Development Server

```bash
cd src/frontend
npm run build
python3 serve.py
```

Visit http://localhost:8080

### Option 3: Netlify Deployment

1. **Visit [netlify.com](https://netlify.com)**
2. **Drag and drop** the `src/frontend/dist` folder
3. **Configure redirects** for SPA routing

## Current Status ✅

- **Backend**: Deployed to Railway at `https://web-production-92856.up.railway.app`
- **Frontend**: Ready for deployment (built and configured)
- **API Integration**: Frontend configured to use production backend

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
