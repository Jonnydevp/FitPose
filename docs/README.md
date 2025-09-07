# 📚 FitPose Documentation

Welcome to the FitPose project documentation. This AI-powered exercise analysis platform combines computer vision and machine learning to provide real-time workout feedback.

## 📖 Table of Contents

- [🚀 Quick Start Guide](#-quick-start-guide)
- [🏗️ Architecture Overview](#-architecture-overview)
- [🔧 Development Setup](#-development-setup)
- [🚀 Deployment Guide](./DEPLOYMENT.md)
- [📚 API Documentation](#-api-documentation)
- [🎯 Usage Examples](#-usage-examples)

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.9+
- Node.js 18+
- OpenAI API Key

### Installation
```bash
# Clone the repository
git clone https://github.com/Jonnydevp/FitPose.git
cd FitPose

# Setup Python environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Start backend server
python main.py

# In a new terminal, setup frontend
cd src/frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to access the application.

## 🏗️ Architecture Overview

FitPose follows a clean architecture pattern with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   AI Services   │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (OpenAI)      │
│                 │    │                 │    │                 │
│ • Video Upload  │    │ • API Routes    │    │ • GPT-4 Analysis│
│ • Real-time UI  │    │ • CORS Handling │    │ • Form Feedback │
│ • Results View  │    │ • File Processing│    │ • Exercise Tips │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │ Computer Vision │
                       │  (MediaPipe)    │
                       │                 │
                       │ • Pose Detection│
                       │ • Keypoints     │
                       │ • Movement Track│
                       └─────────────────┘
```

### Core Components

#### Backend (`src/backend/`)
- **API Layer**: REST endpoints for exercise analysis
- **Core Layer**: Configuration and business logic
- **Models Layer**: Data validation and schemas
- **Services Layer**: External service integrations

#### Computer Vision (`src/cv/`)
- **Video Processor**: MediaPipe integration for pose detection
- **Keypoint Analysis**: Body landmark detection and tracking

#### AI Analysis (`src/ml/`)
- **AI Feedback**: OpenAI GPT-4 integration for exercise analysis
- **Form Assessment**: Intelligent exercise form evaluation

#### Frontend (`src/frontend/`)
- **React Components**: Modern UI with Tailwind CSS
- **Video Handling**: File upload and processing interface
- **Results Display**: AI feedback visualization

## 🔧 Development Setup

### Backend Development
```bash
# Activate virtual environment
source .venv/bin/activate

# Install development dependencies
pip install -r requirements.txt

# Run with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Frontend Development
```bash
cd src/frontend

# Install dependencies
npm install

# Start development server with hot reload
npm run dev

# Build for production
npm run build
```

### Environment Variables
Create a `.env` file in the project root:
```env
# AI Service Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Development Configuration
ENVIRONMENT=development
DEBUG=true

# Production Configuration (for deployment)
FRONTEND_URL=https://fit-pose.vercel.app
BACKEND_URL=https://web-production-92856.up.railway.app
```

## 📚 API Documentation

### Health Check
```http
GET /health
```
Returns server status and health information.

### Exercise Analysis
```http
POST /api/exercise/analyze
Content-Type: multipart/form-data

{
  "video": [video file],
  "exercise_type": "squat" | "pushup" | "pullup"
}
```

Returns AI-powered analysis with:
- Form assessment
- Improvement suggestions
- Exercise-specific feedback

### API Documentation (Swagger)
Visit `http://localhost:8001/docs` when running locally for interactive API documentation.

## 🎯 Usage Examples

### Basic Exercise Analysis
1. Upload a workout video (MP4, MOV, AVI)
2. Select exercise type (squat, pushup, pullup)
3. Submit for AI analysis
4. Review detailed feedback and suggestions

### Supported Exercise Types
- **Squats**: Form analysis, depth assessment, alignment check
- **Push-ups**: Hand positioning, body alignment, range of motion
- **Pull-ups**: Grip analysis, full range evaluation, form consistency

### Video Requirements
- Duration: 5-60 seconds
- Format: MP4, MOV, AVI
- Quality: 720p minimum recommended
- Lighting: Good visibility of body movements

## 🚀 Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions for:
- Railway (Backend)
- Vercel (Frontend)
- Environment configuration
- CI/CD setup

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

For support, please open an issue on GitHub or contact the development team.

---

**Live Demo**: [https://fit-pose.vercel.app](https://fit-pose.vercel.app)  
**API Endpoint**: [https://web-production-92856.up.railway.app](https://web-production-92856.up.railway.app)