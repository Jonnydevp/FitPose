# FitPose Documentation

AI-powered exercise analysis platform using computer vision and machine learning.

## Quick Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- OpenAI API Key

### Installation
```bash
# Clone and setup environment
git clone https://github.com/Jonnydevp/FitPose.git && cd FitPose
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Start backend
python main.py

# Start frontend (new terminal)
cd src/frontend && npm install && npm run dev
```

Visit `http://localhost:5173`

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   AI Services   │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (OpenAI)      │
│                 │    │                 │    │                 │
│ • Video Upload  │    │ • API Routes    │    │ • GPT-4 Analysis│
│ • Real-time UI  │    │ • File Process  │    │ • Form Feedback │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │ Computer Vision │
                       │  (MediaPipe)    │
                       │ • Pose Detection│
                       └─────────────────┘
```

## API Endpoints

### Health Check
```http
GET /health
```

### Exercise Analysis
```http
POST /api/exercise/analyze
Content-Type: multipart/form-data

{
  "video": [file],
  "exercise_type": "squat" | "pushup" | "pullup"
}
```

**Response**: AI analysis with form assessment and suggestions.

## Development

### Backend
```bash
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Frontend
```bash
cd src/frontend
npm run dev
```

### Environment Variables
```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
ENVIRONMENT=development
DEBUG=true
```

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment guides:
- Railway (Backend)
- Vercel (Frontend)
- Environment configuration

## Supported Exercises
- **Squats**: Form analysis, depth assessment
- **Push-ups**: Hand position, body alignment
- **Pull-ups**: Range of motion, form consistency

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push branch: `git push origin feature/name`
5. Open Pull Request

## License

MIT License - see [LICENSE](../LICENSE)

---

**Live Demo**: [https://fit-pose.vercel.app](https://fit-pose.vercel.app)  
**API**: [https://web-production-92856.up.railway.app](https://web-production-92856.up.railway.app)