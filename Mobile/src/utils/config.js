// mobile/src/utils/config.js - Environment configuration
const ENV = {
  development: {
    API_BASE_URL: 'http://192.168.100.5:8000', // Local development
    // API_BASE_URL: 'http://192.168.1.100:8000', // Local network
  },
  production: {
    API_BASE_URL: 'https://your-production-backend.com', // Production backend
  }
};

// Determine current environment
const getEnvironment = () => {
  // You can use __DEV__ in React Native or other methods to detect environment
  return __DEV__ ? 'development' : 'production';
};

export const CONFIG = ENV[getEnvironment()];

// Backend API endpoints
export const ENDPOINTS = {
  CHAT: '/api/chat',
  HEALTH: '/health',
  CONVERSATIONS: '/api/conversations',
  RESOURCES: '/api/resources',
  HOSPITALS: '/api/hospitals'
};