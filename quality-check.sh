#!/bin/bash

# Quality check script for FitPose project
echo "Running quality checks for FitPose..."

# Check for Russian (Cyrillic) text in code files (robust across platforms)
echo "Checking for Russian text..."
if command -v rg >/dev/null 2>&1; then
  if rg -n --pcre2 "[\\p{Cyrillic}]" --glob "src/**/*.py" --glob "src/**/*.js" --glob "src/**/*.jsx" main.py; then
    echo "Found Russian text in code files"
    exit 1
  else
    echo "No Russian text found"
  fi
else
  # Fallback to Python-based check if ripgrep is unavailable
  python3 - <<'PY'
import os, sys, re
paths = []
for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith(('.py','.js','.jsx')):
            paths.append(os.path.join(root,f))
paths.append('main.py')
pat = re.compile(r'[\u0400-\u04FF]')
found = False
for p in paths:
    try:
        with open(p,'r',encoding='utf-8', errors='ignore') as fh:
            for i, line in enumerate(fh,1):
                if pat.search(line):
                    print(f"{p}:{i}:{line.rstrip()}")
                    found = True
    except Exception:
        pass
sys.exit(1 if found else 0)
PY
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "Found Russian text in code files"
    exit 1
  else
    echo "No Russian text found"
  fi
fi

# Check Python syntax (Python 3)
echo "Checking Python syntax..."
python3 -m py_compile main.py
for file in $(find src/ -name "*.py"); do
    python3 -m py_compile "$file"
done
echo "Python syntax OK"

# Check if all required files exist
echo "Checking required files..."
required_files=(
    "main.py"
    "requirements.txt"
    "railway.toml"
    ".env.example"
    "src/backend/core/config.py"
    "src/backend/api/exercise_routes.py"
    "src/frontend/package.json"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "Missing required file: $file"
        exit 1
    fi
done
echo "All required files present"

# Check environment variables
echo "Checking environment setup..."
if [ ! -f ".env" ]; then
    echo ".env file not found (create from .env.example)"
fi

echo "Quality check completed successfully!"
