// App.js - Updated with proper imports
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'expo-status-bar';

// Import screens
import HomeScreen from './src/screens/HomeScreen';
import ChatScreen from './src/screens/ChatScreen';
import HospitalsScreen from './src/screens/HospitalsScreen';
import ResourcesScreen from './src/screens/ResourcesScreen';
import EncouragementScreen from './src/screens/EncouragementScreen';
import SelfExamScreen from './src/screens/SelfExamScreen';

// Import styles
import Colors from './src/styles/colors';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="light" />
      <Stack.Navigator 
        initialRouteName="Home"
        screenOptions={{
          headerStyle: {
            backgroundColor: Colors.primary,
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
          headerBackTitle: 'Back',
        }}
      >
        <Stack.Screen 
          name="Home" 
          component={HomeScreen}
          options={{ 
            title: 'Breast Friend Forever 💖',
            headerShown: false 
          }}
        />
        <Stack.Screen 
          name="Chat" 
          component={ChatScreen}
          options={{ title: 'Chat Assistant' }}
        />
        <Stack.Screen 
          name="Hospitals" 
          component={HospitalsScreen}
          options={{ title: 'Healthcare Facilities' }}
        />
        <Stack.Screen 
          name="Resources" 
          component={ResourcesScreen}
          options={{ title: 'Educational Resources' }}
        />
        <Stack.Screen 
          name="Encouragement" 
          component={EncouragementScreen}
          options={{ title: 'Support Community' }}
        />
        <Stack.Screen 
          name="SelfExam" 
          component={SelfExamScreen}
          options={{ title: 'Self-Examination Guide' }}
        />
        <Stack.Screen 
          name="MobileFeatures" 
          component={MobileFeaturesScreen}
          options={{ title: 'Mobile Features' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}