import React from 'react';
import { Mail, Phone, MapPin } from '../assets/svgicons.jsx';

const ContactPage = () => (
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

  export default ContactPage;