from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# 🛣️ Import all endpoint routers
from app.api.endpoints import chatbot, hospitals, resources, encouragement, self_exam
from app.core.config import settings

# 🏗️ Initialize FastAPI app with metadata
app = FastAPI(
    title="Breast Friend Forever API",
    description="A compassionate backend for breast health education and support",
    version="1.0.0",
    docs_url="/docs",  # 📚 Auto-generated documentation
    redoc_url="/redoc" # 📖 Alternative documentation
)

# 🌐 CORS Middleware - Allow frontends to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specific domains only
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # All headers
)

# 📁 Mount static files for PDF downloads
app.mount("/static", StaticFiles(directory="app/data"), name="static")

# 🔗 Connect all API routers to the main app
app.include_router(chatbot.router, prefix="/api/v1/chat", tags=["Chatbot"])
app.include_router(hospitals.router, prefix="/api/v1/hospitals", tags=["Hospitals"])
app.include_router(resources.router, prefix="/api/v1/resources", tags=["Resources"])
app.include_router(encouragement.router, prefix="/api/v1/encouragement", tags=["Encouragement"])
app.include_router(self_exam.router, prefix="/api/v1/self_exam", tags=["Self Exam"])

# 🏠 Root endpoint - API welcome message
@app.get("/")
async def root():
    return {
        "message": "Breast Friend Forever API is running! 💖",
        "version": "1.0.0",
        "endpoints": {
            "chatbot": "/api/v1/chat",
            "hospitals": "/api/v1/hospitals", 
            "resources": "/api/v1/resources",
            "encouragement": "/api/v1/encouragement",
            "self_exam": "/api/v1/self_exam"
        },
        "documentation": "/docs"
    }

# ❤️ Health check endpoint - for monitoring
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "breast-health-api"}

# 🚀 Server entry point (when running directly)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)