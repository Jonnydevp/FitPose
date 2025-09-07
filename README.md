# FitPose - AI-Powered Exercise Analysis

FitPose analyzes your workout videos using computer vision and artificial intelligence, providing personalized feedback on exercise technique.

## 🏗️ Architecture

```
User → Frontend (React) → Backend API (FastAPI) → CV Processing → AI Analysis
```

### Workflow:
1. **Video Upload** - user uploads video through web interface
2. **Video Processing** - `VideoProcessor` extracts movement vectors using MediaPipe
3. **AI Analysis** - vectors are sent to OpenAI for technique analysis
4. **Results** - user receives detailed feedback

## 🚀 Quick Start

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/Jonnydevp/FitPose.git
cd FitPose
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

4. **Start backend:**
```bash
uvicorn main:app --reload
```

5. **Start frontend (in another terminal):**
```bash
cd src/frontend
npm install
npm run dev
```

### Deploy to Railway

**Automatic deployment:**
```bash
./deploy-railway.sh
```

**Manual deployment:**
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize  
railway init

# 4. Deploy
railway up --detach

# 5. Set environment variable
railway variables set OPENAI_API_KEY=your_actual_key
```

**After deployment:**
1. Copy URL from Railway dashboard
2. Update `API_URL` in `src/frontend/src/App.jsx`
3. Test: `./health-check.sh https://your-app.railway.app`

## 📁 Project Architecture

```
FitPose/
├── main.py                        # FastAPI application entry point
├── requirements.txt               # Python dependencies
├── railway.toml                  # Railway configuration
├── .env.example                  # Environment variables example
├── deploy-railway.sh             # Deployment script
├── src/
│   ├── backend/                  # 🏗️ Backend architecture
│   │   ├── api/                  # API routes
│   │   │   ├── exercise_routes.py   # Exercise analysis endpoints
│   │   │   └── system_routes.py     # System endpoints
│   │   ├── core/                 # Core settings
│   │   │   └── config.py           # Application configuration
│   │   ├── models/               # Data models
│   │   │   └── schemas.py          # API schemas
│   │   └── services/             # Business logic
│   │       ├── video_service.py    # Video processing
│   │       └── analysis_service.py # AI analysis
│   ├── cv/                       # 🎥 Computer Vision
│   │   └── video_processor.py       # Movement vector extraction
│   ├── ml/                       # 🤖 Machine Learning
│   │   └── ai_feedback.py           # AI technique analysis
│   └── frontend/                 # ⚛️ React application
│       ├── package.json
│       ├── vite.config.js
│       └── src/
│           ├── App.jsx
│           └── components/
└── README.md
```

### 🏗️ Backend Architecture

**Clean architecture** with separation of concerns:

- **`api/`** - HTTP routes and endpoints
- **`core/`** - Configuration and settings
- **`models/`** - Data schemas and models
- **`services/`** - Business logic and services

**Principles:**
- Dependency Injection
- Separation of Concerns  
- Single Responsibility
- Clean Code

## 🔧 API Endpoints

### `POST /analyze-exercise`
Main endpoint for exercise analysis.

**Input:** 
- `file` (multipart/form-data) - video file

**Output:**
```json
{
  "status": "success",
  "analysis": {
    "overall_score": 8,
    "exercise_detected": "Push-ups",
    "technique_analysis": {
      "form_quality": "good",
      "symmetry": "symmetric",
      "range_of_motion": "full",
      "tempo": "appropriate"
    },
    "feedback": {
      "positive": ["Good push-up depth"],
      "improvements": ["Keep your back straight"],
      "specific_tips": ["Engage your core"]
    }
  },
  "metrics": {
    "rep_count": 12,
    "total_frames": 360,
    "duration": 12.0
  }
}
```

### `GET /health`
Service health check.

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 8000 |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `DEBUG` | Debug mode | False |
| `CORS_ORIGINS` | Allowed domains | * |
| `MAX_FILE_SIZE_MB` | Max file size | 50 |

## 🔬 Technologies

**Backend:**
- FastAPI - web framework
- OpenCV - video processing
- MediaPipe - pose detection
- NumPy/Pandas - data processing
- OpenAI API - movement analysis

**Frontend:**
- React 19 - UI framework
- Vite - bundler
- Tailwind CSS - styling

**Deployment:**
- Railway - backend hosting
- Vercel/Netlify - frontend hosting (optional)

## 🤝 Development

### Adding New Exercises

1. Update logic in `video_processor.py` to detect new movement types
2. Add corresponding prompts in `ai_feedback.py`
3. Update exercise list in `App.jsx`

### Improving AI Analysis

Modify prompts in `ai_feedback.py`, method `prepare_analysis_prompt()`.

## 📊 Monitoring

- Railway logs: `railway logs`
- API status: `GET /health`
- Metrics in Railway Dashboard

## 🔒 Security

- File type validation
- File size limitations
- Temporary file cleanup
- CORS policies

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🆘 Support

- GitHub Issues: [FitPose Issues](https://github.com/Jonnydevp/FitPose/issues)
- Email: support@fitpose.com

🏋️‍♂️ **FitPose** - Smart exercise analysis system using computer vision and machine learning.

## 🌟 Features

- 📹 Real-time exercise video analysis
- 🤖 MediaPipe pose detection
- 📊 Detailed technique analytics
- 💡 Personalized recommendations
- 🎯 Support for various exercise types:
  - Push-ups
  - Squats
  - Burpees
  - Planks
  - Lunges

## 🏗️ Architecture

- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: FastAPI + Python
- **AI/ML**: MediaPipe + TensorFlow/PyTorch
- **Deploy**: Docker + Docker Compose
- **CI/CD**: GitHub Actions

## 🚀 Quick Start

### Local Development

1. **Clone repository:**
```bash
git clone https://github.com/Jonnydevp/FitPose.git
cd FitPose
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Start backend:**
```bash
cd src/backend
python main.py
```

4. **Install and start frontend:**
```bash
cd src/frontend
npm install
npm run dev
```

### Production Deployment with Docker

1. **Make sure Docker is installed:**
```bash
docker --version
docker-compose --version
```

2. **Create .env file** (use .env as template)

3. **Run deployment:**
```bash
./deploy.sh
```

Application will be available at: http://localhost

## 📡 API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health check
- `POST /analyze-video` - Exercise video analysis
- `GET /supported-exercises` - List of supported exercises
- `GET /docs` - Swagger documentation

## 🔧 Configuration

Main settings in `.env` file:

```env
ENV=production
HOST=0.0.0.0
PORT=8000
MAX_FILE_SIZE=52428800  # 50MB
MIN_DETECTION_CONFIDENCE=0.5
MIN_TRACKING_CONFIDENCE=0.5
```

## 📁 Project Structure

```
FitPose/
├── src/
│   ├── backend/           # FastAPI server
│   │   ├── app/
│   │   │   ├── models/    # Pydantic models
│   │   │   ├── services/  # Business logic
│   │   │   └── routers/   # API routers
│   │   └── main.py        # Entry point
│   ├── frontend/          # React application
│   │   └── src/
│   ├── cv/               # Computer vision
│   └── ml/               # Machine learning
├── .github/workflows/    # CI/CD
├── docker-compose.yml    # Orchestration
├── Dockerfile.backend    # Backend image
├── Dockerfile.frontend   # Frontend image
├── nginx.conf           # Nginx configuration
├── deploy.sh           # Deploy script
└── requirements.txt    # Python dependencies
```

## 🧪 Testing

```bash
# Backend tests
cd src/backend
pytest

# Frontend tests
cd src/frontend
npm test

# Linting
npm run lint
```

## 📊 Monitoring

- Health checks built into Docker containers
- Logs available via `docker-compose logs`
- Metrics can be configured via Prometheus/Grafana

## 🤝 Development

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push branch: `git push origin feature/new-feature`
5. Create Pull Request

## 📝 TODO

- [ ] Add support for more exercises
- [ ] OpenAI integration for enhanced feedback
- [ ] Database for storing results
- [ ] Mobile application
- [ ] Fitness tracker integration
- [ ] Social features and competitions

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 👥 Authors

- [Jonnydevp](https://github.com/Jonnydevp)

## 🆘 Support

If you have questions or issues:
1. Check [Issues](https://github.com/Jonnydevp/FitPose/issues)
2. Create new Issue
3. Contact development team