// src/screens/ChatScreen.js - FINAL FIXED VERSION
import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  Alert,
  Animated,
  Keyboard,
  TouchableWithoutFeedback,
  Dimensions
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { sendChatMessage } from '../services/api';
import { API_CONFIG } from '../services/apiConstants';

const { height: SCREEN_HEIGHT } = Dimensions.get('window');

export default function ChatScreen() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your Breast Health Companion. I'm here to provide compassionate, accurate information about breast health. What would you like to know today? 💖",
      isUser: false,
      timestamp: new Date(),
      type: 'welcome'
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [keyboardHeight, setKeyboardHeight] = useState(0);
  
  const flatListRef = useRef(null);
  const textInputRef = useRef(null);
  const fadeAnim = useRef(new Animated.Value(0)).current;

  // Quick questions for user
  const quickQuestions = [
    "What are early signs of breast cancer?",
    "How to do self-examination?",
    "What are risk factors?",
    "Where can I get screened?"
  ];

  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 500,
      useNativeDriver: true,
    }).start();
  }, []);

  useEffect(() => {
    const keyboardDidShowListener = Keyboard.addListener(
      'keyboardDidShow',
      (e) => {
        setKeyboardHeight(e.endCoordinates.height);
        setTimeout(() => {
          flatListRef.current?.scrollToEnd({ animated: true });
        }, 100);
      }
    );

    const keyboardDidHideListener = Keyboard.addListener(
      'keyboardDidHide',
      () => {
        setKeyboardHeight(0);
      }
    );

    return () => {
      keyboardDidShowListener.remove();
      keyboardDidHideListener.remove();
    };
  }, []);

  const handleSendMessage = async () => {
    if (!inputText.trim()) {
      Alert.alert('Empty Message', 'Please type a message before sending.');
      return;
    }

    const userMessage = {
      id: Date.now(),
      text: inputText.trim(),
      isUser: true,
      timestamp: new Date(),
      type: 'text'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);
    setIsTyping(true);
    Keyboard.dismiss();

    try {
      console.log('📤 Sending message to API...');
      const response = await sendChatMessage(inputText.trim());
      
      console.log('📥 API Response:', response);
      
      let botResponse = '';
      if (typeof response === 'string') {
        botResponse = response;
      } else if (response && response.response) {
        botResponse = response.response;
      } else if (response && response.message) {
        botResponse = response.message;
      } else {
        botResponse = "I understand your concern about breast health. I'm here to provide information and support. Could you tell me more about what you'd like to know?";
      }
      
      setTimeout(() => {
        setIsTyping(false);
        const botMessage = {
          id: Date.now() + 1,
          text: botResponse,
          isUser: false,
          timestamp: new Date(),
          type: 'text'
        };
        setMessages(prev => [...prev, botMessage]);
        setTimeout(() => {
          flatListRef.current?.scrollToEnd({ animated: true });
        }, 100);
      }, 1500);
      
    } catch (error) {
      console.error('💬 Chat error details:', error);
      setIsTyping(false);
      
      const errorMessage = {
        id: Date.now() + 1,
        text: `I'm having trouble connecting right now. ${error.message || 'Please check your internet connection and try again.'} Meanwhile, you can explore our resources section for helpful information about breast health!`,
        isUser: false,
        timestamp: new Date(),
        type: 'error'
      };
      setMessages(prev => [...prev, errorMessage]);
      
      Alert.alert(
        'Connection Issue', 
        `Cannot connect to chat service: ${error.message || 'Network error'}`,
        [{ text: 'OK' }]
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickQuestion = (question) => {
    setInputText(question);
    setTimeout(() => {
      textInputRef.current?.focus();
    }, 100);
  };

  const handleInputSubmit = () => {
    handleSendMessage();
  };

  const renderMessage = ({ item, index }) => {
    const showAvatar = index === 0 || messages[index - 1]?.isUser !== item.isUser;
    
    return (
      <Animated.View 
        style={[
          styles.messageRow,
          { opacity: fadeAnim }
        ]}
      >
        {!item.isUser && showAvatar && (
          <View style={styles.avatarContainer}>
            <View style={styles.avatar}>
              <Ionicons name="heart" size={16} color="white" />
            </View>
          </View>
        )}
        
        <View style={[
          styles.messageContainer,
          item.isUser ? styles.userMessage : styles.botMessage,
          item.type === 'welcome' && styles.welcomeMessage,
          item.type === 'error' && styles.errorMessage
        ]}>
          {item.type === 'welcome' && (
            <View style={styles.welcomeHeader}>
              <Ionicons name="sparkles" size={20} color="#FF69B4" />
              <Text style={styles.welcomeTitle}>Welcome to Breast Friend Forever!</Text>
            </View>
          )}
          
          <Text style={[
            styles.messageText,
            item.isUser ? styles.userMessageText : styles.botMessageText,
            item.type === 'welcome' && styles.welcomeText,
            item.type === 'error' && styles.errorText
          ]}>
            {item.text}
          </Text>
          
          <Text style={[
            styles.timestamp,
            item.isUser ? styles.userTimestamp : styles.botTimestamp
          ]}>
            {item.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </Text>
        </View>

        {item.isUser && showAvatar && (
          <View style={styles.avatarContainer}>
            <View style={[styles.avatar, styles.userAvatar]}>
              <Ionicons name="person" size={16} color="white" />
            </View>
          </View>
        )}
      </Animated.View>
    );
  };

  const renderQuickQuestions = () => (
    <View style={styles.quickQuestionsContainer}>
      <Text style={styles.quickQuestionsTitle}>Quick Questions:</Text>
      <View style={styles.questionsGrid}>
        {quickQuestions.map((question, index) => (
          <TouchableOpacity
            key={index}
            style={styles.questionChip}
            onPress={() => handleQuickQuestion(question)}
            activeOpacity={0.7}
          >
            <Text style={styles.questionText}>{question}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  const renderTypingIndicator = () => (
    <View style={styles.typingContainer}>
      <View style={styles.avatarContainer}>
        <View style={styles.avatar}>
          <Ionicons name="heart" size={16} color="white" />
        </View>
      </View>
      <View style={[styles.messageContainer, styles.botMessage]}>
        <View style={styles.typingDots}>
          <View style={styles.typingDot} />
          <View style={styles.typingDot} />
          <View style={styles.typingDot} />
        </View>
      </View>
    </View>
  );

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss} accessible={false}>
      <View style={styles.container}>
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.headerContent}>
            <View style={styles.botInfo}>
              <View style={[styles.avatar, styles.headerAvatar]}>
                <Ionicons name="heart" size={20} color="white" />
              </View>
              <View>
                <Text style={styles.botName}>Breast Health Companion</Text>
                <Text style={styles.botStatus}>
                  {isTyping ? 'Typing...' : 'Online • Ready to help'}
                </Text>
              </View>
            </View>
            <TouchableOpacity style={styles.infoButton}>
              <Ionicons name="information-circle" size={24} color={API_CONFIG.COLORS.PRIMARY} />
            </TouchableOpacity>
          </View>
        </View>

        {/* Messages List */}
        <FlatList
          ref={flatListRef}
          data={messages}
          renderItem={renderMessage}
          keyExtractor={item => item.id.toString()}
          style={styles.messagesList}
          contentContainerStyle={styles.messagesContent}
          onContentSizeChange={() => flatListRef.current?.scrollToEnd({ animated: true })}
          onLayout={() => flatListRef.current?.scrollToEnd({ animated: true })}
          ListHeaderComponent={messages.length <= 2 ? renderQuickQuestions : null}
          ListFooterComponent={isTyping ? renderTypingIndicator : null}
          showsVerticalScrollIndicator={false}
          keyboardShouldPersistTaps="handled"
        />

        {/* Input Container - FIXED AT BOTTOM */}
        <View style={styles.inputContainer}>
          <View style={styles.inputWrapper}>
            <TextInput
              ref={textInputRef}
              style={styles.textInput}
              value={inputText}
              onChangeText={setInputText}
              placeholder="Ask about breast health, symptoms, prevention..."
              placeholderTextColor="#999"
              multiline
              maxLength={500}
              returnKeyType="send"
              blurOnSubmit={false}
              editable={!isLoading}
            />
            <TouchableOpacity
              style={[
                styles.sendButton,
                (!inputText.trim() || isLoading) && styles.sendButtonDisabled
              ]}
              onPress={handleSendMessage}
              disabled={!inputText.trim() || isLoading}
              activeOpacity={0.7}
            >
              {isLoading ? (
                <Ionicons name="hourglass" size={20} color="#999" />
              ) : (
                <Ionicons
                  name="send"
                  size={20}
                  color={!inputText.trim() ? '#999' : 'white'}
                />
              )}
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </TouchableWithoutFeedback>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA',
  },
  header: {
    backgroundColor: 'white',
    paddingHorizontal: 16,
    paddingTop: 60,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#E8E8E8',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
    zIndex: 1000,
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  botInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  headerAvatar: {
    width: 44,
    height: 44,
    marginRight: 12,
  },
  botName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  botStatus: {
    fontSize: 12,
    color: '#4CAF50',
    marginTop: 2,
  },
  infoButton: {
    padding: 4,
  },
  messagesList: {
    flex: 1,
    backgroundColor: '#F8F9FA',
  },
  messagesContent: {
    paddingHorizontal: 16,
    paddingTop: 10,
    paddingBottom: 20,
  },
  messageRow: {
    flexDirection: 'row',
    marginVertical: 6,
    alignItems: 'flex-end',
  },
  avatarContainer: {
    width: 32,
    alignItems: 'center',
    marginHorizontal: 4,
  },
  avatar: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: API_CONFIG.COLORS.PRIMARY,
    justifyContent: 'center',
    alignItems: 'center',
  },
  userAvatar: {
    backgroundColor: '#6C63FF',
  },
  messageContainer: {
    maxWidth: '80%',
    padding: 14,
    borderRadius: 20,
    marginVertical: 2,
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: API_CONFIG.COLORS.PRIMARY,
    borderBottomRightRadius: 6,
  },
  botMessage: {
    alignSelf: 'flex-start',
    backgroundColor: 'white',
    borderBottomLeftRadius: 6,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 1,
  },
  welcomeMessage: {
    backgroundColor: '#FFF0F5',
    borderLeftWidth: 4,
    borderLeftColor: API_CONFIG.COLORS.PRIMARY,
    marginVertical: 10,
  },
  errorMessage: {
    backgroundColor: '#FFEBEE',
    borderLeftWidth: 4,
    borderLeftColor: '#F44336',
  },
  welcomeHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  welcomeTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: API_CONFIG.COLORS.PRIMARY,
    marginLeft: 8,
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
  },
  userMessageText: {
    color: 'white',
  },
  botMessageText: {
    color: '#333',
  },
  welcomeText: {
    color: '#666',
    lineHeight: 22,
  },
  errorText: {
    color: '#D32F2F',
  },
  timestamp: {
    fontSize: 11,
    marginTop: 6,
    opacity: 0.7,
  },
  userTimestamp: {
    color: 'rgba(255,255,255,0.8)',
    textAlign: 'right',
  },
  botTimestamp: {
    color: '#999',
  },
  quickQuestionsContainer: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 16,
    marginVertical: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  quickQuestionsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 12,
  },
  questionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  questionChip: {
    backgroundColor: '#F0F4FF',
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#E0E7FF',
  },
  questionText: {
    fontSize: 13,
    color: API_CONFIG.COLORS.PRIMARY,
    fontWeight: '500',
  },
  typingContainer: {
    flexDirection: 'row',
    marginVertical: 8,
    alignItems: 'flex-end',
  },
  typingDots: {
    flexDirection: 'row',
    alignItems: 'center',
    height: 20,
    paddingHorizontal: 10,
  },
  typingDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#999',
    marginHorizontal: 3,
  },
  inputContainer: {
    backgroundColor: 'white',
    borderTopWidth: 1,
    borderTopColor: '#E8E8E8',
    paddingHorizontal: 16,
    paddingVertical: 12,
    paddingBottom: Platform.OS === 'ios' ? 24 : 12,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'flex-end',
  },
  textInput: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#E0E0E0',
    borderRadius: 25,
    paddingHorizontal: 16,
    paddingVertical: 12,
    maxHeight: 100,
    marginRight: 12,
    backgroundColor: '#F8F9FA',
    fontSize: 16,
    textAlignVertical: 'center',
  },
  sendButton: {
    backgroundColor: API_CONFIG.COLORS.PRIMARY,
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: API_CONFIG.COLORS.PRIMARY,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 3,
  },
  sendButtonDisabled: {
    backgroundColor: '#E0E0E0',
    shadowOpacity: 0,
  },
});