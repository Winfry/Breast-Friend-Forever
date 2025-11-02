FROM ubuntu:22.04
FROM python:3.9-slim
WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Create directories and generate icons
RUN mkdir -p mobile/static/icons && \
    python -c "
from PIL import Image, ImageDraw
sizes = [72, 96, 128, 144, 152, 192, 384, 512]
for size in sizes:
 img = Image.new('RGB', (size, size), '#FF69B4')
    draw = ImageDraw.Draw(img)
    center = size // 2
    radius = size // 4
    draw.ellipse([center-radius, center-radius, center+radius, center+radius], fill='white')
    img.save(f'mobile/static/icons/icon-{size}x{size}.png')
    "

# Start both services
CMD ["sh", "-c", "cd Backend/app && uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run mobile_app.py --server.port 8501 --server.address 0.0.0.0"]