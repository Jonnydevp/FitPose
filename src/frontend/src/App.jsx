import React, { useState, useRef } from 'react';

// Simple SVG icon components
const Upload = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
  </svg>
);

const CheckCircle = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const Loader = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
  </svg>
);

const Dumbbell = ({ className }) => (
  <svg className={className} fill="currentColor" viewBox="0 0 24 24">
    <path d="M20.57 14.86L22 13.43 20.57 12 17 15.57 8.43 7 12 3.43 10.57 2 9.14 3.43 7.71 2 5.57 4.14 4.14 2.71 2.71 4.14l1.43 1.43L2 7.71l1.43 1.43L2 10.57 3.43 12 7 8.43 15.57 17 12 20.57 13.43 22l1.43-1.43L16.29 22l2.14-2.14 1.43 1.43 1.43-1.43-1.43-1.43L22 16.29l-1.43-1.43z"/>
  </svg>
);

const Mail = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
  </svg>
);

const Phone = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
  </svg>
);

const MapPin = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
);

const Users = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a4 4 0 11-8 0 4 4 0 018 0z" />
  </svg>
);

const Target = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
  </svg>
);

const Award = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
  </svg>
);

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

  const renderHome = () => (
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
              <div key={index} className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:border-purple-400/50 transition-all duration-300">
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

  const renderAbout = () => (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 py-24">
      {/* Remove max-w-4xl wrapper */}
      <div className="text-center mb-16">
        <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
          About FitPose
        </h1>
        <p className="text-xl text-gray-300 max-w-2xl mx-auto">
          Revolutionizing fitness through AI-powered form analysis
        </p>
      </div>

      <div className="bg-white/10 backdrop-blur-lg rounded-3xl border border-white/20 p-12 shadow-2xl">
        <div className="prose prose-lg prose-invert max-w-none">
          <p className="text-gray-300 text-lg leading-relaxed mb-6">
            FitPose was born from a simple yet powerful idea: everyone deserves access to professional-quality fitness coaching. Using cutting-edge computer vision and machine learning technologies, we analyze your exercise form in real-time, providing instant feedback that helps you train safer and more effectively.
          </p>
          
          <p className="text-gray-300 text-lg leading-relaxed mb-6">
            Our AI has been trained on thousands of hours of exercise footage, learning from certified trainers and physiotherapists to provide you with accurate, actionable insights. Whether you're a beginner learning proper form or an athlete fine-tuning your technique, FitPose adapts to your level and goals.
          </p>

          <p className="text-gray-300 text-lg leading-relaxed">
            Join the fitness revolution and discover how technology can transform your workout experience. Perfect your form, prevent injuries, and achieve your fitness goals faster than ever before.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mt-12 pt-8 border-t border-white/20">
          <div className="text-center">
            <div className="text-4xl font-bold text-purple-400 mb-2">50K+</div>
            <div className="text-gray-300">Videos Analyzed</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-pink-400 mb-2">95%</div>
            <div className="text-gray-300">Accuracy Rate</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-emerald-400 mb-2">24/7</div>
            <div className="text-gray-300">Available</div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderContact = () => (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 py-24">
      <div className="w-full text-center mb-16">
        <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
          Contact Us
        </h1>
        <p className="text-xl text-gray-300 max-w-2xl mx-auto">
          Have questions? We'd love to hear from you. Get in touch with our team.
        </p>
      </div>

      {/* Add this wrapper for consistent width */}
        <div className="w-screen grid md:grid-cols-2 gap-8">
          {/* Contact Form */}
          <div className="w-full h-full bg-white/10 backdrop-blur-lg rounded-3xl border border-white/20 p-8 shadow-2xl flex flex-col">
            <h2 className="text-2xl font-bold text-white mb-6">Send us a message</h2>
            <div className="space-y-6">
              <div>
                <input
                  type="text"
                  placeholder="Your Name"
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>
              <div>
                <input
                  type="email"
                  placeholder="Your Email"
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>
              <div>
                <textarea
                  rows={5}
                  placeholder="Your Message"
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                ></textarea>
              </div>
              <button
                onClick={() => alert('Message sent! We\'ll get back to you soon.')}
                className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-105"
              >
                Send Message
              </button>
            </div>
          </div>

          {/* Contact Information */}
          <div className="w-full h-full space-y-8 flex flex-col">
            <div className="bg-white/10 backdrop-blur-lg rounded-3xl border border-white/20 p-8 shadow-2xl">
              <h2 className="text-2xl font-bold text-white mb-6">Get in touch</h2>
              <div className="space-y-6">
                <div className="flex items-center space-x-4">
                  <div className="bg-purple-600 rounded-full p-3">
                    <Mail className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <p className="text-white font-semibold">Email</p>
                    <p className="text-gray-300">hello@fitpose.ai</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="bg-pink-600 rounded-full p-3">
                    <Phone className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <p className="text-white font-semibold">Phone</p>
                    <p className="text-gray-300">+1 (555) 123-4567</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="bg-emerald-600 rounded-full p-3">
                    <MapPin className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <p className="text-white font-semibold">Address</p>
                    <p className="text-gray-300">123 Fitness Street<br />Tech City, TC 12345</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white/10 backdrop-blur-lg rounded-3xl border border-white/20 p-8 shadow-2xl">
              <h3 className="text-xl font-bold text-white mb-4">Office Hours</h3>
              <div className="space-y-2 text-gray-300">
                <p>Monday - Friday: 9:00 AM - 6:00 PM</p>
                <p>Saturday: 10:00 AM - 4:00 PM</p>
                <p>Sunday: Closed</p>
              </div>
            </div>
          </div>
        </div>
    </div>
  );

  return (
    <div className="w-full">
      {/* Navigation */}
      <nav className="fixed top-6 left-1/2 transform -translate-x-1/2 z-50">
      <div className="bg-white/20 backdrop-blur-lg rounded-full px-2 py-2 border border-white/30">
        <div className="flex items-center space-x-2">
          {/* Logo */}
          <div className="flex items-center space-x-2 px-4">
            <div className="p-2 bg-purple-600/40 rounded-full">
              <Dumbbell className="h-5 w-5 text-white" />
            </div>
            <span className="text-white font-bold text-lg hidden sm:inline">
              Fit<span className="text-purple-300">Pose</span>
            </span>
          </div>
          
          {/* Navigation Links */}
          <div className="flex space-x-2">
            {['home', 'about', 'contact'].map((page) => (
              <button
                key={page}
                onClick={() => setCurrentPage(page)}
                className={`px-4 sm:px-6 py-2 rounded-full text-sm font-medium transition-all duration-300 capitalize ${
                  currentPage === page
                    ? 'bg-purple-600 text-white shadow-lg'
                    : 'text-purple-800 hover:bg-white/30'
                }`}
              >
                {page}
              </button>
            ))}
          </div>
        </div>
      </div>
    </nav>

      {/* Main Content */}
      <main>
          {currentPage === 'home' && renderHome()}
          {currentPage === 'about' && renderAbout()}
          {currentPage === 'contact' && renderContact()}
      </main>
    </div>
  );
};

export default FitPoseApp;