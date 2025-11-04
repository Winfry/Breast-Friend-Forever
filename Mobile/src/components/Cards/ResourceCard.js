// src/components/Cards/ResourceCard.js
import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import Colors from '../../styles/colors';
import GlobalStyles from '../../styles/globalStyles';

const ResourceCard = ({
  title,
  description,
  type,
  onPress,
  icon = 'document-text',
  color = Colors.primary,
}) => {
  return (
    <TouchableOpacity
      style={[styles.card, GlobalStyles.shadow]}
      onPress={onPress}
      activeOpacity={0.8}
    >
      <View style={[styles.iconContainer, { backgroundColor: color }]}>
        <Ionicons name={icon} size={24} color="white" />
      </View>
      
      <View style={styles.content}>
        <Text style={styles.title}>{title}</Text>
        <Text style={styles.description}>{description}</Text>
        <View style={styles.typeContainer}>
          <Text style={[styles.type, { color }]}>{type}</Text>
        </View>
      </View>
      
      <View style={styles.arrow}>
        <Ionicons name="chevron-forward" size={20} color={Colors.textLight} />
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    marginVertical: 6,
  },
  iconContainer: {
    width: 50,
    height: 50,
    borderRadius: 25,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 16,
  },
  content: {
    flex: 1,
  },
  title: {
    fontSize: 16,
    fontWeight: 'bold',
    color: Colors.textPrimary,
    marginBottom: 4,
  },
  description: {
    fontSize: 14,
    color: Colors.textSecondary,
    lineHeight: 18,
    marginBottom: 8,
  },
  typeContainer: {
    alignSelf: 'flex-start',
  },
  type: {
    fontSize: 12,
    fontWeight: '600',
    textTransform: 'uppercase',
  },
  arrow: {
    marginLeft: 8,
  },
});

export default ResourceCard;