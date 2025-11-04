// src/components/Common/Header.js
import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import Colors from '../../styles/colors';
import GlobalStyles from '../../styles/GlobalStyles';

const Header = ({ 
  title, 
  subtitle, 
  onBack, 
  rightIcon, 
  onRightPress,
  backgroundColor = Colors.primary,
  textColor = 'white'
}) => {
  return (
    <View style={[styles.header, { backgroundColor }]}>
      <View style={styles.headerContent}>
        <View style={styles.leftSection}>
          {onBack && (
            <TouchableOpacity onPress={onBack} style={styles.backButton}>
              <Ionicons name="arrow-back" size={24} color={textColor} />
            </TouchableOpacity>
          )}
        </View>
        
        <View style={styles.titleSection}>
          <Text style={[styles.title, { color: textColor }]}>{title}</Text>
          {subtitle && (
            <Text style={[styles.subtitle, { color: textColor }]}>{subtitle}</Text>
          )}
        </View>
        
        <View style={styles.rightSection}>
          {rightIcon && onRightPress && (
            <TouchableOpacity onPress={onRightPress} style={styles.rightButton}>
              <Ionicons name={rightIcon} size={24} color={textColor} />
            </TouchableOpacity>
          )}
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  header: {
    paddingTop: 60,
    paddingBottom: 16,
    paddingHorizontal: 20,
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: 20,
    ...GlobalStyles.shadowLarge,
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  leftSection: {
    width: 40,
  },
  backButton: {
    padding: 4,
  },
  titleSection: {
    flex: 1,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 14,
    marginTop: 4,
    textAlign: 'center',
    opacity: 0.9,
  },
  rightSection: {
    width: 40,
    alignItems: 'flex-end',
  },
  rightButton: {
    padding: 4,
  },
});

export default Header;