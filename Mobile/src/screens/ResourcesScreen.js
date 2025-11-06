import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  Alert,
  TouchableOpacity,
  Linking
} from 'react-native';
import { getResources } from '../services/api';
import { API_CONFIG } from '../services/apiConstants';

export default function ResourcesScreen() {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadResources();
  }, []);

  const loadResources = async () => {
    try {
      setLoading(true);
      const data = await getResources();
      setResources(Array.isArray(data) ? data : defaultResources);
    } catch (error) {
      Alert.alert('Error', 'Failed to load resources');
      setResources(defaultResources);
    } finally {
      setLoading(false);
    }
  };

  const handleResourcePress = async (resource) => {
    // Try to open PDF or resource URL
    if (resource.url) {
      try {
        await Linking.openURL(resource.url);
      } catch (error) {
        Alert.alert('Error', 'Cannot open this resource');
      }
    } else {
      Alert.alert(resource.title, resource.description);
    }
  };

  const renderResourceItem = ({ item }) => (
    <TouchableOpacity 
      style={styles.resourceCard}
      onPress={() => handleResourcePress(item)}
    >
      <View style={styles.resourceIcon}>
        <Text style={styles.iconText}>📚</Text>
      </View>
      
      <View style={styles.resourceContent}>
        <Text style={styles.resourceTitle}>{item.title}</Text>
        <Text style={styles.resourceDescription}>{item.description}</Text>
        <Text style={styles.resourceType}>{item.type}</Text>
      </View>
      
      <View style={styles.arrowContainer}>
        <Text style={styles.arrow}>›</Text>
      </View>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color={API_CONFIG.COLORS.PRIMARY} />
        <Text style={styles.loadingText}>Loading resources...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>📚 Educational Resources</Text>
        <Text style={styles.subtitle}>
          Access breast health information and guides
        </Text>
      </View>

      <FlatList
        data={resources}
        renderItem={renderResourceItem}
        keyExtractor={(item, index) => index.toString()}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.listContent}
      />
    </View>
  );
}

// Default resources matching your PDF files
const defaultResources = [
  {
    title: 'Breast Cancer Risk and Prevention',
    description: 'American Cancer Society guide on risk factors and prevention strategies',
    type: 'PDF Guide',
    url: 'http://192.168.1.118:8000/static/pdfs/American Cancer Society Breast Cancer Risk and Prevention.pdf'
  },
  {
    title: 'Diet and Breast Cancer',
    description: 'Research on the relationship between diet and breast cancer risk',
    type: 'Research Paper',
    url: 'http://192.168.1.118:8000/static/pdfs/bcc98-diet-and-breast-cancer-web (1).pdf'
  },
  {
    title: 'Early Detection Summary',
    description: 'Comprehensive knowledge summary on early detection methods',
    type: 'Medical Summary',
    url: 'http://192.168.1.118:8000/static/pdfs/KNOWLEDGE-SUMMARY---EARLY-DETECTION.pdf'
  },
  {
    title: 'Self-Examination Guide',
    description: 'Step-by-step guide for breast self-examination',
    type: 'Instruction Guide',
    url: 'http://192.168.1.118:8000/static/pdfs/self_exam_guide.pdf'
  },
  {
    title: 'Risk Factors Overview',
    description: 'Detailed information about breast cancer risk factors',
    type: 'Educational Material',
    url: 'http://192.168.100.5:8000/static/pdfs/Risk factors.pdf'
  },
  {
    title: 'Facts and Myths',
    description: 'Separating facts from common myths about breast cancer',
    type: 'Informational Guide',
    url: 'http://192.168.100.5:8000/static/pdfs/Risks,Facts-and-Myths.pdf'
  }
];

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: API_CONFIG.COLORS.BACKGROUND,
  },
  header: {
    padding: 20,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: API_CONFIG.COLORS.BACKGROUND,
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  listContent: {
    padding: 16,
  },
  resourceCard: {
    backgroundColor: '#FFFFFF',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
  },
  resourceIcon: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: API_CONFIG.COLORS.SECONDARY,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  iconText: {
    fontSize: 20,
  },
  resourceContent: {
    flex: 1,
  },
  resourceTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  resourceDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
    lineHeight: 18,
  },
  resourceType: {
    fontSize: 12,
    color: API_CONFIG.COLORS.PRIMARY,
    fontWeight: '500',
  },
  arrowContainer: {
    paddingLeft: 8,
  },
  arrow: {
    fontSize: 20,
    color: '#999',
    fontWeight: 'bold',
  },
});