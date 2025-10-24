// mobile/src/utils/helpers.js - Utility functions
import { Linking, Alert } from 'react-native';

/**
 * Open URL in browser
 */
export const openURL = async (url) => {
  try {
    const supported = await Linking.canOpenURL(url);
    if (supported) {
      await Linking.openURL(url);
    } else {
      Alert.alert('Error', 'Cannot open this link');
    }
  } catch (error) {
    Alert.alert('Error', 'Failed to open link');
  }
};

/**
 * Format distance for display
 */
export const formatDistance = (distance) => {
  return `${distance} away`;
};

/**
 * Get time ago string from date
 */
export const getTimeAgo = (timestamp) => {
  const now = new Date();
  const diff = now - new Date(timestamp);
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
  if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
  if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
  return 'Just now';
};

/**
 * Capitalize first letter
 */
export const capitalize = (str) => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};