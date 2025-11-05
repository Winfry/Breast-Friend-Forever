// Exact API configuration matching your FastAPI backend
export const API_CONFIG = {
  BASE_URL: 'http://192.168.1.118:8000', // Your computer's current IP address
  ENDPOINTS: {
    // Exact endpoints matching backend routes
    CHAT: '/api/v1/chat/message',
    HOSPITALS: '/api/v1/hospitals/',
    RESOURCES: '/api/v1/resources/',
    ENCOURAGEMENT: '/api/v1/encouragement/',
    SELF_EXAM: '/api/v1/self_exam/steps',
    MOBILE: '/api/v1/mobile/',
    HEALTH: '/health',
    MOBILE_TEST: '/api/v1/mobile-test'
  },
  // Colors from your Streamlit app
  COLORS: {
    PRIMARY: '#e91e63',    // Your pink from Streamlit
    SECONDARY: '#f8bbd0',  // Light pink
    BACKGROUND: '#f5f5f5', // Light gray
    CARD_BACKGROUND: '#FCE4EC' // Light pink card background
  }
};