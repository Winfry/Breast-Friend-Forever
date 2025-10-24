// mobile/src/styles/GlobalStyles.js - Global styling constants
import { StyleSheet, Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');

export const GlobalStyles = StyleSheet.create({
  // Colors
  colors: {
    primary: '#FF69B4',
    primaryDark: '#EC4899',
    primaryLight: '#FFF0F5',
    secondary: '#10B981',
    background: '#FFFFFF',
    text: {
      primary: '#1F2937',
      secondary: '#6B7280',
      light: '#9CA3AF'
    }
  },

  // Spacing
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32
  },

  // Typography
  typography: {
    header: {
      fontSize: 28,
      fontWeight: 'bold',
      color: '#1F2937',
    },
    subheader: {
      fontSize: 20,
      fontWeight: '600',
      color: '#1F2937',
    },
    body: {
      fontSize: 16,
      color: '#6B7280',
      lineHeight: 22,
    },
    caption: {
      fontSize: 14,
      color: '#9CA3AF',
    }
  },

  // Layout
  container: {
    flex: 1,
    backgroundColor: '#FFF0F5',
  },
  screenContainer: {
    flex: 1,
    backgroundColor: '#FFF0F5',
    paddingHorizontal: 16,
  },
  card: {
    backgroundColor: 'white',
    borderRadius: 16,
    padding: 16,
    marginVertical: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },

  // Buttons
  button: {
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonPrimary: {
    backgroundColor: '#FF69B4',
  },
  buttonSecondary: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: '#FF69B4',
  },
  buttonText: {
    fontSize: 16,
    fontWeight: '600',
    color: 'white',
  },
  buttonTextSecondary: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FF69B4',
  }
});