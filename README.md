# FitPose

> AI-Powered Exercise Analysis Platform

[![Live Demo](https://img.shields.io/badge/Demo-fit--pose.vercel.app-blue)](https://fit-pose.vercel.app)
[![API](https://img.shields.io/badge/API-Railway-purple)](https://web-production-92856.up.railway.app/docs)

Transform your workouts with AI-powered form analysis using Computer Vision and GPT-4.

## Quick Start

```bash
# Clone and setup
git clone https://github.com/Jonnydevp/FitPose.git && cd FitPose

# Backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your OPENAI_API_KEY
python main.py

# Frontend (new terminal)
cd src/frontend && npm install && npm run dev
```

**Open**: http://localhost:5173

## Tech Stack

- **Frontend**: React + Vite + Tailwind CSS  
- **Backend**: FastAPI + OpenAI GPT-4 + MediaPipe  
- **Deploy**: Vercel + Railway  

## Architecture

```
User → Frontend (React) → Backend API (FastAPI) → CV Processing → AI Analysis
```

### Workflow:

1. **Video Upload** - user uploads video through web interface
2. **Video Processing** - VideoProcessor extracts movement vectors using MediaPipe  
3. **AI Analysis** - vectors are sent to OpenAI for technique analysis
4. **Results** - user receives detailed feedback

## Features

- AI exercise form analysis
- Real-time video processing
- Support for multiple exercise types (squats, push-ups, pull-ups)
- REST API with interactive documentation
- Modern responsive UI

## API Endpoints

### Health Check
```http
GET /health
```

### Exercise Analysis
```http
POST /api/v1/analyze-exercise
Content-Type: multipart/form-data

file: [video file]
```

## Environment

```bash
# .env
OPENAI_API_KEY=your_openai_api_key_here
```

## Development

### Backend
```bash
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd src/frontend
npm run dev
```

For production builds on Vercel, set:
```env
VITE_API_URL=""
```
Then add a Vercel Rewrite (Project Settings → Routing → Rewrites):
- Source: `/api/(.*)`
- Destination: `https://your-railway-url.up.railway.app/api/$1`

With this setup the frontend calls relative paths (same-origin), and Vercel proxies `/api/...` to Railway. If you prefer not to use rewrites, set `VITE_API_URL` to `https://your-railway-url.up.railway.app` instead.

## Deploy

**One-Click Deploy:**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/fitpose) [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Jonnydevp/FitPose)

**Manual**: See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## Project Structure

```
FitPose/
├── main.py                   # FastAPI entry point
├── requirements.txt          # Python dependencies  
├── .env.example             # Environment template
├── src/
│   ├── backend/             # FastAPI application
│   │   ├── api/             # REST endpoints
│   │   ├── core/            # Configuration
│   │   ├── models/          # Data schemas
│   │   └── services/        # Business logic
│   ├── cv/                  # Computer Vision (MediaPipe)
│   ├── ml/                  # AI Analysis (OpenAI)
│   └── frontend/            # React application
├── docs/                    # Documentation
│   ├── README.md            # Detailed setup guide
│   └── DEPLOYMENT.md        # Production deployment
└── .github/workflows/       # CI/CD pipeline
```

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push branch: `git push origin feature/name`
5. Open Pull Request

## License

MIT License - see [LICENSE](LICENSE)
