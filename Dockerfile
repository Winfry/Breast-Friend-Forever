# Use official Python runtime
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pillow  # For icon generation

# Copy backend code
COPY backend/ ./backend/

# Copy frontend code
COPY frontend/ ./frontend/

# Create necessary directories
RUN mkdir -p frontend/static/icons

# Generate PWA icons using Python
RUN python3 -c '''
from PIL import Image, ImageDraw
import os

# Create icons directory if it doesn\'t exist
os.makedirs(\'/app/frontend/static/icons\', exist_ok=True)

sizes = [72, 96, 128, 144, 152, 192, 384, 512]
for size in sizes:
    # Create a pink background with white circle (BFF logo style)
    img = Image.new(\'RGB\', (size, size), \'#FF69B4\')
    draw = ImageDraw.Draw(img)
    
    # Draw a white circle in the center
    center = size // 2
    radius = size // 3  # Slightly larger circle
    
    # Draw the circle
    draw.ellipse([
        center - radius, 
        center - radius, 
        center + radius, 
        center + radius
    ], fill=\'white\')
    
    # Save the icon
    img.save(f\'/app/frontend/static/icons/icon-{size}x{size}.png\')
    print(f\'Generated icon: {size}x{size}\')
'''

# Create static files directory for FastAPI
RUN mkdir -p backend/app/static && \
    cp -r frontend/* backend/app/static/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]