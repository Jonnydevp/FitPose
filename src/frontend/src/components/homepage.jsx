import React from 'react';
import { Loader, CheckCircle, Upload, Target, Award, Users } from '../assets/svgicons.jsx';

const HomePage = ({
  analysisComplete,
  selectedExercise,
  setSelectedExercise,
  isAnalyzing,
  selectedFile,
  fileInputRef,
  handleFileSelect,
  resetAnalysis,
  exercises
}) => (
  <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
    <div className="relative overflow-hidden py-24">
      <div className="absolute inset-0 bg-gradient-to-r from-purple-600/20 to-pink-600/20"></div>
      <div className="relative px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            FitPose
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-3xl mx-auto">
            AI-powered form analysis to perfect your workouts. Upload your exercise video and get instant feedback.
          </p>
        </div>

        {/* Analysis Section */}
        <div className="relative max-w-2xl mx-auto">
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl border border-white/20 p-8 shadow-2xl">
            {!analysisComplete ? (
              <div className="space-y-6">
                {/* Exercise Dropdown */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-3">
                    Select Exercise
                  </label>
                  <select
                    value={selectedExercise}
                    onChange={(e) => setSelectedExercise(e.target.value)}
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    disabled={isAnalyzing}
                  >
                    <option value="">Choose an exercise...</option>
                    {exercises.map((exercise) => (
                      <option key={exercise} value={exercise} className="bg-slate-800">
                        {exercise}
                      </option>
                    ))}
                  </select>
                </div>

                {/* File Upload */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-3">
                    Upload Video (MP4)
                  </label>
                  <div 
                    className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${
                      selectedFile ? 'border-green-400 bg-green-400/10' : 'border-purple-400 bg-purple-400/5 hover:bg-purple-400/10'
                    }`}
                  >
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="video/mp4"
                      onChange={handleFileSelect}
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      disabled={!selectedExercise || isAnalyzing}
                    />
                    
                    {isAnalyzing ? (
                      <div className="flex flex-col items-center">
                        <Loader className="h-12 w-12 text-purple-400 animate-spin mb-4" />
                        <p className="text-white font-medium">Analyzing your form...</p>
                        <p className="text-gray-400 text-sm mt-2">This may take a few moments</p>
                      </div>
                    ) : selectedFile ? (
                      <div className="flex flex-col items-center">
                        <CheckCircle className="h-12 w-12 text-green-400 mb-4" />
                        <p className="text-white font-medium">{selectedFile.name}</p>
                        <p className="text-gray-400 text-sm mt-2">File ready for analysis</p>
                      </div>
                    ) : (
                      <div className="flex flex-col items-center">
                        <Upload className="h-12 w-12 text-purple-400 mb-4" />
                        <p className="text-white font-medium">Click to upload your exercise video</p>
                        <p className="text-gray-400 text-sm mt-2">
                          {selectedExercise ? 'MP4 files only' : 'Please select an exercise first'}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center space-y-6">
                <div className="flex justify-center">
                  <div className="bg-gradient-to-r from-green-400 to-emerald-500 rounded-full p-4">
                    <CheckCircle className="h-12 w-12 text-white" />
                  </div>
                </div>
                <h3 className="text-2xl font-bold text-white">Analysis Complete!</h3>
                <p className="text-gray-300">
                  Your {selectedExercise.toLowerCase()} form has been analyzed. Results are ready!
                </p>
                <div className="bg-white/5 rounded-xl p-6 text-left">
                  <h4 className="text-lg font-semibold text-white mb-3">Analysis Results:</h4>
                  <ul className="space-y-2 text-gray-300">
                    <li>• Form accuracy: 85% - Good job!</li>
                    <li>• Posture alignment: Excellent</li>
                    <li>• Range of motion: 92%</li>
                    <li>• Recommendations: Keep your core engaged throughout the movement</li>
                  </ul>
                </div>
                <button
                  onClick={resetAnalysis}
                  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-105"
                >
                  Analyze Another Video
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>

    {/* Features Section */}
    <div className="py-24 bg-black/20">
      <div className="px-4 sm:px-6 lg:px-8">
        <h2 className="text-4xl font-bold text-center text-white mb-16">
          Why Choose FitPose?
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          {[
            {
              icon: <Target className="h-8 w-8" />,
              title: "Precision Analysis",
              description: "Advanced AI algorithms analyze your form with surgical precision"
            },
            {
              icon: <Award className="h-8 w-8" />,
              title: "Expert Feedback",
              description: "Get professional-level coaching recommendations instantly"
            },
            {
              icon: <Users className="h-8 w-8" />,
              title: "Progress Tracking",
              description: "Monitor your improvement over time with detailed analytics"
            }
          ].map((feature, index) => (
            <div
              key={index}
              className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:border-purple-400/50 transition-all duration-300"
            >
              <div className="text-purple-400 mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
              <p className="text-gray-300">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
);

export default HomePage;