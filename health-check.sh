#!/bin/bash

# Health check script for FitPose API

URL=${1:-"http://localhost:8000"}

echo "🔍 Testing FitPose API at $URL"

# Test health endpoint
echo "📊 Testing /health endpoint..."
curl -s "$URL/health" | python3 -m json.tool

echo ""

# Test root endpoint  
echo "🏠 Testing / endpoint..."
curl -s "$URL/" | python3 -m json.tool

echo ""
echo "✅ Health check completed!"
