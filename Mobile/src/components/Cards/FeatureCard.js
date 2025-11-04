// src/components/Cards/FeatureCard.js
import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import Colors from '../../styles/colors';
import GlobalStyles from '../../styles/GlobalStyles';

const FeatureCard = ({
  icon,
  title,
  description,
  onPress,
  color = Colors.primary,
  backgroundColor,
  style,
}) => {
  return (
    <TouchableOpacity
      style={[
        styles.card,
        { backgroundColor: backgroundColor || color },
        GlobalStyles.shadow,
        style,
      ]}
      onPress={onPress}
      activeOpacity={0.9}
    >
      <View style={styles.iconContainer}>
        <Text style={styles.icon}>{icon}</Text>
      </View>
      
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.description}>{description}</Text>
      
      <View style={styles.arrowContainer}>
        <Ionicons name="arrow-forward" size={20} color="white" />
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    padding: 20,
    borderRadius: 16,
    marginVertical: 8,
    minHeight: 140,
    justifyContent: 'space-between',
  },
  iconContainer: {
    marginBottom: 12,
  },
  icon: {
    fontSize: 24,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 8,
  },
  description: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.9)',
    lineHeight: 18,
    flex: 1,
  },
  arrowContainer: {
    alignSelf: 'flex-end',
    marginTop: 12,
  },
});

export default FeatureCard;