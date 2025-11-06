// mobile/src/utils/config.js - Updated for your backend structure
const ENV = {
  development: {
    // Replace 192.168.1.100 with your actual computer IP
    API_BASE_URL: 'http://192.168.1.118:8000', // Your computer's IP
  },
  production: {
    API_BASE_URL: 'https://your-production-backend.com',
  }
};

// Determine current environment
const getEnvironment = () => {
  return __DEV__ ? 'development' : 'production';
};

export const CONFIG = ENV[getEnvironment()];

// Backend API endpoints - MATCH YOUR EXISTING ROUTES
export const ENDPOINTS = {
  CHAT: '/api/v1/chat/', // Note the trailing slash to match your router
  HEALTH: '/health',
  CONVERSATIONS: '/api/v1/chat/conversations', // Adjust based on your actual routes
  RESOURCES: '/api/v1/resources/',
  HOSPITALS: '/api/v1/hospitals/',
  ENCOURAGEMENT: '/api/v1/encouragement/',
  SELF_EXAM: '/api/v1/self_exam/'
};