// mobile/src/utils/connectionTest.js - Test backend connection
import { Alert } from 'react-native';
import apiService from './api';

export const testBackendConnection = async () => {
  try {
    const response = await apiService.healthCheck();
    Alert.alert('✅ Connection Successful', 'Mobile app is connected to your backend!');
    return true;
  } catch (error) {
    Alert.alert(
      '❌ Connection Failed', 
      `Cannot connect to backend. Please check:\n\n1. Backend is running\n2. Correct IP address\n3. Network connection\n\nError: ${error.message}`
    );
    return false;
  }
};