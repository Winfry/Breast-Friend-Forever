// mobile/src/screens/EncouragementScreen.js - Community support & motivation
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Share,
  Alert,
  ActivityIndicator,
  RefreshControl
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { GlobalStyles } from '../styles/GlobalStyles';
import apiService from '../utils/api';

const EncouragementScreen = () => {
  const [encouragements, setEncouragements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [activeTab, setActiveTab] = useState('community');

  // Sample data
  const sampleEncouragements = {
    community: [
      {
        id: 1,
        type: 'story',
        title: "Sarah's Journey",
        content: "After my diagnosis, I found strength in taking things one day at a time. Regular self-exams helped me catch it early!",
        author: "Sarah, 34",
        timestamp: "2 days ago",
        likes: 24,
        comments: 8,
        color: '#FF69B4',
        icon: '💖'
      },
      {
        id: 2,
        type: 'tip',
        title: "Monthly Reminder Tip",
        content: "I set my self-exam reminder for the same day I pay my rent - hard to forget both!",
        author: "Maria, 42",
        timestamp: "1 week ago",
        likes: 18,
        comments: 3,
        color: '#EC4899',
        icon: '💡'
      },
      {
        id: 3,
        type: 'question',
        title: "Support System",
        content: "How do you all remember to do monthly checks? Looking for accountability buddies!",
        author: "Jessica, 29",
        timestamp: "3 days ago",
        likes: 12,
        comments: 15,
        color: '#DB2777',
        icon: '🤝'
      }
    ],
    daily: [
      {
        id: 4,
        type: 'affirmation',
        title: "Today's Affirmation",
        content: "I am strong, I am capable, and I prioritize my health because I deserve care and attention.",
        author: "Daily Wellness",
        timestamp: "Today",
        likes: 56,
        color: '#BE185D',
        icon: '🌈'
      },
      {
        id: 5,
        type: 'milestone',
        title: "Consistency Achievement",
        content: "You've completed 3 monthly self-exams in a row! Your commitment to health is inspiring.",
        author: "Health Tracker",
        timestamp: "Just now",
        color: '#9D174D',
        icon: '🎯'
      }
    ]
  };

  const motivationalQuotes = [
    {
      text: "Your body hears everything your mind says. Stay positive.",
      author: "Naomi Judd",
      category: "Mindset"
    },
    {
      text: "Self-care is not selfish. You cannot serve from an empty vessel.",
      author: "Eleanor Brown",
      category: "Self-Care"
    },
    {
      text: "The greatest wealth is health.",
      author: "Virgil",
      category: "Wisdom"
    },
    {
      text: "You're braver than you believe, stronger than you seem, and smarter than you think.",
      author: "A.A. Milne",
      category: "Encouragement"
    }
  ];

  useEffect(() => {
    loadEncouragements();
  }, []);

  const loadEncouragements = async () => {
    try {
      // TODO: Replace with actual API call
      // const data = await apiService.getEncouragement();
      // setEncouragements(data);
      setEncouragements(sampleEncouragements);
    } catch (error) {
      console.error('Failed to load encouragements:', error);
      setEncouragements(sampleEncouragements); // Fallback
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadEncouragements();
  };

  const shareEncouragement = async (item) => {
    try {
      await Share.share({
        message: `${item.content}\n\n- Shared from Breast Friend Forever App 💖`,
        title: item.title
      });
    } catch (error) {
      Alert.alert('Error', 'Could not share this post');
    }
  };

  const likePost = (postId) => {
    // TODO: Implement like functionality with backend
    Alert.alert('Liked!', 'This would update in the backend');
  };

  const renderCommunityPost = (post) => (
    <View key={post.id} style={[styles.postCard, { borderLeftColor: post.color }]}>
      <View style={styles.postHeader}>
        <View style={[styles.postIcon, { backgroundColor: post.color }]}>
          <Text style={styles.iconText}>{post.icon}</Text>
        </View>
        <View style={styles.postInfo}>
          <Text style={styles.postTitle}>{post.title}</Text>
          <Text style={styles.postAuthor}>{post.author} • {post.timestamp}</Text>
        </View>
      </View>

      <Text style={styles.postContent}>{post.content}</Text>

      <View style={styles.postActions}>
        <TouchableOpacity 
          style={styles.actionButton}
          onPress={() => likePost(post.id)}
        >
          <Ionicons name="heart-outline" size={18} color="#666" />
          <Text style={styles.actionText}>{post.likes}</Text>
        </TouchableOpacity>

        {post.comments && (
          <TouchableOpacity style={styles.actionButton}>
            <Ionicons name="chatbubble-outline" size={16} color="#666" />
            <Text style={styles.actionText}>{post.comments}</Text>
          </TouchableOpacity>
        )}

        <TouchableOpacity 
          style={styles.actionButton}
          onPress={() => shareEncouragement(post)}
        >
          <Ionicons name="share-outline" size={18} color="#666" />
          <Text style={styles.actionText}>Share</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  const renderDailyEncouragement = (item) => (
    <View key={item.id} style={[styles.dailyCard, { backgroundColor: item.color }]}>
      <View style={styles.dailyHeader}>
        <Text style={styles.dailyIcon}>{item.icon}</Text>
        <View style={styles.dailyBadge}>
          <Text style={styles.dailyBadgeText}>{item.type.toUpperCase()}</Text>
        </View>
      </View>
      
      <Text style={styles.dailyTitle}>{item.title}</Text>
      <Text style={styles.dailyContent}>{item.content}</Text>
      
      <View style={styles.dailyFooter}>
        <Text style={styles.dailyAuthor}>{item.author}</Text>
        <Text style={styles.dailyTimestamp}>{item.timestamp}</Text>
      </View>
    </View>
  );

  const renderQuoteCard = (quote, index) => (
    <View key={index} style={styles.quoteCard}>
      <Ionicons name="quote" size={24} color="#FF69B4" />
      <Text style={styles.quoteText}>"{quote.text}"</Text>
      <View style={styles.quoteFooter}>
        <Text style={styles.quoteAuthor}>— {quote.author}</Text>
        <View style={styles.quoteCategory}>
          <Text style={styles.quoteCategoryText}>{quote.category}</Text>
        </View>
      </View>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#FF69B4" />
        <Text style={styles.loadingText}>Loading encouragement...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>💕 Encouragement</Text>
        <Text style={styles.subtitle}>Community support & daily motivation</Text>
      </View>

      {/* Tab Navigation */}
      <View style={styles.tabContainer}>
        <TouchableOpacity
          style={[styles.tab, activeTab === 'community' && styles.activeTab]}
          onPress={() => setActiveTab('community')}
        >
          <Ionicons 
            name="people" 
            size={20} 
            color={activeTab === 'community' ? '#FF69B4' : '#666'} 
          />
          <Text style={[
            styles.tabText,
            activeTab === 'community' && styles.activeTabText
          ]}>Community</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.tab, activeTab === 'daily' && styles.activeTab]}
          onPress={() => setActiveTab('daily')}
        >
          <Ionicons 
            name="calendar" 
            size={20} 
            color={activeTab === 'daily' ? '#FF69B4' : '#666'} 
          />
          <Text style={[
            styles.tabText,
            activeTab === 'daily' && styles.activeTabText
          ]}>Daily</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.tab, activeTab === 'quotes' && styles.activeTab]}
          onPress={() => setActiveTab('quotes')}
        >
          <Ionicons 
            name="heart" 
            size={20} 
            color={activeTab === 'quotes' ? '#FF69B4' : '#666'} 
          />
          <Text style={[
            styles.tabText,
            activeTab === 'quotes' && styles.activeTabText
          ]}>Quotes</Text>
        </TouchableOpacity>
      </View>

      {/* Content */}
      <ScrollView
        style={styles.content}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            colors={['#FF69B4']}
          />
        }
        showsVerticalScrollIndicator={false}
      >
        {activeTab === 'community' && (
          <View style={styles.tabContent}>
            <View style={styles.welcomeCard}>
              <Text style={styles.welcomeTitle}>Welcome to Our Community! 💖</Text>
              <Text style={styles.welcomeText}>
                Share your journey, ask questions, and support others in their breast health awareness.
              </Text>
              <TouchableOpacity style={styles.shareButton}>
                <Ionicons name="add" size={20} color="white" />
                <Text style={styles.shareButtonText}>Share Your Story</Text>
              </TouchableOpacity>
            </View>

            {encouragements.community?.map(renderCommunityPost)}
          </View>
        )}

        {activeTab === 'daily' && (
          <View style={styles.tabContent}>
            {encouragements.daily?.map(renderDailyEncouragement)}
            
            <View style={styles.streakCard}>
              <View style={styles.streakHeader}>
                <Ionicons name="flame" size={24} color="#FF6B35" />
                <Text style={styles.streakTitle}>Your Self-Care Streak</Text>
              </View>
              <Text style={styles.streakCount}>12 days</Text>
              <Text style={styles.streakSubtitle}>Keep going! You're building healthy habits.</Text>
              <View style={styles.streakProgress}>
                <View style={[styles.streakProgressFill, { width: '80%' }]} />
              </View>
            </View>
          </View>
        )}

        {activeTab === 'quotes' && (
          <View style={styles.tabContent}>
            <Text style={styles.quotesTitle}>Motivational Quotes</Text>
            {motivationalQuotes.map(renderQuoteCard)}
            
            <TouchableOpacity style={styles.saveQuoteButton}>
              <Ionicons name="bookmark" size={20} color="#FF69B4" />
              <Text style={styles.saveQuoteText}>Save Favorite Quotes</Text>
            </TouchableOpacity>
          </View>
        )}
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
  tabContainer: {
    flexDirection: 'row',
    backgroundColor: 'white',
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  tab: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    gap: 8,
  },
  activeTab: {
    borderBottomWidth: 3,
    borderBottomColor: '#FF69B4',
  },
  tabText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
  },
  activeTabText: {
    color: '#FF69B4',
  },
  content: {
    flex: 1,
  },
  tabContent: {
    padding: 16,
  },
  welcomeCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 16,
    marginBottom: 16,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  welcomeTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#FF69B4',
    marginBottom: 8,
    textAlign: 'center',
  },
  welcomeText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    lineHeight: 20,
    marginBottom: 16,
  },
  shareButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FF69B4',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 25,
    gap: 8,
  },
  shareButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
  },
  postCard: {
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
  postHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  postIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  iconText: {
    fontSize: 16,
    color: 'white',
  },
  postInfo: {
    flex: 1,
  },
  postTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 2,
  },
  postAuthor: {
    fontSize: 12,
    color: '#666',
  },
  postContent: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
    marginBottom: 12,
  },
  postActions: {
    flexDirection: 'row',
    gap: 16,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  actionText: {
    fontSize: 12,
    color: '#666',
  },
  dailyCard: {
    padding: 20,
    borderRadius: 16,
    marginBottom: 12,
  },
  dailyHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  dailyIcon: {
    fontSize: 24,
  },
  dailyBadge: {
    backgroundColor: 'rgba(255,255,255,0.3)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  dailyBadgeText: {
    color: 'white',
    fontSize: 10,
    fontWeight: 'bold',
  },
  dailyTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 8,
  },
  dailyContent: {
    fontSize: 16,
    color: 'white',
    lineHeight: 22,
    marginBottom: 12,
  },
  dailyFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  dailyAuthor: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.8)',
    fontWeight: '500',
  },
  dailyTimestamp: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.8)',
  },
  streakCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 16,
    marginTop: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  streakHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    gap: 8,
  },
  streakTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
  },
  streakCount: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FF6B35',
    marginBottom: 4,
  },
  streakSubtitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
  },
  streakProgress: {
    height: 8,
    backgroundColor: '#f0f0f0',
    borderRadius: 4,
    overflow: 'hidden',
  },
  streakProgressFill: {
    height: '100%',
    backgroundColor: '#FF6B35',
    borderRadius: 4,
  },
  quotesTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 16,
  },
  quoteCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  quoteText: {
    fontSize: 16,
    color: '#666',
    fontStyle: 'italic',
    lineHeight: 22,
    marginVertical: 12,
    textAlign: 'center',
  },
  quoteFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  quoteAuthor: {
    fontSize: 14,
    color: '#FF69B4',
    fontWeight: '500',
  },
  quoteCategory: {
    backgroundColor: '#FFF0F5',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  quoteCategoryText: {
    fontSize: 10,
    color: '#FF69B4',
    fontWeight: '600',
  },
  saveQuoteButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#FF69B4',
    borderStyle: 'dashed',
    gap: 8,
    marginTop: 8,
  },
  saveQuoteText: {
    color: '#FF69B4',
    fontSize: 14,
    fontWeight: '600',
  },
});

export default EncouragementScreen;