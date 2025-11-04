// src/utils/constants.js
import Colors from '../styles/colors';

export const AppConstants = {
  APP_NAME: 'Breast Friend Forever',
  VERSION: '1.0.0',
  
  // API Configuration
  API_TIMEOUT: 15000,
  MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
  
  // Chat constants
  MAX_MESSAGE_LENGTH: 500,
  TYPING_INDICATOR_DELAY: 1000,
  
  // Storage keys
  STORAGE_KEYS: {
    USER_PREFERENCES: 'user_preferences',
    CHAT_HISTORY: 'chat_history',
    FAVORITE_RESOURCES: 'favorite_resources',
  },
  
  // Feature flags
  FEATURES: {
    COMMUNITY_POSTS: true,
    OFFLINE_MODE: true,
    PUSH_NOTIFICATIONS: false,
  },
};

export const HospitalFilters = {
  ALL: 'all',
  SCREENING: 'screening',
  SUPPORT: 'support',
  EMERGENCY: 'emergency',
};

export const ResourceTypes = {
  PDF: 'PDF Guide',
  VIDEO: 'Video',
  ARTICLE: 'Article',
  WEBSITE: 'Website',
  CONTACT: 'Contact',
};

export const SelfExamSteps = {
  VISUAL_INSPECTION: 1,
  ARM_MOVEMENT: 2,
  DISCHARGE_CHECK: 3,
  LYING_DOWN: 4,
  CIRCULAR_MOTION: 5,
  PATTERN_COVERAGE: 6,
  SHOWER_CHECK: 7,
};

export default {
  AppConstants,
  HospitalFilters,
  ResourceTypes,
  SelfExamSteps,
};