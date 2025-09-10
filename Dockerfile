FROM python:3.11-slim

# Environment for reliable headless CV
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    MEDIAPIPE_DISABLE_GPU=1 \
    OPENCV_DISABLE_GPU=1 \
    LIBGL_ALWAYS_SOFTWARE=1 \
    MESA_LOADER_DRIVER_OVERRIDE=llvmpipe

# Minimal system deps for OpenCV/MediaPipe headless
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        libgomp1 \
        libgl1 \
        libglx-mesa0 \
        libgl1-mesa-dri \
        libegl1 \
        libgles2 \
        libx11-6 \
        libx11-xcb1 \
        libxfixes3 \
        libxcb1 \
        libxau6 \
        libxdmcp6 \
        libstdc++6 \
        libgcc-s1 \
    && ldconfig \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . .

# Expose not strictly needed for Railway, but informative
EXPOSE 8000

# Start uvicorn reading PORT from environment (works even without shell interpolation)
CMD ["python","-c","import os,uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=int(os.environ.get('PORT','8000')))"]
