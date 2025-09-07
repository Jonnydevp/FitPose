#!/bin/bash

# Quality check script for FitPose project
echo "🔍 Running quality checks for FitPose..."

# Check for Russian text in code files
echo "📝 Checking for Russian text..."
if grep -r "[\u0400-\u04FF]" --include="*.py" --include="*.js" --include="*.jsx" src/ main.py 2>/dev/null; then
    echo "❌ Found Russian text in code files"
    exit 1
else
    echo "✅ No Russian text found"
fi

# Check Python syntax
echo "🐍 Checking Python syntax..."
python -m py_compile main.py
for file in $(find src/ -name "*.py"); do
    python -m py_compile "$file"
done
echo "✅ Python syntax OK"

# Check if all required files exist
echo "📁 Checking required files..."
required_files=(
    "main.py"
    "requirements.txt"
    "railway.toml"
    "Procfile"
    ".env.example"
    "src/backend/core/config.py"
    "src/backend/api/exercise_routes.py"
    "src/frontend/package.json"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing required file: $file"
        exit 1
    fi
done
echo "✅ All required files present"

# Check environment variables
echo "🔧 Checking environment setup..."
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found (create from .env.example)"
fi

echo "🎉 Quality check completed successfully!"
