import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import HomeScreen from './src/screens/HomeScreen';
import ChatScreen from './src/screens/ChatScreen';
import HospitalsScreen from './src/screens/HospitalsScreen';
import ResourcesScreen from './src/screens/ResourcesScreen';
import EncouragementScreen from './src/screens/EncouragementScreen';
import SelfExamScreen from './src/screens/SelfExamScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator 
        initialRouteName="Home"
        screenOptions={{
          headerStyle: {
            backgroundColor: '#e91e63',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen 
          name="Home" 
          component={HomeScreen}
          options={{ title: 'Breast Friend Forever 💖' }}
        />
        <Stack.Screen name="Chat" component={ChatScreen} />
        <Stack.Screen name="Hospitals" component={HospitalsScreen} />
        <Stack.Screen name="Resources" component={ResourcesScreen} />
        <Stack.Screen name="Encouragement" component={EncouragementScreen} />
        <Stack.Screen name="SelfExam" component={SelfExamScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}