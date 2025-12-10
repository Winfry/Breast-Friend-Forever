from fastapi import FastAPI
import time
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# Import all endpoint routers
from app.api.endpoints import chatbot, hospitals, resources, encouragement, self_exam, mobile, agentic_chatbot, symptom_checker, journal, reminders
from app.core.config import settings

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Breast Friend Forever API",
    description="A compassionate backend for breast health education and support",
    version="1.0.0",
    docs_url="/docs",  # 📚 Auto-generated documentation
    redoc_url="/redoc" # 📖 Alternative documentation
)

# CORS Middleware - Allow frontends to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000", 
        "http://192.168.1.118:8000",  # Your computer's IP
        "http://localhost:8081",
        "exp://192.168.1.118:8081",   # Your Expo URL
        "http://192.168.1.118:8081",
        "*"  # For development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Mount static files for PDF downloads
app.mount("/static", StaticFiles(directory="app/data"), name="static")

#  Connect all API routers to the main app
app.include_router(chatbot.router, prefix="/api/v1/chat", tags=["Chatbot"])
app.include_router(agentic_chatbot.router, prefix="/api/v1/chatbot", tags=["Agentic Chatbot"])  # 🤖 New agentic RAG endpoint
app.include_router(hospitals.router, prefix="/api/v1/hospitals", tags=["Hospitals"])
app.include_router(resources.router, prefix="/api/v1/resources", tags=["Resources"])
app.include_router(encouragement.router, prefix="/api/v1/encouragement", tags=["Encouragement"])
app.include_router(self_exam.router, prefix="/api/v1/self_exam", tags=["Self Exam"])
app.include_router(mobile.router, prefix="/api/v1/mobile", tags=["Mobile"])
app.include_router(symptom_checker.router, prefix="/api/v1/symptom-check", tags=["Symptom Checker"])
app.include_router(journal.router, prefix="/api/v1/journal", tags=["Journal"])
app.include_router(reminders.router, prefix="/api/v1/reminders", tags=["Reminders"])

# Root endpoint - API welcome message
@app.get("/")
async def root():
    return {
        "message": "Breast Friend Forever API is running! 💖",
        "version": "1.0.0",
        "endpoints": {
            "chatbot": "/api/v1/chat",
            "agentic_chatbot": "/api/v1/chatbot/agentic",
            "hospitals": "/api/v1/hospitals",
            "resources": "/api/v1/resources",
            "encouragement": "/api/v1/encouragement",
            "self_exam": "/api/v1/self_exam"
        },
        "documentation": "/docs",
        "new_features": {
            "agentic_rag": "Intelligent AI assistant with routing, web search, and verification"
        }
    }

# Health check endpoint - for monitoring
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "breast-health-api"}

# Add request logging middleware (add this after CORS)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log the incoming request
    print(f"[REQ] [{time.strftime('%H:%M:%S')}] {request.method} {request.url}")
    print(f"   Origin: {request.headers.get('origin', 'No origin')}")
    print(f"   User-Agent: {request.headers.get('user-agent', 'No agent')}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    print(f"   Response: {response.status_code} ({process_time:.2f}s)")
    print("   " + "-" * 40)
    
    return response

# Add mobile-specific test endpoint
@app.get("/api/v1/mobile-test")
async def mobile_test():
    return {
        "message": "🎉 Mobile connection successful!",
        "timestamp": time.time(),
        "your_ip": "192.168.1.118",
        "endpoints": {
            "chat": "/api/v1/chat/",
            "hospitals": "/api/v1/hospitals/", 
            "resources": "/api/v1/resources/",
            "encouragement": "/api/v1/encouragement/",
            "self_exam": "/api/v1/self_exam/"
        },
        "instructions": "Use these endpoints in your mobile app"
    }

# Server entry point (when running directly)
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        access_log=True
    )

@app.get("/")
async def root():
    return {
        "message": "Breast-Friend-Forever API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
