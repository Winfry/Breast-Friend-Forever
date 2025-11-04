// src/components/Animations/LoadingAnimation.js
import React, { useEffect, useRef } from 'react';
import { View, Animated, StyleSheet } from 'react-native';
import Colors from '../../styles/colors';

const LoadingAnimation = ({ dotCount = 3, color = Colors.primary, size = 8 }) => {
  const dots = useRef(Array.from({ length: dotCount }, () => new Animated.Value(0))).current;

  useEffect(() => {
    const animations = dots.map((dot, index) =>
      Animated.sequence([
        Animated.timing(dot, {
          toValue: 1,
          duration: 400,
          delay: index * 200,
          useNativeDriver: true,
        }),
        Animated.timing(dot, {
          toValue: 0,
          duration: 400,
          useNativeDriver: true,
        }),
      ])
    );

    Animated.loop(Animated.stagger(200, animations)).start();
  }, [dots]);

  return (
    <View style={styles.container}>
      {dots.map((dot, index) => (
        <Animated.View
          key={index}
          style={[
            styles.dot,
            {
              width: size,
              height: size,
              borderRadius: size / 2,
              backgroundColor: color,
              transform: [
                {
                  scale: dot.interpolate({
                    inputRange: [0, 1],
                    outputRange: [0.5, 1.2],
                  }),
                },
              ],
              opacity: dot.interpolate({
                inputRange: [0, 1],
                outputRange: [0.3, 1],
              }),
            },
          ]}
        />
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  dot: {
    marginHorizontal: 4,
  },
});

export default LoadingAnimation;