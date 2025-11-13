// src/screens/ChatScreen.js - Professional GiftedChat Implementation
import React, { useState, useCallback } from 'react';
import { View, TouchableOpacity, StyleSheet } from 'react-native';
import { GiftedChat, Bubble, InputToolbar, Send } from 'react-native-gifted-chat';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { sendChatMessage } from '../services/api';
import { API_CONFIG } from '../services/apiConstants';

export default function ChatScreen() {
  const [messages, setMessages] = useState([
    {
      _id: 1,
      text: "Hello! I'm your Breast Health Assistant. How can I help you today? 💖",
      createdAt: new Date(),
      user: {
        _id: 2,
        name: 'Breast Health Assistant',
        avatar: '💖',
      },
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const onSend = useCallback(async (newMessages = []) => {
    // Add user message immediately
    setMessages((previousMessages) =>
      GiftedChat.append(previousMessages, newMessages)
    );

    const userMessage = newMessages[0];
    setIsTyping(true);

    try {
      // Call your backend API
      const response = await sendChatMessage(userMessage.text);

      // Create bot response
      const botMessage = {
        _id: Math.random().toString(36).substring(7),
        text: response.response || response.message || "I'm here to help with your breast health questions.",
        createdAt: new Date(),
        user: {
          _id: 2,
          name: 'Breast Health Assistant',
          avatar: '💖',
        },
      };

      setMessages((previousMessages) =>
        GiftedChat.append(previousMessages, [botMessage])
      );
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        _id: Math.random().toString(36).substring(7),
        text: "I apologize, but I'm having trouble connecting right now. Please try again.",
        createdAt: new Date(),
        user: {
          _id: 2,
          name: 'Breast Health Assistant',
          avatar: '💖',
        },
      };
      setMessages((previousMessages) =>
        GiftedChat.append(previousMessages, [errorMessage])
      );
    } finally {
      setIsTyping(false);
    }
  }, []);

  const renderBubble = (props) => {
    return (
      <Bubble
        {...props}
        wrapperStyle={{
          right: {
            backgroundColor: API_CONFIG.COLORS.PRIMARY,
            borderRadius: 16,
            padding: 2,
            marginBottom: 8,
          },
          left: {
            backgroundColor: '#F0F0F0',
            borderRadius: 16,
            padding: 2,
            marginBottom: 8,
          },
        }}
        textStyle={{
          right: {
            color: '#FFFFFF',
            fontSize: 16,
          },
          left: {
            color: '#000000',
            fontSize: 16,
          },
        }}
      />
    );
  };

  const renderInputToolbar = (props) => {
    return (
      <InputToolbar
        {...props}
        containerStyle={styles.inputToolbar}
        primaryStyle={styles.inputPrimary}
      />
    );
  };

  const renderSend = (props) => {
    return (
      <Send {...props}>
        <View style={styles.sendButton}>
          <Ionicons name="send" size={24} color={API_CONFIG.COLORS.PRIMARY} />
        </View>
      </Send>
    );
  };

  return (
    <SafeAreaView style={styles.container} edges={['bottom']}>
      <GiftedChat
        messages={messages}
        onSend={(messages) => onSend(messages)}
        user={{
          _id: 1,
        }}
        renderBubble={renderBubble}
        renderInputToolbar={renderInputToolbar}
        renderSend={renderSend}
        isTyping={isTyping}
        placeholder="Type your question..."
        alwaysShowSend
        scrollToBottom
        showUserAvatar={false}
        renderAvatar={null}
        textInputProps={{
          style: styles.textInput,
        }}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  inputToolbar: {
    backgroundColor: '#FFFFFF',
    borderTopWidth: 1,
    borderTopColor: '#E8E8E8',
    paddingHorizontal: 8,
    paddingVertical: 8,
  },
  inputPrimary: {
    alignItems: 'center',
  },
  textInput: {
    backgroundColor: '#F5F5F5',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 8,
    fontSize: 16,
    color: '#000',
    marginLeft: 0,
  },
  sendButton: {
    justifyContent: 'center',
    alignItems: 'center',
    width: 44,
    height: 44,
    marginRight: 4,
    marginBottom: 4,
  },
});
