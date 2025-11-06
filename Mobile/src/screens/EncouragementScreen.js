// src/screens/EncouragementScreen.js - HYBRID VERSION
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  Alert,
  TouchableOpacity,
  Share,
  ScrollView,
  RefreshControl
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { getEncouragement } from '../services/api';
import { API_CONFIG } from '../services/apiConstants';

function EncouragementScreen() {
  const [activeTab, setActiveTab] = useState('community');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadEncouragement();
  }, []);

  const loadEncouragement = async () => {
    try {
      setLoading(true);
      const data = await getEncouragement();
      // Transform API data to include rich content types
      const enrichedData = Array.isArray(data) 
        ? data.map((msg, index) => ({
            ...msg,
            type: getMessageType(index),
            color: getColorByType(index),
            icon: getIconByType(index),
            timestamp: getRandomTimestamp(),
            comments: Math.floor(Math.random() * 20),
            liked: false
          }))
        : defaultMessages;
      setMessages(enrichedData);
    } catch (error) {
      Alert.alert('Error', 'Failed to load encouragement messages');
      setMessages(defaultMessages);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadEncouragement();
  };

  const handleShare = async (message) => {
    try {
      await Share.share({
        message: `${message.text} 💖 #BreastFriendForever`,
        title: 'Encouraging Message'
      });
    } catch (error) {
      Alert.alert('Error', 'Sharing failed');
    }
  };

  const handleLike = (messageId) => {
    setMessages(prev => prev.map(msg => 
      msg.id === messageId 
        ? { ...msg, likes: (msg.likes || 0) + 1, liked: true }
        : msg
    ));
  };

  // Helper functions for rich content
  const getMessageType = (index) => {
    const types = ['story', 'tip', 'affirmation', 'milestone', 'question'];
    return types[index % types.length];
  };

  const getColorByType = (index) => {
    const colors = ['#FF69B4', '#EC4899', '#DB2777', '#BE185D', '#9D174D'];
    return colors[index % colors.length];
  };

  const getIconByType = (index) => {
    const icons = ['💖', '💡', '🌈', '🎯', '🤝'];
    return icons[index % icons.length];
  };

  const getRandomTimestamp = () => {
    const times = ['Just now', '2 hours ago', '1 day ago', '3 days ago', '1 week ago'];
    return times[Math.floor(Math.random() * times.length)];
  };

  // Motivational quotes section
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
    }
  ];

  // Render different card types based on message type
  const renderMessageItem = ({ item }) => {
    switch (item.type) {
      case 'story':
        return renderStoryCard(item);
      case 'tip':
        return renderTipCard(item);
      case 'affirmation':
        return renderAffirmationCard(item);
      case 'milestone':
        return renderMilestoneCard(item);
      default:
        return renderCommunityCard(item);
    }
  };

  const renderCommunityCard = (item) => (
    <View style={[styles.messageCard, { borderLeftColor: item.color }]}>
      <View style={styles.messageHeader}>
        <View style={[styles.messageIcon, { backgroundColor: item.color }]}>
          <Text style={styles.iconText}>{item.icon}</Text>
        </View>
        <View style={styles.messageInfo}>
          <Text style={styles.messageTitle}>
            {item.type === 'story' ? `${item.author}'s Story` : 
             item.type === 'tip' ? 'Helpful Tip' : 'Community Post'}
          </Text>
          <Text style={styles.messageAuthor}>{item.author} • {item.timestamp}</Text>
        </View>
      </View>

      <Text style={styles.messageText}>"{item.text}"</Text>

      <View style={styles.actionsContainer}>
        <TouchableOpacity 
          style={styles.actionButton}
          onPress={() => handleLike(item.id)}
          disabled={item.liked}
        >
          <Ionicons 
            name={item.liked ? "heart" : "heart-outline"} 
            size={18} 
            color={item.liked ? item.color : '#666'} 
          />
          <Text style={[styles.actionText, item.liked && { color: item.color }]}>
            {item.likes || 0}
          </Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.actionButton}>
          <Ionicons name="chatbubble-outline" size={16} color="#666" />
          <Text style={styles.actionText}>{item.comments}</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.actionButton}
          onPress={() => handleShare(item)}
        >
          <Ionicons name="share-outline" size={18} color="#666" />
          <Text style={styles.actionText}>Share</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  const renderStoryCard = (item) => (
    <View style={[styles.specialCard, { backgroundColor: item.color }]}>
      <View style={styles.specialHeader}>
        <Text style={styles.specialIcon}>{item.icon}</Text>
        <View style={styles.typeBadge}>
          <Text style={styles.typeBadgeText}>STORY</Text>
        </View>
      </View>
      <Text style={styles.specialTitle}>"{item.text}"</Text>
      <View style={styles.specialFooter}>
        <Text style={styles.specialAuthor}>- {item.author}</Text>
        <Text style={styles.specialTimestamp}>{item.timestamp}</Text>
      </View>
    </View>
  );

  const renderTipCard = (item) => (
    <View style={[styles.tipCard, { borderColor: item.color }]}>
      <View style={styles.tipHeader}>
        <Text style={styles.tipIcon}>💡</Text>
        <Text style={styles.tipTitle}>Helpful Tip</Text>
      </View>
      <Text style={styles.tipText}>{item.text}</Text>
      <Text style={styles.tipAuthor}>Shared by {item.author}</Text>
    </View>
  );

  const renderAffirmationCard = (item) => (
    <View style={[styles.affirmationCard, { backgroundColor: '#FFF0F5' }]}>
      <Text style={styles.affirmationIcon}>🌈</Text>
      <Text style={styles.affirmationText}>"{item.text}"</Text>
      <Text style={styles.affirmationAuthor}>- {item.author}</Text>
    </View>
  );

  const renderMilestoneCard = (item) => (
    <View style={[styles.milestoneCard, { backgroundColor: item.color }]}>
      <View style={styles.milestoneHeader}>
        <Ionicons name="trophy" size={24} color="white" />
        <Text style={styles.milestoneTitle}>Community Milestone</Text>
      </View>
      <Text style={styles.milestoneText}>{item.text}</Text>
      <Text style={styles.milestoneStats}>{item.likes} supporters</Text>
    </View>
  );

  const renderQuoteCard = (quote, index) => (
    <View key={index} style={styles.quoteCard}>
      <Ionicons name="chatbox-ellipses" size={24} color={API_CONFIG.COLORS.PRIMARY} />
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
      <View style={styles.centered}>
        <ActivityIndicator size="large" color={API_CONFIG.COLORS.PRIMARY} />
        <Text style={styles.loadingText}>Loading encouragement...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header with gradient */}
      <View style={styles.header}>
        <Text style={styles.title}>💕 Support Community</Text>
        <Text style={styles.subtitle}>
          Share and receive encouragement from others
        </Text>
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
            color={activeTab === 'community' ? API_CONFIG.COLORS.PRIMARY : '#666'} 
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
            name="flash" 
            size={20} 
            color={activeTab === 'daily' ? API_CONFIG.COLORS.PRIMARY : '#666'} 
          />
          <Text style={[
            styles.tabText,
            activeTab === 'daily' && styles.activeTabText
          ]}>Highlights</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.tab, activeTab === 'quotes' && styles.activeTab]}
          onPress={() => setActiveTab('quotes')}
        >
          <Ionicons 
            name="heart" 
            size={20} 
            color={activeTab === 'quotes' ? API_CONFIG.COLORS.PRIMARY : '#666'} 
          />
          <Text style={[
            styles.tabText,
            activeTab === 'quotes' && styles.activeTabText
          ]}>Quotes</Text>
        </TouchableOpacity>
      </View>

      {/* Content */}
      {activeTab === 'community' && (
        <FlatList
          data={messages}
          renderItem={renderMessageItem}
          keyExtractor={(item, index) => item.id?.toString() || index.toString()}
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.listContent}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              colors={[API_CONFIG.COLORS.PRIMARY]}
            />
          }
        />
      )}

      {activeTab === 'daily' && (
        <ScrollView 
          style={styles.listContent}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              colors={[API_CONFIG.COLORS.PRIMARY]}
            />
          }
        >
          {/* Welcome Card */}
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

          {/* Top Stories */}
          <Text style={styles.sectionTitle}>🌟 Today's Highlights</Text>
          {messages.filter(msg => msg.type === 'story' || msg.type === 'milestone').map((item, index) => (
            <View key={item.id || index}>
              {renderMessageItem({ item, index })}
            </View>
          ))}
        </ScrollView>
      )}

      {activeTab === 'quotes' && (
        <ScrollView 
          style={styles.listContent}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              colors={[API_CONFIG.COLORS.PRIMARY]}
            />
          }
        >
          <Text style={styles.sectionTitle}>💫 Motivational Quotes</Text>
          {motivationalQuotes.map(renderQuoteCard)}
          
          <TouchableOpacity style={styles.saveQuoteButton}>
            <Ionicons name="bookmark" size={20} color={API_CONFIG.COLORS.PRIMARY} />
            <Text style={styles.saveQuoteText}>Save Favorite Quotes</Text>
          </TouchableOpacity>
        </ScrollView>
      )}
    </View>
  );
}

// Default encouragement messages
const defaultMessages = [
  {
    id: 1,
    text: "You are stronger than you know, and you are not alone in this journey.",
    author: "Survivor Sister",
    likes: 42,
    type: "story",
    color: "#FF69B4",
    icon: "💖",
    timestamp: "2 days ago",
    comments: 8
  },
  {
    id: 2,
    text: "Early detection saves lives. Your regular check-ups are acts of self-love.",
    author: "Health Advocate",
    likes: 38,
    type: "tip",
    color: "#EC4899",
    icon: "💡",
    timestamp: "1 week ago",
    comments: 3
  },
  {
    id: 3,
    text: "Your strength inspires everyone around you. Keep fighting!",
    author: "Support Friend",
    likes: 56,
    type: "affirmation",
    color: "#DB2777",
    icon: "🌈",
    timestamp: "3 days ago",
    comments: 15
  },
  {
    id: 4,
    text: "Knowledge is power. Understanding your body is the first step to taking control.",
    author: "Educator",
    likes: 29,
    type: "tip",
    color: "#BE185D",
    icon: "🎯",
    timestamp: "5 days ago",
    comments: 6
  },
  {
    id: 5,
    text: "You are beautiful, you are strong, and you are worthy of all the love and support.",
    author: "Community Member",
    likes: 67,
    type: "affirmation",
    color: "#9D174D",
    icon: "💝",
    timestamp: "Just now",
    comments: 12
  },
  {
    id: 6,
    text: "Every self-exam, every doctor's visit, every question asked - you're taking powerful steps.",
    author: "Healthcare Worker",
    likes: 44,
    type: "milestone",
    color: "#FF69B4",
    icon: "🏆",
    timestamp: "1 day ago",
    comments: 9
  }
];

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: API_CONFIG.COLORS.BACKGROUND,
  },
  header: {
    backgroundColor: API_CONFIG.COLORS.PRIMARY,
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
    borderBottomColor: API_CONFIG.COLORS.PRIMARY,
  },
  tabText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
  },
  activeTabText: {
    color: API_CONFIG.COLORS.PRIMARY,
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
  // Community Card Styles
  messageCard: {
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
  messageHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  messageIcon: {
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
  messageInfo: {
    flex: 1,
  },
  messageTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 2,
  },
  messageAuthor: {
    fontSize: 12,
    color: '#666',
  },
  messageText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
    marginBottom: 12,
    fontStyle: 'italic',
  },
  actionsContainer: {
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
  // Special Card Styles
  specialCard: {
    padding: 20,
    borderRadius: 16,
    marginBottom: 12,
  },
  specialHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  specialIcon: {
    fontSize: 24,
  },
  typeBadge: {
    backgroundColor: 'rgba(255,255,255,0.3)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  typeBadgeText: {
    color: 'white',
    fontSize: 10,
    fontWeight: 'bold',
  },
  specialTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 8,
    textAlign: 'center',
    fontStyle: 'italic',
  },
  specialFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  specialAuthor: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.8)',
    fontWeight: '500',
  },
  specialTimestamp: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.8)',
  },
  // Tip Card
  tipCard: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    borderWidth: 2,
    borderStyle: 'dashed',
  },
  tipHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
    gap: 8,
  },
  tipIcon: {
    fontSize: 20,
  },
  tipTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1F2937',
  },
  tipText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
    marginBottom: 8,
  },
  tipAuthor: {
    fontSize: 12,
    color: '#999',
    fontStyle: 'italic',
  },
  // Affirmation Card
  affirmationCard: {
    padding: 20,
    borderRadius: 16,
    marginBottom: 12,
    alignItems: 'center',
  },
  affirmationIcon: {
    fontSize: 32,
    marginBottom: 12,
  },
  affirmationText: {
    fontSize: 16,
    color: '#333',
    fontStyle: 'italic',
    textAlign: 'center',
    lineHeight: 22,
    marginBottom: 8,
  },
  affirmationAuthor: {
    fontSize: 14,
    color: API_CONFIG.COLORS.PRIMARY,
    fontWeight: '500',
  },
  // Milestone Card
  milestoneCard: {
    padding: 20,
    borderRadius: 16,
    marginBottom: 12,
  },
  milestoneHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    gap: 8,
  },
  milestoneTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
  },
  milestoneText: {
    fontSize: 16,
    color: 'white',
    lineHeight: 22,
    marginBottom: 8,
  },
  milestoneStats: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.8)',
    fontWeight: '500',
  },
  // Welcome Card
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
    color: API_CONFIG.COLORS.PRIMARY,
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
    backgroundColor: API_CONFIG.COLORS.PRIMARY,
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
  // Quotes
  sectionTitle: {
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
    color: API_CONFIG.COLORS.PRIMARY,
    fontWeight: '500',
  },
  quoteCategory: {
    backgroundColor: API_CONFIG.COLORS.SECONDARY,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  quoteCategoryText: {
    fontSize: 10,
    color: API_CONFIG.COLORS.PRIMARY,
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
    borderColor: API_CONFIG.COLORS.PRIMARY,
    borderStyle: 'dashed',
    gap: 8,
    marginTop: 8,
  },
  saveQuoteText: {
    color: API_CONFIG.COLORS.PRIMARY,
    fontSize: 14,
    fontWeight: '600',
  },
});

export default EncouragementScreen;