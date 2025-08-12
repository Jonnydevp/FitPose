import React from 'react';
import { Dumbbell } from '../assets/svgicons.jsx';

const Navbar = ({ currentPage, setCurrentPage }) => (
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
);

export default Navbar;