// src/screens/DebugScreen.js - Add this temporary screen
import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, StyleSheet, TouchableOpacity, Alert } from 'react-native';
import { checkBackendHealth, sendChatMessage } from '../services/api';
import { API_CONFIG } from '../services/apiConstants';

export default function DebugScreen() {
  const [logs, setLogs] = useState([]);
  const [apiStatus, setApiStatus] = useState('checking...');

  const addLog = (message) => {
    setLogs(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const testConnection = async () => {
    addLog('🔍 Testing backend connection...');
    const isHealthy = await checkBackendHealth();
    setApiStatus(isHealthy ? '✅ Connected' : '❌ Disconnected');
    addLog(isHealthy ? '✅ Backend is healthy!' : '❌ Backend connection failed');
  };

  const testChat = async () => {
    addLog('💬 Testing chat message...');
    try {
      const response = await sendChatMessage('Hello, test message');
      addLog(`✅ Chat response: ${JSON.stringify(response).substring(0, 100)}...`);
    } catch (error) {
      addLog(`❌ Chat error: ${error.message}`);
    }
  };

  const testDirectFetch = async () => {
    addLog('🌐 Testing direct fetch...');
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}/health`);
      addLog(`✅ Direct fetch: ${response.status} ${response.statusText}`);
    } catch (error) {
      addLog(`❌ Direct fetch error: ${error.message}`);
    }
  };

  useEffect(() => {
    testConnection();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Debug Information</Text>
      
      <View style={styles.statusContainer}>
        <Text style={styles.status}>API Status: {apiStatus}</Text>
        <Text style={styles.url}>URL: {API_CONFIG.BASE_URL}</Text>
      </View>

      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.button} onPress={testConnection}>
          <Text style={styles.buttonText}>Test Connection</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={testChat}>
          <Text style={styles.buttonText}>Test Chat</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={testDirectFetch}>
          <Text style={styles.buttonText}>Test Direct Fetch</Text>
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.logsContainer}>
        <Text style={styles.logsTitle}>Logs:</Text>
        {logs.map((log, index) => (
          <Text key={index} style={styles.log}>{log}</Text>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  statusContainer: {
    backgroundColor: 'white',
    padding: 15,
    borderRadius: 10,
    marginBottom: 20,
  },
  status: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  url: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  button: {
    backgroundColor: '#007AFF',
    padding: 10,
    borderRadius: 5,
    flex: 1,
    marginHorizontal: 5,
  },
  buttonText: {
    color: 'white',
    textAlign: 'center',
    fontWeight: 'bold',
  },
  logsContainer: {
    flex: 1,
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 15,
  },
  logsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  log: {
    fontSize: 12,
    fontFamily: 'monospace',
    marginBottom: 5,
  },
});