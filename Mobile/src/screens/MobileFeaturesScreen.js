// src/screens/MobileFeaturesScreen.js - Mobile-specific features
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  Switch,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
  RefreshControl
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { getMobileFeatures } from '../services/api';
import { API_CONFIG } from '../services/apiConstants';
import Colors from '../styles/colors';
import GlobalStyles from '../styles/GlobalStyles';
import CustomButton from '../components/Common/CustomButton';
import LoadingSpinner from '../components/Common/LoadingSpinner';

export default function MobileFeaturesScreen() {
  const [features, setFeatures] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [settings, setSettings] = useState({
    pushNotifications: true,
    reminderAlerts: true,
    offlineMode: false,
    dataSaving: true,
    darkMode: false,
    voiceAssistant: false,
  });

  // Mobile-specific features data
  const mobileFeatures = {
    exclusive: [
      {
        id: 1,
        icon: '📱',
        title: 'Push Reminders',
        description: 'Get timely reminders for self-exams and appointments',
        enabled: settings.pushNotifications,
        settingKey: 'pushNotifications'
      },
      {
        id: 2,
        icon: '🔔',
        title: 'Smart Alerts',
        description: 'Personalized health alerts based on your activity',
        enabled: settings.reminderAlerts,
        settingKey: 'reminderAlerts'
      },
      {
        id: 3,
        icon: '📶',
        title: 'Offline Access',
        description: 'Access key resources without internet connection',
        enabled: settings.offlineMode,
        settingKey: 'offlineMode'
      },
      {
        id: 4,
        icon: '💾',
        title: 'Data Saving',
        description: 'Optimize data usage for slower connections',
        enabled: settings.dataSaving,
        settingKey: 'dataSaving'
      },
      {
        id: 5,
        icon: '🌙',
        title: 'Dark Mode',
        description: 'Comfortable viewing in low light conditions',
        enabled: settings.darkMode,
        settingKey: 'darkMode'
      },
      {
        id: 6,
        icon: '🎤',
        title: 'Voice Assistant',
        description: 'Hands-free navigation and chat using voice',
        enabled: settings.voiceAssistant,
        settingKey: 'voiceAssistant'
      }
    ],
    upcoming: [
      {
        id: 7,
        icon: '👥',
        title: 'Live Support Groups',
        description: 'Real-time video support sessions (Coming Soon)',
        status: 'beta'
      },
      {
        id: 8,
        icon: '🏃‍♀️',
        title: 'Activity Tracking',
        description: 'Sync with health apps for wellness tracking (Coming Soon)',
        status: 'planned'
      },
      {
        id: 9,
        icon: '🌍',
        title: 'Multi-language',
        description: 'Support for multiple languages (In Development)',
        status: 'development'
      }
    ]
  };

  useEffect(() => {
    loadMobileFeatures();
  }, []);

  const loadMobileFeatures = async () => {
    try {
      setLoading(true);
      const data = await getMobileFeatures();
      setFeatures(data || mobileFeatures);
    } catch (error) {
      console.error('Failed to load mobile features:', error);
      setFeatures(mobileFeatures);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadMobileFeatures();
  };

  const handleSettingToggle = (settingKey, value) => {
    setSettings(prev => ({
      ...prev,
      [settingKey]: value
    }));
    
    // Show confirmation for important toggles
    if (settingKey === 'pushNotifications' && value) {
      Alert.alert(
        'Notifications Enabled',
        'You will now receive important reminders and health updates.',
        [{ text: 'OK' }]
      );
    }
    
    if (settingKey === 'offlineMode' && value) {
      Alert.alert(
        'Offline Mode',
        'Downloading essential resources for offline access...',
        [{ text: 'OK' }]
      );
    }
  };

  const handleFeaturePress = (feature) => {
    if (feature.status) {
      Alert.alert(
        'Coming Soon',
        `${feature.title} is ${getStatusText(feature.status)}. Stay tuned!`,
        [{ text: 'OK' }]
      );
    } else {
      Alert.alert(
        feature.title,
        feature.description,
        [{ text: 'OK' }]
      );
    }
  };

  const getStatusText = (status) => {
    const statusMap = {
      'beta': 'in beta testing',
      'planned': 'planned for future release',
      'development': 'currently in development'
    };
    return statusMap[status] || 'coming soon';
  };

  const getStatusColor = (status) => {
    const colorMap = {
      'beta': '#FFA726',
      'planned': '#42A5F5',
      'development': '#66BB6A'
    };
    return colorMap[status] || Colors.textLight;
  };

  const renderFeatureCard = (feature, isUpcoming = false) => (
    <TouchableOpacity
      key={feature.id}
      style={[styles.featureCard, GlobalStyles.shadow]}
      onPress={() => handleFeaturePress(feature)}
      activeOpacity={0.8}
    >
      <View style={styles.featureHeader}>
        <View style={styles.featureIconContainer}>
          <Text style={styles.featureIcon}>{feature.icon}</Text>
        </View>
        
        <View style={styles.featureInfo}>
          <Text style={styles.featureTitle}>{feature.title}</Text>
          <Text style={styles.featureDescription}>{feature.description}</Text>
        </View>

        {!isUpcoming ? (
          <Switch
            value={settings[feature.settingKey]}
            onValueChange={(value) => handleSettingToggle(feature.settingKey, value)}
            trackColor={{ false: '#E0E0E0', true: Colors.primaryLight }}
            thumbColor={settings[feature.settingKey] ? Colors.primary : '#F4F4F4'}
          />
        ) : (
          <View style={[styles.statusBadge, { backgroundColor: getStatusColor(feature.status) }]}>
            <Text style={styles.statusText}>{feature.status.toUpperCase()}</Text>
          </View>
        )}
      </View>

      {isUpcoming && (
        <View style={styles.progressContainer}>
          <View style={styles.progressBar}>
            <View 
              style={[
                styles.progressFill,
                { 
                  width: feature.status === 'beta' ? '80%' : 
                         feature.status === 'development' ? '60%' : '30%'
                }
              ]} 
            />
          </View>
          <Text style={styles.progressText}>
            {feature.status === 'beta' ? 'Testing' : 
             feature.status === 'development' ? 'Developing' : 'Planning'}
          </Text>
        </View>
      )}
    </TouchableOpacity>
  );

  const renderStatsCard = () => (
    <View style={[styles.statsCard, GlobalStyles.shadow]}>
      <Text style={styles.statsTitle}>Mobile Usage</Text>
      
      <View style={styles.statsGrid}>
        <View style={styles.statItem}>
          <Ionicons name="notifications" size={24} color={Colors.primary} />
          <Text style={styles.statNumber}>12</Text>
          <Text style={styles.statLabel}>Reminders Set</Text>
        </View>
        
        <View style={styles.statItem}>
          <Ionicons name="download" size={24} color={Colors.primary} />
          <Text style={styles.statNumber}>8</Text>
          <Text style={styles.statLabel}>Resources Saved</Text>
        </View>
        
        <View style={styles.statItem}>
          <Ionicons name="time" size={24} color={Colors.primary} />
          <Text style={styles.statNumber}>45min</Text>
          <Text style={styles.statLabel}>Avg. Weekly Use</Text>
        </View>
      </View>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color={Colors.primary} />
        <Text style={styles.loadingText}>Loading mobile features...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>📱 Mobile Features</Text>
        <Text style={styles.subtitle}>
          Customize your app experience and explore upcoming features
        </Text>
      </View>

      <ScrollView
        style={styles.content}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            colors={[Colors.primary]}
          />
        }
      >
        {/* Stats Overview */}
        {renderStatsCard()}

        {/* Active Features Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="settings" size={24} color={Colors.primary} />
            <Text style={styles.sectionTitle}>Feature Settings</Text>
          </View>
          <Text style={styles.sectionDescription}>
            Customize how the app works on your device
          </Text>

          {features?.exclusive?.map(feature => renderFeatureCard(feature))}
        </View>

        {/* Upcoming Features Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="rocket" size={24} color={Colors.primary} />
            <Text style={styles.sectionTitle}>Coming Soon</Text>
          </View>
          <Text style={styles.sectionDescription}>
            Exciting new features we're working on
          </Text>

          {features?.upcoming?.map(feature => renderFeatureCard(feature, true))}
        </View>

        {/* Quick Actions */}
        <View style={styles.actionsSection}>
          <Text style={styles.actionsTitle}>Quick Actions</Text>
          
          <View style={styles.actionsGrid}>
            <CustomButton
              title="Clear Cache"
              variant="outline"
              size="small"
              icon="trash"
              onPress={() => Alert.alert('Clear Cache', 'App cache cleared successfully!')}
            />
            
            <CustomButton
              title="Export Data"
              variant="outline"
              size="small"
              icon="download"
              onPress={() => Alert.alert('Export Data', 'Your data export has started.')}
            />
            
            <CustomButton
              title="App Feedback"
              variant="outline"
              size="small"
              icon="chatbubble"
              onPress={() => Alert.alert('Feedback', 'Thank you for your feedback!')}
            />
          </View>
        </View>

        {/* App Info */}
        <View style={styles.infoCard}>
          <Ionicons name="information-circle" size={24} color={Colors.primary} />
          <View style={styles.infoContent}>
            <Text style={styles.infoTitle}>App Information</Text>
            <Text style={styles.infoText}>
              Version 1.0.0 • Last updated: Today{'\n'}
              Storage used: 45.2 MB{'\n'}
              Data synced: 2 hours ago
            </Text>
          </View>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: Colors.background,
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: Colors.textSecondary,
  },
  header: {
    backgroundColor: Colors.primary,
    paddingHorizontal: 20,
    paddingTop: 60,
    paddingBottom: 20,
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: 20,
    ...GlobalStyles.shadowLarge,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: 'white',
    opacity: 0.9,
    lineHeight: 20,
  },
  content: {
    flex: 1,
    padding: 16,
  },
  statsCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 16,
    marginBottom: 24,
  },
  statsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: Colors.textPrimary,
    marginBottom: 16,
  },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statItem: {
    alignItems: 'center',
    flex: 1,
  },
  statNumber: {
    fontSize: 20,
    fontWeight: 'bold',
    color: Colors.primary,
    marginVertical: 4,
  },
  statLabel: {
    fontSize: 12,
    color: Colors.textSecondary,
    textAlign: 'center',
  },
  section: {
    marginBottom: 24,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
    gap: 8,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: Colors.textPrimary,
  },
  sectionDescription: {
    fontSize: 14,
    color: Colors.textSecondary,
    marginBottom: 16,
    lineHeight: 20,
  },
  featureCard: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
  },
  featureHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  featureIconContainer: {
    marginRight: 12,
  },
  featureIcon: {
    fontSize: 24,
  },
  featureInfo: {
    flex: 1,
    marginRight: 12,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: Colors.textPrimary,
    marginBottom: 4,
  },
  featureDescription: {
    fontSize: 14,
    color: Colors.textSecondary,
    lineHeight: 18,
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  statusText: {
    fontSize: 10,
    color: 'white',
    fontWeight: 'bold',
  },
  progressContainer: {
    marginTop: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#F0F0F0',
  },
  progressBar: {
    height: 6,
    backgroundColor: '#F0F0F0',
    borderRadius: 3,
    marginBottom: 6,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: Colors.primary,
    borderRadius: 3,
  },
  progressText: {
    fontSize: 11,
    color: Colors.textLight,
    textAlign: 'right',
  },
  actionsSection: {
    marginBottom: 24,
  },
  actionsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: Colors.textPrimary,
    marginBottom: 12,
  },
  actionsGrid: {
    flexDirection: 'row',
    gap: 8,
  },
  infoCard: {
    flexDirection: 'row',
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    marginBottom: 24,
    ...GlobalStyles.shadow,
  },
  infoContent: {
    flex: 1,
    marginLeft: 12,
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: Colors.textPrimary,
    marginBottom: 4,
  },
  infoText: {
    fontSize: 12,
    color: Colors.textSecondary,
    lineHeight: 16,
  },
});
