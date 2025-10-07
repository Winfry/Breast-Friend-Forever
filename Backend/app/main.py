from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import chatbot, hospitals, resources, encouragement
from app.core.config import settings

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Breast Friend Forever API",
    description="A compassionate backend for breast health education and support",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 🔒 CORS Middleware - Allow both Flutter and Streamlit to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: ["https://yourapp.com", "http://localhost:8501"]
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # All headers
)

# 📊 Mount static files for PDF downloads
app.mount("/static", StaticFiles(directory="app/data"), name="static")

# 🔗 Include all API routers
app.include_router(chatbot.router, prefix="/api/v1/chat", tags=["Chatbot"])
app.include_router(hospitals.router, prefix="/api/v1/hospitals", tags=["Hospitals"])
app.include_router(resources.router, prefix="/api/v1/resources", tags=["Resources"])
app.include_router(encouragement.router, prefix="/api/v1/encouragement", tags=["Encouragement"])

# 🏠 Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Breast Friend Forever API is running! 💖",
        "version": "1.0.0",
        "endpoints": {
            "chatbot": "/api/v1/chat",
            "hospitals": "/api/v1/hospitals", 
            "resources": "/api/v1/resources",
            "encouragement": "/api/v1/encouragement"
        }
    }

# ❤️ Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "breast-health-api"}

# 🚀 Server entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)