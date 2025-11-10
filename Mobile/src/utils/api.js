// mobile/src/utils/api.js - API service for RAG backend
import axios from 'axios';

// Configuration - UPDATE THESE WITH YOUR ACTUAL BACKEND URLS
const API_CONFIG = {
  // For development - replace with your actual backend URL
  baseURL: 'http://192.168.1.126:8000', // Your computer's IP for mobile testing
  timeout: 30000, // 30 seconds timeout for AI responses
  headers: {
    'Content-Type': 'application/json',
  }
};

// Create axios instance
const api = axios.create(API_CONFIG);

// API Service for Breast Friend Forever
export const apiService = {
  /**
   * Send message to RAG backend and get AI response
   * @param {string} message - User's message
   * @param {string} userId - Optional user ID for context
   */
  async sendChatMessage(message, userId = null) {
    try {
      console.log('Sending message to RAG backend:', message);
      
      const payload = {
        message: message,
        user_id: userId,
        timestamp: new Date().toISOString(),
        source: 'mobile_app'
      };

      // Adjust the endpoint based on your RAG backend API
      const response = await api.post('/api/chat', payload);
      
      console.log('Received response from backend:', response.data);
      return response.data;
      
    } catch (error) {
      console.error('API Error:', error);
      
      // Provide fallback responses based on error type
      if (error.code === 'NETWORK_ERROR') {
        throw new Error('Network connection failed. Please check your internet connection.');
      } else if (error.response?.status === 404) {
        throw new Error('Service temporarily unavailable. Please try again later.');
      } else {
        throw new Error('Unable to connect to our knowledge base. Please try again.');
      }
    }
  },

  /**
   * Health check for backend connection
   */
  async healthCheck() {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  },

  /**
   * Get conversation history (if your backend supports it)
   */
  async getConversationHistory(userId) {
    try {
      const response = await api.get(`/api/conversations/${userId}`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch conversation history:', error);
      throw error;
    }
  }
};

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('Response interceptor error:', error);
    return Promise.reject(error);
  }
);

export default apiService;