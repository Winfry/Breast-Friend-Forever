// mobile/src/navigation/AppNavigator.js - Bottom tab navigation
import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';

// Import all screens
import SelfExamScreen from '../screens/SelfExamScreen';
import ChatScreen from '../screens/ChatScreen';
import ResourcesScreen from '../screens/ResourcesScreen';
import HospitalsScreen from '../screens/HospitalsScreen';
import EncouragementScreen from '../screens/EncouragementScreen';

const Tab = createBottomTabNavigator();

export default function AppNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          // Set icons for each tab
          if (route.name === 'Self Exam') {
            iconName = focused ? 'body' : 'body-outline';
          } else if (route.name === 'Chat Assistant') {
            iconName = focused ? 'chatbubbles' : 'chatbubbles-outline';
          } else if (route.name === 'Resources') {
            iconName = focused ? 'library' : 'library-outline';
          } else if (route.name === 'Hospitals') {
            iconName = focused ? 'medkit' : 'medkit-outline';
          } else if (route.name === 'Encouragement') {
            iconName = focused ? 'heart' : 'heart-outline';
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#FF69B4',
        tabBarInactiveTintColor: 'gray',
        tabBarStyle: {
          backgroundColor: 'white',
          borderTopWidth: 1,
          borderTopColor: '#f0f0f0',
          height: 60,
          paddingBottom: 10,
          paddingTop: 5,
        },
        headerStyle: {
          backgroundColor: '#FF69B4',
        },
        headerTintColor: 'white',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      })}
    >
      <Tab.Screen 
        name="Self Exam" 
        component={SelfExamScreen}
        options={{ title: '🤗 Self Exam Guide' }}
      />
      <Tab.Screen 
        name="Chat Assistant" 
        component={ChatScreen}
        options={{ title: '💬 Chat Assistant' }}
      />
      <Tab.Screen 
        name="Resources" 
        component={ResourcesScreen}
        options={{ title: '📚 Resources' }}
      />
      <Tab.Screen 
        name="Hospitals" 
        component={HospitalsScreen}
        options={{ title: '🏥 Find Screening' }}
      />
      <Tab.Screen 
        name="Encouragement" 
        component={EncouragementScreen}
        options={{ title: '💕 Encouragement' }}
      />
    </Tab.Navigator>
  );
}