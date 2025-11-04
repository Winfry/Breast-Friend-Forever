import { API_CONFIG } from './apiConstants';
import axios from 'axios';

const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health check - matches your Streamlit connection check
export const checkBackendHealth = async () => {
  try {
    const response = await api.get(API_CONFIG.ENDPOINTS.HEALTH);
    return response.data.status === 'healthy';
  } catch (error) {
    console.error('Backend health check failed:', error);
    return false;
  }
};

// Chat - matches your FastAPI chatbot endpoint
export const sendChatMessage = async (message) => {
  try {
    const response = await api.post(API_CONFIG.ENDPOINTS.CHAT, { 
      message: message 
    });
    return response.data;
  } catch (error) {
    console.error('Chat API Error:', error);
    throw new Error('Failed to send message. Please check your connection.');
  }
};

// Resources - matches your FastAPI resources endpoint
export const getResources = async () => {
  try {
    const response = await api.get(API_CONFIG.ENDPOINTS.RESOURCES);
    return response.data;
  } catch (error) {
    console.error('Resources API Error:', error);
    throw error;
  }
};

// Hospitals - matches your FastAPI hospitals endpoint
export const getHospitals = async () => {
  try {
    const response = await api.get(API_CONFIG.ENDPOINTS.HOSPITALS);
    return response.data;
  } catch (error) {
    console.error('Hospitals API Error:', error);
    throw error;
  }
};

// Encouragement - matches your FastAPI encouragement endpoint
export const getEncouragement = async () => {
  try {
    const response = await api.get(API_CONFIG.ENDPOINTS.ENCOURAGEMENT);
    return response.data;
  } catch (error) {
    console.error('Encouragement API Error:', error);
    throw error;
  }
};

// Self Exam - matches your FastAPI self_exam endpoint
export const getSelfExamGuide = async () => {
  try {
    const response = await api.get(API_CONFIG.ENDPOINTS.SELF_EXAM);
    return response.data;
  } catch (error) {
    console.error('Self Exam API Error:', error);
    throw error;
  }
};

// Mobile features - matches your FastAPI mobile endpoint
export const getMobileFeatures = async () => {
  try {
    const response = await api.get(API_CONFIG.ENDPOINTS.MOBILE);
    return response.data;
  } catch (error) {
    console.error('Mobile API Error:', error);
    throw error;
  }
};

export default api;