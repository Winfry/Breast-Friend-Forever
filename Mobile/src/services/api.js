import { API_CONFIG } from './apiConstants';
import axios from 'axios';

const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: 15000,
});

// Health check (from your Streamlit connection check)
export const checkBackendHealth = async () => {
  try {
    const response = await api.get(API_CONFIG.ENDPOINTS.HEALTH);
    return response.data.status === 'healthy';
  } catch (error) {
    console.error('Backend health check failed:', error);
    return false;
  }
};

// Chat functionality (mirroring Streamlit chat)
export const sendChatMessage = async (message) => {
  try {
    const response = await api.post(API_CONFIG.ENDPOINTS.CHAT, { 
      message: message 
    });
    return response.data;
  } catch (error) {
    console.error('Chat API Error:', error);
    throw new Error('Failed to send message');
  }
};

// Resources (PDFs from your backend)
export const getResources = async () => {
  try {
    const response = await api.get(API_CONFIG.ENDPOINTS.RESOURCES);
    return response.data;
  } catch (error) {
    console.error('Resources API Error:', error);
    throw error;
  }
};

// Hospitals data
export const getHospitals = async () => {
  try {
    const response = await api.get(API_CONFIG.ENDPOINTS.HOSPITALS);
    return response.data;
  } catch (error) {
    console.error('Hospitals API Error:', error);
    throw error;
  }
};

// Encouragement messages
export const getEncouragement = async () => {
  try {
    const response = await api.get(API_CONFIG.ENDPOINTS.ENCOURAGEMENT);
    return response.data;
  } catch (error) {
    console.error('Encouragement API Error:', error);
    throw error;
  }
};

// Self-exam guide
export const getSelfExamGuide = async () => {
  try {
    const response = await api.get(API_CONFIG.ENDPOINTS.SELF_EXAM);
    return response.data;
  } catch (error) {
    console.error('Self Exam API Error:', error);
    throw error;
  }
};

// Mobile-specific features
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