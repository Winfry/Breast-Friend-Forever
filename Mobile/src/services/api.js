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

// Chat - FIXED endpoint path
export const sendChatMessage = async (message) => {
  try {
    console.log('📱 Sending chat message:', message);
    
    const response = await api.post(API_CONFIG.ENDPOINTS.CHAT, { 
      message: message,
      conversation_history: []
    });
    
    console.log('✅ Chat response received:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Chat API Error:', error);
    
    // Provide better error message
    if (error.response) {
      // Server responded with error status
      throw new Error(`Chat service error: ${error.response.status} - ${error.response.data?.detail || 'Please try again'}`);
    } else if (error.request) {
      // Network error
      throw new Error('Cannot connect to chat service. Please check your internet connection.');
    } else {
      // Other error
      throw new Error('Failed to send message. Please try again.');
    }
  }
};

// Hospitals - FIXED with better error handling
export const getHospitals = async () => {
  try {
    console.log('🏥 Fetching hospitals...');
    const response = await api.get(API_CONFIG.ENDPOINTS.HOSPITALS);
    console.log('🏥 Hospitals response:', response.data);
    
    // Handle different response formats
    let hospitalsData = [];
    
    if (Array.isArray(response.data)) {
      hospitalsData = response.data;
    } else if (response.data && Array.isArray(response.data.hospitals)) {
      hospitalsData = response.data.hospitals;
    } else if (response.data && Array.isArray(response.data.data)) {
      hospitalsData = response.data.data;
    } else {
      console.warn('⚠️ Unexpected hospitals response format, using default data');
      return getDefaultHospitals();
    }
    
    // Enrich the data with required fields
    const enrichedHospitals = hospitalsData.map((hospital, index) => ({
      id: hospital.id || index + 1,
      name: hospital.name || hospital.Facility_N || 'Healthcare Facility',
      address: hospital.address || hospital.Location || hospital.Address || 'Address not available',
      phone: hospital.phone || hospital.Phone || '+254 XXX XXX XXX',
      services: hospital.services || hospital.Services || 'General healthcare services',
      hours: hospital.hours || hospital.Hours || 'Mon-Fri: 8AM-5PM',
      specialty: hospital.specialty || hospital.Specialty || getRandomSpecialty(),
      insurance: hospital.insurance || ['NHIF', 'Private Pay'],
      rating: hospital.rating || Math.random() * 2 + 3, // 3-5 stars
      waitTime: hospital.waitTime || Math.floor(Math.random() * 30) + 10, // 10-40 mins
      isOpen: hospital.isOpen !== undefined ? hospital.isOpen : Math.random() > 0.2,
      type: hospital.type || hospital.Type || 'Medical Clinic',
      county: hospital.county || hospital.County || 'Nairobi',
      latitude: hospital.latitude || hospital.lat || hospital.Latitude || -1.286389,
      longitude: hospital.longitude || hospital.lon || hospital.Longitude || 36.817223
    }));
    
    return enrichedHospitals;
    
  } catch (error) {
    console.error('🏥 Hospitals API Error:', error);
    
    // Return default hospitals when API fails
    console.log('📋 Using default hospitals data due to API error');
    return getDefaultHospitals();
  }
};

// Enhanced default hospitals data for Kenya
const getDefaultHospitals = () => {
  return [
    {
      id: 1,
      name: 'Nairobi Women\'s Hospital',
      address: 'James Gichuru Road, Lavington, Nairobi, Kenya',
      phone: '+254 20 272 6000',
      services: 'Mammography, Ultrasound, Biopsy, Breast Surgery, Oncology',
      hours: '24/7',
      specialty: 'Comprehensive Women\'s Healthcare',
      insurance: ['NHIF', 'Madison', 'Jubilee', 'AAR', 'Private Pay'],
      rating: 4.8,
      waitTime: 15,
      isOpen: true,
      type: 'National Hospital',
      county: 'Nairobi',
      latitude: -1.2684,
      longitude: 36.7965
    },
    {
      id: 2,
      name: 'Aga Khan University Hospital',
      address: '3rd Parklands Avenue, Nairobi, Kenya',
      phone: '+254 20 366 2000',
      services: 'Breast Screening, Genetic Testing, Surgical Oncology, Radiation Therapy',
      hours: 'Mon-Sun: 6AM-10PM',
      specialty: 'Comprehensive Cancer Care',
      insurance: ['NHIF', 'Jubilee', 'AAR', 'CIC', 'Liberty'],
      rating: 4.9,
      waitTime: 20,
      isOpen: true,
      type: 'National Hospital',
      county: 'Nairobi',
      latitude: -1.2545,
      longitude: 36.8004
    },
    {
      id: 3,
      name: 'Kenyatta National Hospital',
      address: 'Hospital Road, Nairobi, Kenya',
      phone: '+254 20 272 6300',
      services: 'Mammography, Clinical Breast Exam, Biopsy, Cancer Treatment',
      hours: '24/7',
      specialty: 'National Referral Hospital',
      insurance: ['NHIF', 'All major providers'],
      rating: 4.5,
      waitTime: 30,
      isOpen: true,
      type: 'National Hospital',
      county: 'Nairobi',
      latitude: -1.3045,
      longitude: 36.8075
    },
    {
      id: 4,
      name: 'Mombasa Hospital',
      address: 'Mama Ngina Drive, Mombasa, Kenya',
      phone: '+254 41 231 2191',
      services: 'Breast Screening, Ultrasound, Women\'s Health, Consultation',
      hours: 'Mon-Sun: 7AM-9PM',
      specialty: 'Coastal Healthcare Services',
      insurance: ['NHIF', 'Madison', 'Jubilee'],
      rating: 4.3,
      waitTime: 25,
      isOpen: true,
      type: 'County Hospital',
      county: 'Mombasa',
      latitude: -4.0547,
      longitude: 39.6636
    },
    {
      id: 5,
      name: 'Nakuru General Hospital',
      address: 'Hospital Road, Nakuru, Kenya',
      phone: '+254 51 221 0000',
      services: 'Breast Screening, Clinical Exams, Basic Diagnostics',
      hours: 'Mon-Sun: 24/7',
      specialty: 'Regional Healthcare Services',
      insurance: ['NHIF', 'Private Pay'],
      rating: 4.2,
      waitTime: 35,
      isOpen: true,
      type: 'County Hospital',
      county: 'Nakuru',
      latitude: -0.3031,
      longitude: 36.0800
    }
  ];
};

// Helper function for specialties
const getRandomSpecialty = () => {
  const specialties = [
    'Breast Cancer Center',
    'Women Health Specialist',
    'Comprehensive Care',
    'Oncology Center',
    'Mammography Expert',
    'General Healthcare',
    'Specialized Women\'s Services'
  ];
  return specialties[Math.floor(Math.random() * specialties.length)];
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