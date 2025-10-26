// mobile/src/screens/ResourcesScreen.js - Educational resources
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Linking,
  Alert,
  ActivityIndicator
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { GlobalStyles } from '../styles/GlobalStyles';
import apiService from '../utils/api';

const ResourcesScreen = () => {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');

  const resourceCategories = [
    { id: 'all', name: 'All Resources', icon: '📚', count: 12 },
    { id: 'guides', name: 'Self-Exam Guides', icon: '🤗', count: 4 },
    { id: 'prevention', name: 'Prevention', icon: '🛡️', count: 3 },
    { id: 'screening', name: 'Screening', icon: '🏥', count: 3 },
    { id: 'support', name: 'Support', icon: '💕', count: 2 },
  ];

  // Sample resources data
  const sampleResources = [
    {
      id: 1,
      title: "Breast Self-Examination Guide",
      description: "Step-by-step instructions for monthly breast self-exams with illustrations and tips.",
      category: 'guides',
      type: 'pdf',
      duration: '10 min read',
      level: 'Beginner',
      icon: '📖',
      color: '#FF69B4',
      url: 'https://example.com/self-exam-guide.pdf'
    },
    {
      id: 2,
      title: "Understanding Mammograms",
      description: "Everything you need to know about mammogram screening, preparation, and results.",
      category: 'screening',
      type: 'article',
      duration: '8 min read',
      level: 'Intermediate',
      icon: '🏥',
      color: '#EC4899',
      url: 'https://example.com/mammogram-guide'
    },
    {
      id: 3,
      title: "Breast Cancer Risk Factors",
      description: "Learn about genetic, lifestyle, and environmental factors that affect breast cancer risk.",
      category: 'prevention',
      type: 'interactive',
      duration: '12 min read',
      level: 'Intermediate',
      icon: '🔍',
      color: '#DB2777',
      url: 'https://example.com/risk-factors'
    },
    {
      id: 4,
      title: "Nutrition for Breast Health",
      description: "Foods and dietary habits that support breast health and overall wellness.",
      category: 'prevention',
      type: 'article',
      duration: '6 min read',
      level: 'Beginner',
      icon: '🥦',
      color: '#BE185D',
      url: 'https://example.com/nutrition-guide'
    },
    {
      id: 5,
      title: "Coping with Diagnosis",
      description: "Emotional support and practical advice for those newly diagnosed with breast cancer.",
      category: 'support',
      type: 'guide',
      duration: '15 min read',
      level: 'All Levels',
      icon: '💝',
      color: '#9D174D',
      url: 'https://example.com/coping-guide'
    },
    {
      id: 6,
      title: "Family History & Genetics",
      description: "Understanding hereditary risks and when to consider genetic testing.",
      category: 'prevention',
      type: 'article',
      duration: '10 min read',
      level: 'Advanced',
      icon: '🧬',
      color: '#831843',
      url: 'https://example.com/genetics-guide'
    }
  ];

  useEffect(() => {
    loadResources();
  }, []);

  const loadResources = async () => {
    try {
      // TODO: Replace with actual API call
      // const resourcesData = await apiService.getResources();
      // setResources(resourcesData);
      setResources(sampleResources);
    } catch (error) {
      console.error('Failed to load resources:', error);
      setResources(sampleResources); // Fallback to sample data
    } finally {
      setLoading(false);
    }
  };

  const openResource = async (resource) => {
    try {
      await Linking.openURL(resource.url);
    } catch (error) {
      Alert.alert('Error', 'Could not open this resource');
    }
  };

  const filteredResources = selectedCategory === 'all' 
    ? resources 
    : resources.filter(resource => resource.category === selectedCategory);

  const getCategoryInfo = (categoryId) => {
    return resourceCategories.find(cat => cat.id === categoryId) || resourceCategories[0];
  };

  const renderResourceCard = (resource) => (
    <TouchableOpacity 
      key={resource.id}
      style={[styles.resourceCard, { borderLeftColor: resource.color }]}
      onPress={() => openResource(resource)}
    >
      <View style={styles.resourceHeader}>
        <View style={[styles.resourceIcon, { backgroundColor: resource.color }]}>
          <Text style={styles.iconText}>{resource.icon}</Text>
        </View>
        <View style={styles.resourceInfo}>
          <Text style={styles.resourceTitle}>{resource.title}</Text>
          <View style={styles.metaContainer}>
            <View style={[styles.levelBadge, { backgroundColor: resource.color + '20' }]}>
              <Text style={[styles.levelText, { color: resource.color }]}>
                {resource.level}
              </Text>
            </View>
            <Text style={styles.duration}>{resource.duration}</Text>
          </View>
        </View>
        <Ionicons name="open-outline" size={20} color="#666" />
      </View>

      <Text style={styles.resourceDescription}>{resource.description}</Text>

      <View style={styles.resourceFooter}>
        <View style={styles.typeContainer}>
          <Ionicons 
            name={resource.type === 'pdf' ? 'document-text' : 
                  resource.type === 'interactive' ? 'play-circle' : 'book'} 
            size={16} 
            color={resource.color} 
          />
          <Text style={[styles.typeText, { color: resource.color }]}>
            {resource.type.charAt(0).toUpperCase() + resource.type.slice(1)}
          </Text>
        </View>
        <TouchableOpacity 
          style={[styles.readButton, { backgroundColor: resource.color }]}
          onPress={() => openResource(resource)}
        >
          <Text style={styles.readButtonText}>Read Now</Text>
        </TouchableOpacity>
      </View>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#FF69B4" />
        <Text style={styles.loadingText}>Loading resources...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>📚 Resources</Text>
        <Text style={styles.subtitle}>Educational materials for your breast health journey</Text>
      </View>

      {/* Category Filter */}
      <ScrollView 
        horizontal 
        showsHorizontalScrollIndicator={false}
        style={styles.categoriesContainer}
        contentContainerStyle={styles.categoriesContent}
      >
        {resourceCategories.map(category => (
          <TouchableOpacity
            key={category.id}
            style={[
              styles.categoryButton,
              selectedCategory === category.id && styles.selectedCategory
            ]}
            onPress={() => setSelectedCategory(category.id)}
          >
            <Text style={styles.categoryIcon}>{category.icon}</Text>
            <Text style={[
              styles.categoryName,
              selectedCategory === category.id && styles.selectedCategoryName
            ]}>
              {category.name}
            </Text>
            <View style={[
              styles.categoryCount,
              selectedCategory === category.id && styles.selectedCategoryCount
            ]}>
              <Text style={styles.categoryCountText}>{category.count}</Text>
            </View>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Resources List */}
      <ScrollView 
        style={styles.resourcesList}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.resourcesContent}
      >
        <Text style={styles.sectionTitle}>
          {getCategoryInfo(selectedCategory).name} ({filteredResources.length})
        </Text>

        {filteredResources.map(renderResourceCard)}

        {/* Additional Help */}
        <View style={styles.helpCard}>
          <Ionicons name="help-circle" size={24} color="#FF69B4" />
          <View style={styles.helpContent}>
            <Text style={styles.helpTitle}>Need More Information?</Text>
            <Text style={styles.helpText}>
              Our chat assistant can provide personalized answers to your specific questions about breast health.
            </Text>
            <TouchableOpacity style={styles.chatButton}>
              <Ionicons name="chatbubble" size={16} color="white" />
              <Text style={styles.chatButtonText}>Ask Our Assistant</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFF0F5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#FFF0F5',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  header: {
    backgroundColor: '#FF69B4',
    padding: 25,
    paddingTop: 60,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 16,
    color: 'white',
    opacity: 0.9,
  },
  categoriesContainer: {
    backgroundColor: 'white',
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  categoriesContent: {
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  categoryButton: {
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    marginRight: 8,
    borderRadius: 12,
    backgroundColor: '#f8f9fa',
    minWidth: 100,
  },
  selectedCategory: {
    backgroundColor: '#FF69B4',
  },
  categoryIcon: {
    fontSize: 20,
    marginBottom: 4,
  },
  categoryName: {
    fontSize: 12,
    fontWeight: '600',
    color: '#666',
    textAlign: 'center',
  },
  selectedCategoryName: {
    color: 'white',
  },
  categoryCount: {
    marginTop: 4,
    backgroundColor: 'rgba(255,255,255,0.2)',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
  },
  selectedCategoryCount: {
    backgroundColor: 'rgba(255,255,255,0.3)',
  },
  categoryCountText: {
    fontSize: 10,
    fontWeight: 'bold',
    color: 'white',
  },
  resourcesList: {
    flex: 1,
  },
  resourcesContent: {
    padding: 16,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 16,
  },
  resourceCard: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  resourceHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  resourceIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  iconText: {
    fontSize: 16,
  },
  resourceInfo: {
    flex: 1,
  },
  resourceTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 4,
  },
  metaContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  levelBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 6,
  },
  levelText: {
    fontSize: 10,
    fontWeight: '600',
  },
  duration: {
    fontSize: 12,
    color: '#666',
  },
  resourceDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
    marginBottom: 12,
  },
  resourceFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  typeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  typeText: {
    fontSize: 12,
    fontWeight: '500',
  },
  readButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  readButtonText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '600',
  },
  helpCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 16,
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
    borderWidth: 2,
    borderColor: '#FF69B4',
    borderStyle: 'dashed',
  },
  helpContent: {
    flex: 1,
    marginLeft: 12,
  },
  helpTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#FF69B4',
    marginBottom: 4,
  },
  helpText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 18,
    marginBottom: 12,
  },
  chatButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FF69B4',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
    alignSelf: 'flex-start',
    gap: 6,
  },
  chatButtonText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '600',
  },
});

export default ResourcesScreen;
