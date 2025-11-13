import React, { useState, useEffect } from 'react';
import { 
  View, 
  Text, 
  ScrollView, 
  TouchableOpacity, 
  StyleSheet,
  Alert 
} from 'react-native';
import { checkBackendHealth } from '../services/api';
import { API_CONFIG } from '../services/apiConstants';

export default function HomeScreen({ navigation }) {
  const [backendConnected, setBackendConnected] = useState(false);

  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      const isHealthy = await checkBackendHealth();
      setBackendConnected(isHealthy);
      if (!isHealthy) {
        Alert.alert('Connection Issue', 'Cannot connect to backend server');
      }
    } catch (error) {
      setBackendConnected(false);
      Alert.alert('Connection Issue', 'Cannot connect to backend server');
    }
  };

  // Mirroring your Streamlit feature cards
  const menuItems = [
    { 
      title: '🤗 Self-Exam Guide', 
      screen: 'SelfExam', 
      color: API_CONFIG.COLORS.PRIMARY,
      description: 'Interactive step-by-step instructions with visual guides'
    },
    { 
      title: '💬 AI Assistant', 
      screen: 'Chat', 
      color: '#4ECDC4',
      description: 'Animated chatbot with compassionate responses' 
    },
    { 
      title: '🏥 Find Help', 
      screen: 'Hospitals', 
      color: '#45B7D1',
      description: 'Locate screening facilities with interactive maps' 
    },
    { 
      title: '💕 Support Community', 
      screen: 'Encouragement', 
      color: '#96CEB4',
      description: 'Share and receive encouragement with animations' 
    },
    { 
      title: '📚 Resources', 
      screen: 'Resources', 
      color: '#FFA726',
      description: 'Access educational content with smooth transitions' 
    },
    { 
      title: '📱 Mobile Features', 
      screen: 'MobileFeatures', 
      color: '#8B5CF6',
      description: 'Customize app settings and explore mobile-exclusive features'
    },
  ];

  return (
    <ScrollView style={styles.container}>
      {/* Main header - mirroring Streamlit */}
      <View style={styles.header}>
        <Text style={styles.welcomeText}>Breast Friend Forever 💖</Text>
        <Text style={styles.subtitle}>
          Your compassionate guide to breast health
        </Text>
      </View>

      {/* Backend connection status - mirroring Streamlit */}
      <View style={styles.connectionContainer}>
        {backendConnected ? (
          <View style={styles.connectionStatus}>
            <Text style={styles.connectionText}>✅ Backend Connected & Ready!</Text>
          </View>
        ) : (
          <View style={styles.connectionError}>
            <Text style={styles.connectionText}>❌ Backend Connection Failed</Text>
          </View>
        )}
      </View>

      {/* Welcome card - mirroring Streamlit pink-card */}
      <View style={styles.welcomeCard}>
        <Text style={styles.welcomeCardTitle}>🎀 Welcome to Your Breast Health Companion</Text>
        <Text style={styles.welcomeCardText}>
          Your compassionate, animated guide to breast health education, support, and resources. 
          Every interaction is designed with care and understanding.
        </Text>
      </View>

      {/* Features grid - mirroring Streamlit */}
      <Text style={styles.sectionTitle}>✨ Explore Our Features</Text>
      
      {menuItems.map((item, index) => (
        <TouchableOpacity
          key={index}
          style={[styles.featureCard, { backgroundColor: item.color }]}
          onPress={() => navigation.navigate(item.screen)}
        >
          <Text style={styles.featureTitle}>{item.title}</Text>
          <Text style={styles.featureDescription}>{item.description}</Text>
        </TouchableOpacity>
      ))}

      {/* Quick Start Guide - mirroring Streamlit */}
      <View style={styles.quickStartCard}>
        <Text style={styles.quickStartTitle}>🚀 Quick Start Guide</Text>
        <Text style={styles.quickStartText}>
          1. 🤗 Self-Exam Guide - Learn breast self-examination with animated steps{"\n"}
          2. 💬 Chat Assistant - Ask questions and get animated responses{"\n"}  
          3. 🏥 Find Screening - Locate facilities with interactive search{"\n"}
          4. 💕 Support Wall - Share encouragement with heart animations{"\n"}
          5. 📚 Resources - Access educational content with smooth transitions
        </Text>
        
        <TouchableOpacity 
          style={styles.startButton}
          onPress={() => navigation.navigate('SelfExam')}
        >
          <Text style={styles.startButtonText}>🎯 Start Your Journey</Text>
        </TouchableOpacity>
      </View>

      {/* Footer - mirroring Streamlit */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>Made with 💖 for your health journey</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: API_CONFIG.COLORS.BACKGROUND,
    padding: 16,
  },
  header: {
    alignItems: 'center',
    marginVertical: 20,
  },
  welcomeText: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginTop: 8,
  },
  connectionContainer: {
    marginVertical: 10,
  },
  connectionStatus: {
    backgroundColor: '#E8F5E8',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  connectionError: {
    backgroundColor: '#FFEBEE',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  connectionText: {
    fontSize: 14,
    fontWeight: 'bold',
  },
  welcomeCard: {
    backgroundColor: '#FCE4EC', // Light pink background
    padding: 20,
    borderRadius: 12,
    marginVertical: 16,
    borderLeftWidth: 4,
    borderLeftColor: API_CONFIG.COLORS.PRIMARY,
  },
  welcomeCardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  welcomeCardText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginVertical: 16,
  },
  featureCard: {
    padding: 16,
    borderRadius: 12,
    marginVertical: 8,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  featureTitle: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  featureDescription: {
    color: 'white',
    fontSize: 12,
    opacity: 0.9,
  },
  quickStartCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 12,
    marginVertical: 16,
    borderWidth: 1,
    borderColor: '#E0E0E0',
  },
  quickStartTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 12,
  },
  quickStartText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
    marginBottom: 16,
  },
  startButton: {
    backgroundColor: API_CONFIG.COLORS.PRIMARY,
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
  },
  startButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  footer: {
    alignItems: 'center',
    marginVertical: 20,
    padding: 16,
  },
  footerText: {
    color: API_CONFIG.COLORS.PRIMARY,
    fontWeight: 'bold',
    fontSize: 14,
  },
});