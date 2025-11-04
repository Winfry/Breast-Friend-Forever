// src/components/Common/LoadingSpinner.js
import React from 'react';
import { View, Text, ActivityIndicator, StyleSheet } from 'react-native';
import Colors from '../../styles/colors';
import GlobalStyles from '../../styles/GlobalStyles';

const LoadingSpinner = ({ 
  size = 'large', 
  color = Colors.primary, 
  text, 
  fullScreen = false 
}) => {
  const containerStyle = fullScreen 
    ? [styles.fullScreenContainer, styles.container]
    : styles.container;

  return (
    <View style={containerStyle}>
      <ActivityIndicator size={size} color={color} />
      {text && <Text style={styles.loadingText}>{text}</Text>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  fullScreenContainer: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  loadingText: {
    marginTop: 12,
    fontSize: 16,
    color: Colors.textSecondary,
    textAlign: 'center',
  },
});

export default LoadingSpinner;