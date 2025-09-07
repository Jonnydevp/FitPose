import React, { useState, useRef } from 'react';
import Navbar from './components/navbar.jsx';
import HomePage from './components/homepage.jsx';
import AboutPage from './components/aboutpage.jsx';
import ContactPage from './components/contactpage.jsx';

const FitPoseApp = () => {
  const [currentPage, setCurrentPage] = useState('home');
  const [selectedExercise, setSelectedExercise] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisComplete, setAnalysisComplete] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  // API URL - Railway URL for production
  const API_URL = process.env.NODE_ENV === 'production' 
    ? 'https://your-railway-app.railway.app' 
    : 'http://localhost:8001';

  const exercises = [
    'Push-ups',
    'Squats', 
    'Burpees',
    'Planks',
    'Lunges',
    'Deadlifts',
    'Pull-ups',
    'Mountain Climbers'
  ];

  const handleFileSelect = async (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setError(null);
      
      // Check file type
      if (!file.type.startsWith('video/')) {
        setError('Please select a video file');
        return;
      }
      
      // Check file size (50MB limit)
      if (file.size > 50 * 1024 * 1024) {
        setError('File is too large. Maximum size: 50MB');
        return;
      }
      
      // Automatically start analysis
      await analyzeVideo(file);
    }
  };

  const analyzeVideo = async (file) => {
    setIsAnalyzing(true);
    setError(null);
    setAnalysisResult(null);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
            const response = await fetch(`${API_URL}/api/v1/analyze-exercise`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      
      const result = await response.json();
      
      if (result.status === 'success') {
        setAnalysisResult(result);
        setAnalysisComplete(true);
      } else {
        throw new Error('Video analysis error');
      }
      
    } catch (err) {
      console.error('Error analyzing video:', err);
      setError(err.message || 'An error occurred while analyzing the video');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const resetAnalysis = () => {
    setSelectedFile(null);
    setIsAnalyzing(false);
    setAnalysisComplete(false);
    setAnalysisResult(null);
    setError(null);
    setSelectedExercise('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="w-full">
      <Navbar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      <main>
        {currentPage === 'home' && (
          <HomePage
            analysisComplete={analysisComplete}
            selectedExercise={selectedExercise}
            setSelectedExercise={setSelectedExercise}
            isAnalyzing={isAnalyzing}
            selectedFile={selectedFile}
            fileInputRef={fileInputRef}
            handleFileSelect={handleFileSelect}
            resetAnalysis={resetAnalysis}
            exercises={exercises}
            analysisResult={analysisResult}
            error={error}
          />
        )}
        {currentPage === 'about' && <AboutPage />}
        {currentPage === 'contact' && <ContactPage />}
      </main>
    </div>
  );
};

export default FitPoseApp;