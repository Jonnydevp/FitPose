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
  const fileInputRef = useRef(null);

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

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'video/mp4') {
      setSelectedFile(file);
      // Simulate file upload and analysis
      setIsAnalyzing(true);
      setTimeout(() => {
        setIsAnalyzing(false);
        setAnalysisComplete(true);
      }, 3000);
    }
  };

  const resetAnalysis = () => {
    setSelectedFile(null);
    setIsAnalyzing(false);
    setAnalysisComplete(false);
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
          />
        )}
        {currentPage === 'about' && <AboutPage />}
        {currentPage === 'contact' && <ContactPage />}
      </main>
    </div>
  );
};

export default FitPoseApp;