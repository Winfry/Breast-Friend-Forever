// mobile/App.js - Main entry point
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';
import AppNavigator from './src/navigation/AppNavigator';

/**
 * Breast Friend Forever - Mobile App
 * 
 * This is the root component that sets up navigation for our
 * breast health companion app with 5 main screens.
 */
export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="auto" />
      <AppNavigator />
    </NavigationContainer>
  );
}