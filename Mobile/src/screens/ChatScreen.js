// mobile/src/screens/ChatScreen.js - Chat with RAG backend
import React, { useState, useRef } from 'react';
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
  ActivityIndicator
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import apiService from '../utils/api';

import { GlobalStyles } from '../styles/GlobalStyles';

// Mock API service - replace with your actual RAG backend calls
const apiService = {
  async sendMessage(message) {
    // Simulate API call to your RAG backend
    return new Promise((resolve) => {
      setTimeout(() => {
        const responses = {
          'hello': "Hello! I'm your Breast Health Assistant. I can help answer questions about breast health, self-exams, and screening using our comprehensive knowledge base.",
          'self exam': "Monthly self-exams are recommended, ideally 3-5 days after your period ends. Would you like step-by-step instructions from our self-exam guide?",
          'symptoms': "Common breast changes include lumps, pain, nipple discharge, or skin changes. However, most breast changes are NOT cancer. I recommend consulting a healthcare professional for any concerning symptoms.",
          'mammogram': "Mammogram screening guidelines vary. Generally, women should start regular screenings between ages 40-50. Our database has the latest guidelines - would you like more specific information?",
          'default': "I understand you're asking about breast health. I can access our comprehensive medical database to provide you with accurate, up-to-date information. Could you please rephrase or ask about a specific topic?"
        };

        const lowerMessage = message.toLowerCase();
        let response = responses.default;

        Object.keys(responses).forEach(key => {
          if (lowerMessage.includes(key)) {
            response = responses[key];
          }
        });

        resolve({
          response,
          suggestions: [
            "Self-examination steps",
            "Common symptoms guide", 
            "Screening guidelines",
            "Find healthcare providers"
          ]
        });
      }, 1500);
    });
  }
};

const ChatScreen = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your Breast Health Assistant with access to comprehensive medical knowledge. I can help answer questions about breast health, self-exams, screening, and more. What would you like to know?",
      isUser: false,
      timestamp: new Date(),
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const flatListRef = useRef(null);

  const commonQuestions = [
    "How often should I do self-exams?",
    "What are early signs of breast cancer?",
    "When should I get a mammogram?",
    "Are breast lumps always cancerous?",
    "How to do proper self-examination?"
  ];

  const sendMessage = async () => {
    if (!inputText.trim()) return;

  const userMessage = {
    id: Date.now(),
    text: inputText,
    isUser: true,
    timestamp: new Date(),
  };

  setMessages(prev => [...prev, userMessage]);
  setInputText('');
  setIsLoading(true);

  try {
    // Call your actual RAG backend
    const response = await apiService.sendChatMessage(inputText);
    
    const botMessage = {
      id: Date.now() + 1,
      text: response.response || response.answer || "I've processed your question with our medical database.",
      isUser: false,
      timestamp: new Date(),
      suggestions: response.suggestions || [
        "Learn more about this topic",
        "Related health information",
        "Find healthcare providers"
      ]
    };

    setMessages(prev => [...prev, botMessage]);
  } catch (error) {
    console.error('Chat error:', error);
    
    const errorMessage = {
      id: Date.now() + 1,
      text: `I'm having trouble connecting to our medical database right now. Error: ${error.message}`,
      isUser: false,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, errorMessage]);
    
    // Show alert for network errors
    if (error.message.includes('Network')) {
      Alert.alert(
        "Connection Issue",
        "Please check your internet connection and try again.",
        [{ text: "OK" }]
      );
    }
  } finally {
    setIsLoading(false);
  }
};

  const handleQuickQuestion = (question) => {
    setInputText(question);
  };

  const renderMessage = ({ item }) => (
    <View style={[
      styles.messageContainer,
      item.isUser ? styles.userMessage : styles.botMessage
    ]}>
      <View style={[
        styles.messageBubble,
        item.isUser ? styles.userBubble : styles.botBubble
      ]}>
        <Text style={[
          styles.messageText,
          item.isUser ? styles.userMessageText : styles.botMessageText
        ]}>
          {item.text}
        </Text>
        
        {/* Suggestions for bot messages */}
        {!item.isUser && item.suggestions && (
          <View style={styles.suggestionsContainer}>
            <Text style={styles.suggestionsTitle}>Related questions:</Text>
            {item.suggestions.map((suggestion, index) => (
              <TouchableOpacity
                key={index}
                style={styles.suggestionButton}
                onPress={() => handleQuickQuestion(suggestion)}
              >
                <Text style={styles.suggestionText}>{suggestion}</Text>
              </TouchableOpacity>
            ))}
          </View>
        )}
        
        <Text style={styles.timestamp}>
          {item.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </Text>
      </View>
    </View>
  );

  return (
    <KeyboardAvoidingView 
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      keyboardVerticalOffset={90}
    >
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.botAvatar}>
          <Ionicons name="medical" size={24} color="white" />
        </View>
        <View style={styles.headerInfo}>
          <Text style={styles.headerTitle}>Breast Health Assistant</Text>
          <Text style={styles.headerSubtitle}>Powered by Medical AI • Online</Text>
        </View>
        <TouchableOpacity style={styles.infoButton}>
          <Ionicons name="information-circle" size={24} color="white" />
        </TouchableOpacity>
      </View>

      {/* Quick Questions */}
      <View style={styles.quickQuestionsContainer}>
        <Text style={styles.quickQuestionsTitle}>💡 Quick Questions</Text>
        <FlatList
          horizontal
          data={commonQuestions}
          showsHorizontalScrollIndicator={false}
          keyExtractor={(item, index) => index.toString()}
          renderItem={({ item }) => (
            <TouchableOpacity 
              style={styles.quickQuestion}
              onPress={() => handleQuickQuestion(item)}
            >
              <Text style={styles.quickQuestionText}>{item}</Text>
            </TouchableOpacity>
          )}
          contentContainerStyle={styles.quickQuestionsList}
        />
      </View>

      {/* Messages */}
      <FlatList
        ref={flatListRef}
        data={messages}
        renderItem={renderMessage}
        keyExtractor={(item) => item.id.toString()}
        style={styles.messagesList}
        contentContainerStyle={styles.messagesContainer}
        onContentSizeChange={() => flatListRef.current?.scrollToEnd()}
        showsVerticalScrollIndicator={false}
      />

      {/* Loading Indicator */}
      {isLoading && (
        <View style={styles.loadingContainer}>
          <View style={styles.loadingBubble}>
            <ActivityIndicator size="small" color="#FF69B4" />
            <Text style={styles.loadingText}>Consulting knowledge base...</Text>
          </View>
        </View>
      )}

      {/* Input Area */}
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.textInput}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Ask about breast health..."
          placeholderTextColor="#999"
          multiline
          maxLength={500}
          onSubmitEditing={sendMessage}
          returnKeyType="send"
        />
        <TouchableOpacity 
          style={[styles.sendButton, !inputText.trim() && styles.sendButtonDisabled]}
          onPress={sendMessage}
          disabled={!inputText.trim() || isLoading}
        >
          <Ionicons 
            name="send" 
            size={20} 
            color={inputText.trim() && !isLoading ? "white" : "#ccc"} 
          />
        </TouchableOpacity>
      </View>

      {/* Disclaimer */}
      <View style={styles.disclaimer}>
        <Ionicons name="warning" size={14} color="#666" />
        <Text style={styles.disclaimerText}>
          This assistant provides information from medical databases. For medical advice, consult a healthcare professional.
        </Text>
      </View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FF69B4',
    padding: 20,
    paddingTop: 60,
  },
  botAvatar: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#EC4899',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  headerInfo: {
    flex: 1,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
  },
  headerSubtitle: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.8)',
    marginTop: 2,
  },
  infoButton: {
    padding: 4,
  },
  quickQuestionsContainer: {
    backgroundColor: 'white',
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e5e5e5',
  },
  quickQuestionsTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    marginLeft: 16,
    marginBottom: 12,
  },
  quickQuestionsList: {
    paddingHorizontal: 12,
  },
  quickQuestion: {
    backgroundColor: '#FFF0F5',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 20,
    marginHorizontal: 4,
    borderWidth: 1,
    borderColor: '#FF69B4',
  },
  quickQuestionText: {
    color: '#FF69B4',
    fontSize: 12,
    fontWeight: '500',
  },
  messagesList: {
    flex: 1,
  },
  messagesContainer: {
    padding: 16,
    paddingBottom: 8,
  },
  messageContainer: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  userMessage: {
    justifyContent: 'flex-end',
  },
  botMessage: {
    justifyContent: 'flex-start',
  },
  messageBubble: {
    maxWidth: '80%',
    padding: 16,
    borderRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  userBubble: {
    backgroundColor: '#FF69B4',
    borderBottomRightRadius: 6,
  },
  botBubble: {
    backgroundColor: 'white',
    borderBottomLeftRadius: 6,
  },
  messageText: {
    fontSize: 16,
    lineHeight: 20,
  },
  userMessageText: {
    color: 'white',
  },
  botMessageText: {
    color: '#333',
  },
  suggestionsContainer: {
    marginTop: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: 'rgba(0,0,0,0.1)',
  },
  suggestionsTitle: {
    fontSize: 12,
    fontWeight: '600',
    color: '#666',
    marginBottom: 8,
  },
  suggestionButton: {
    backgroundColor: '#f8f9fa',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    marginBottom: 6,
    borderWidth: 1,
    borderColor: '#e5e5e5',
  },
  suggestionText: {
    fontSize: 12,
    color: '#FF69B4',
    fontWeight: '500',
  },
  timestamp: {
    fontSize: 11,
    color: 'rgba(255,255,255,0.7)',
    marginTop: 8,
    alignSelf: 'flex-end',
  },
  loadingContainer: {
    flexDirection: 'row',
    marginBottom: 16,
    paddingHorizontal: 16,
  },
  loadingBubble: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 20,
    borderBottomLeftRadius: 6,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  loadingText: {
    color: '#666',
    fontSize: 14,
    fontStyle: 'italic',
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    padding: 16,
    backgroundColor: 'white',
    borderTopWidth: 1,
    borderTopColor: '#e5e5e5',
  },
  textInput: {
    flex: 1,
    backgroundColor: '#f8f9fa',
    borderWidth: 1,
    borderColor: '#e5e5e5',
    borderRadius: 25,
    paddingHorizontal: 20,
    paddingVertical: 12,
    paddingTop: 12,
    marginRight: 12,
    maxHeight: 100,
    fontSize: 16,
    lineHeight: 20,
  },
  sendButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#FF69B4',
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: '#f0f0f0',
  },
  disclaimer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f8f9fa',
    padding: 12,
    paddingHorizontal: 16,
    borderTopWidth: 1,
    borderTopColor: '#e5e5e5',
  },
  disclaimerText: {
    flex: 1,
    fontSize: 11,
    color: '#666',
    marginLeft: 6,
    fontStyle: 'italic',
    lineHeight: 14,
  },
});

export default ChatScreen;