// src/services/apiConstants.js - Updated with correct endpoints
export const API_CONFIG = {
  // ⚠️ IMPORTANT: Replace with your actual backend IP address
  BASE_URL: 'http://192.168.1.126:8000', // Your computer's IP
  // BASE_URL: 'http://localhost:8000', // For development (web only)
  // BASE_URL: 'https://your-production-domain.com', // For production
  
  ENDPOINTS: {
    // Make sure these match your FastAPI router prefixes
    CHAT: '/api/v1/chat/', // Matches: app.include_router(chatbot.router, prefix="/api/v1/chat")
    HOSPITALS: '/api/v1/hospitals/', // Matches: app.include_router(hospitals.router, prefix="/api/v1/hospitals")
    RESOURCES: '/api/v1/resources/', // Matches: app.include_router(resources.router, prefix="/api/v1/resources")
    ENCOURAGEMENT: '/api/v1/encouragement/', // Matches: app.include_router(encouragement.router, prefix="/api/v1/encouragement")
    SELF_EXAM: '/api/v1/self_exam/', // Matches: app.include_router(self_exam.router, prefix="/api/v1/self_exam")
    MOBILE: '/api/v1/mobile/', // Matches: app.include_router(mobile.router, prefix="/api/v1/mobile")
    HEALTH: '/health', // Your health endpoint
    MOBILE_TEST: '/api/v1/mobile-test' // Your test endpoint
  },
  
  COLORS: {
    PRIMARY: '#E91E63',
    SECONDARY: '#9C27B0',
    SUCCESS: '#4CAF50',
    WARNING: '#FF9800',
    ERROR: '#F44336',
    BACKGROUND: '#F8F9FA'
  }
};