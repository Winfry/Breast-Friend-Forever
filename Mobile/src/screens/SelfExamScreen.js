// mobile/src/screens/SelfExamScreen.js - Self examination guide
import React, { useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Alert
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { GlobalStyles } from '../styles/GlobalStyles';

const SelfExamScreen = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState([]);

  const examSteps = [
    {
      id: 1,
      title: "Get Comfortable & Relax",
      description: "Find a quiet, private space where you can relax. Sit or stand in front of a mirror with your shoulders straight and arms on your hips. Take a few deep breaths to relax.",
      icon: "🪞",
      tip: "💖 Be gentle with yourself - this is about loving awareness, not criticism",
      color: "#FF69B4"
    },
    {
      id: 2,
      title: "Visual Inspection - Arms Down", 
      description: "Look for any changes in size, shape, color, or visible distortion. Check for swelling, dimpling, puckering, or changes in the nipple with arms at your sides.",
      icon: "👀",
      tip: "🌈 You're building a powerful health habit - that's something to celebrate!",
      color: "#EC4899"
    },
    {
      id: 3,
      title: "Raise Arms & Inspect",
      description: "Raise your arms overhead and look for the same changes. Notice if there's any fluid coming from one or both nipples. Check for symmetry and skin changes.",
      icon: "🙆‍♀️",
      tip: "🎵 Put on some calming music - make this your special self-care time",
      color: "#DB2777"
    },
    {
      id: 4,
      title: "Lie Down & Feel",
      description: "Lie down and use your right hand to feel your left breast, then left hand for right breast. Use a firm, smooth touch with the first few finger pads of your hand.",
      icon: "💆‍♀️",
      tip: "💫 You're learning your body's unique landscape - how amazing is that!",
      color: "#BE185D"
    },
    {
      id: 5,
      title: "Follow a Systematic Pattern", 
      description: "Use a systematic pattern - circular, up-and-down, or wedge. Cover the entire breast from collarbone to top of abdomen, armpit to cleavage.",
      icon: "🌀",
      tip: "🌟 Consistency creates confidence - you're building a lifelong health skill",
      color: "#9D174D"
    },
    {
      id: 6,
      title: "Final Check in Shower",
      description: "Many women find it easiest to feel their breasts when skin is wet and slippery. In the shower, repeat the same hand movements with soapy hands for better glide.",
      icon: "🚿",
      tip: "🎉 You did it! Regular checks are a beautiful act of self-love and care",
      color: "#831843"
    }
  ];

  const completeStep = (stepId) => {
    if (!completedSteps.includes(stepId)) {
      const newCompletedSteps = [...completedSteps, stepId];
      setCompletedSteps(newCompletedSteps);
      
      if (newCompletedSteps.length === examSteps.length) {
        Alert.alert(
          "🎉 Amazing!",
          "You've completed your self-exam training! You've learned a valuable lifelong skill.",
          [{ text: "Continue" }]
        );
      }
    }
  };

  const progress = completedSteps.length / examSteps.length;

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>🤗 Self-Exam Guide</Text>
        <Text style={styles.subtitle}>Learn with love, care, and confidence</Text>
      </View>

      {/* Progress Tracker */}
      <View style={styles.progressContainer}>
        <View style={styles.progressHeader}>
          <Text style={styles.progressTitle}>Your Progress</Text>
          <Text style={styles.progressText}>
            {completedSteps.length} of {examSteps.length} completed
          </Text>
        </View>
        <View style={styles.progressBar}>
          <View style={[styles.progressFill, { width: `${progress * 100}%` }]} />
        </View>
      </View>

      {/* Steps */}
      {examSteps.map((step, index) => (
        <TouchableOpacity 
          key={step.id}
          style={[
            styles.stepCard,
            completedSteps.includes(step.id) && styles.completedCard,
            currentStep === index && styles.currentCard
          ]}
          onPress={() => setCurrentStep(currentStep === index ? -1 : index)}
          activeOpacity={0.7}
        >
          <View style={styles.stepHeader}>
            <View style={[styles.stepIcon, { backgroundColor: step.color }]}>
              <Text style={styles.iconText}>{step.icon}</Text>
            </View>
            <View style={styles.stepInfo}>
              <Text style={styles.stepNumber}>Step {step.id}</Text>
              <Text style={styles.stepTitle}>{step.title}</Text>
              {completedSteps.includes(step.id) && (
                <View style={styles.completedBadge}>
                  <Ionicons name="checkmark" size={14} color="white" />
                  <Text style={styles.completedText}>Completed</Text>
                </View>
              )}
            </View>
            <Ionicons 
              name={currentStep === index ? "chevron-up" : "chevron-down"} 
              size={24} 
              color="#666" 
            />
          </View>

          {currentStep === index && (
            <View style={styles.stepDetails}>
              <Text style={styles.stepDescription}>{step.description}</Text>
              
              <View style={styles.tipContainer}>
                <Text style={styles.tipText}>{step.tip}</Text>
              </View>

              <View style={styles.buttonContainer}>
                <TouchableOpacity 
                  style={[styles.primaryButton, { backgroundColor: step.color }]}
                  onPress={() => completeStep(step.id)}
                >
                  <Ionicons name="checkmark-circle" size={20} color="white" />
                  <Text style={styles.primaryButtonText}>Mark Complete</Text>
                </TouchableOpacity>
              </View>
            </View>
          )}
        </TouchableOpacity>
      ))}

      {/* Completion Celebration */}
      {completedSteps.length === examSteps.length && (
        <View style={styles.completionContainer}>
          <Text style={styles.completionTitle}>🎊 Training Complete! 🎊</Text>
          <Text style={styles.completionText}>
            You've mastered breast self-examination! Remember to perform monthly checks.
          </Text>
          <View style={styles.certificate}>
            <Ionicons name="trophy" size={40} color="#FFD700" />
            <Text style={styles.certificateText}>Certificate of Completion</Text>
          </View>
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFF0F5',
  },
  header: {
    padding: 25,
    backgroundColor: '#FF69B4',
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 5,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: 'white',
    opacity: 0.9,
    textAlign: 'center',
  },
  progressContainer: {
    backgroundColor: 'white',
    margin: 16,
    padding: 20,
    borderRadius: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  progressHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  progressTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
  },
  progressText: {
    fontSize: 14,
    color: '#6B7280',
  },
  progressBar: {
    height: 8,
    backgroundColor: '#E5E7EB',
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#FF69B4',
    borderRadius: 4,
  },
  stepCard: {
    backgroundColor: 'white',
    borderRadius: 16,
    padding: 20,
    marginHorizontal: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  completedCard: {
    borderLeftWidth: 4,
    borderLeftColor: '#10B981',
    backgroundColor: '#F0FFF4',
  },
  currentCard: {
    borderLeftWidth: 4,
    borderLeftColor: '#FF69B4',
    backgroundColor: '#FFF0F5',
  },
  stepHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  stepIcon: {
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  iconText: {
    fontSize: 20,
  },
  stepInfo: {
    flex: 1,
  },
  stepNumber: {
    fontSize: 14,
    color: '#6B7280',
    marginBottom: 2,
  },
  stepTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 4,
  },
  completedBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#10B981',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
    alignSelf: 'flex-start',
  },
  completedText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '600',
    marginLeft: 4,
  },
  stepDetails: {
    marginTop: 16,
  },
  stepDescription: {
    fontSize: 16,
    color: '#6B7280',
    lineHeight: 22,
    marginBottom: 12,
  },
  tipContainer: {
    backgroundColor: '#FFF0F5',
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
  },
  tipText: {
    color: '#DB2777',
    fontStyle: 'italic',
    fontSize: 14,
    textAlign: 'center',
  },
  buttonContainer: {
    flexDirection: 'row',
  },
  primaryButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    borderRadius: 12,
    gap: 8,
  },
  primaryButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  completionContainer: {
    backgroundColor: 'white',
    margin: 16,
    padding: 25,
    borderRadius: 20,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  completionTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FF69B4',
    marginBottom: 10,
    textAlign: 'center',
  },
  completionText: {
    fontSize: 16,
    color: '#6B7280',
    textAlign: 'center',
    lineHeight: 22,
    marginBottom: 20,
  },
  certificate: {
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#FFF0F5',
    borderRadius: 15,
    borderWidth: 2,
    borderColor: '#FF69B4',
    borderStyle: 'dashed',
  },
  certificateText: {
    marginTop: 10,
    fontSize: 16,
    fontWeight: '600',
    color: '#FF69B4',
  },
});

export default SelfExamScreen;