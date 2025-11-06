// src/services/apiConstants.js - Updated with correct endpoints
export const API_CONFIG = {
  // Use your actual backend IP address - IMPORTANT!
  // BASE_URL: 'http://192.168.100.5:8000', // Replace with your computer's IP
  BASE_URL: 'http://localhost:8000', // For development
  // BASE_URL: 'https://your-backend-domain.com', // For production
  
  ENDPOINTS: {
    CHAT: '/api/v1/chat/',
    HOSPITALS: '/api/v1/hospitals/',
    RESOURCES: '/api/v1/resources/',
    ENCOURAGEMENT: '/api/v1/encouragement/',
    SELF_EXAM: '/api/v1/self_exam/',
    HEALTH: '/health',
    MOBILE_TEST: '/api/v1/mobile-test'
  },
  
  COLORS: {
    PRIMARY: '#E91E63',
    SECONDARY: '#9C27B0',
    SUCCESS: '#4CAF50',
    WARNING: '#FF9800',
    ERROR: '#F44336',
    BACKGROUND: '#F8F9FA'
  },
  
  TIMEOUTS: {
    DEFAULT: 10000,
    CHAT: 15000,
    UPLOAD: 30000
  }
};