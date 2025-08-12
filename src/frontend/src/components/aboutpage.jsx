import React from 'react';

const AboutPage = () => (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 py-24">
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

export default AboutPage;