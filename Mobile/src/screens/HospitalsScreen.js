// src/screens/HospitalsScreen.js - Enhanced Version
import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  Alert,
  TouchableOpacity,
  Linking,
  ScrollView,
  Animated,
  RefreshControl
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { getHospitals } from '../services/api';
import { API_CONFIG } from '../services/apiConstants';

export default function HospitalsScreen() {
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [apiStatus, setApiStatus] = useState('checking...');
  const fadeAnim = useRef(new Animated.Value(0)).current;

  const filters = [
    { id: 'all', label: 'All Facilities', icon: '🏥' },
    { id: 'screening', label: 'Screening', icon: '🔍' },
    { id: 'support', label: 'Support', icon: '💖' },
    { id: 'emergency', label: '24/7', icon: '🚨' }
  ];

  useEffect(() => {
    loadHospitals();
    checkAPIStatus();
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 600,
      useNativeDriver: true,
    }).start();
  }, []);

  const checkAPIStatus = async () => {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}/health`);
      setApiStatus(response.ok ? 'connected' : 'error');
    } catch (error) {
      setApiStatus('disconnected');
    }
  };

  const loadHospitals = async () => {
    try {
      setLoading(true);
      console.log('🏥 Starting hospitals data load...');
      
      const data = await getHospitals();
      console.log('🏥 Raw hospitals data:', data);
      
      // Enhanced data processing with fallbacks
      const enrichedData = Array.isArray(data) ? data.map((hospital, index) => {
        // Ensure all required fields exist
        const enrichedHospital = {
          id: hospital.id || index + 1,
          name: hospital.name || hospital.Facility_N || 'Healthcare Facility',
          address: hospital.address || hospital.Location || hospital.Address || 'Address not available',
          phone: hospital.phone || hospital.Phone || '+254 XXX XXX XXX',
          services: hospital.services || hospital.Services || 'General healthcare services',
          hours: hospital.hours || hospital.Hours || 'Mon-Fri: 8AM-5PM',
          specialty: hospital.specialty || hospital.Specialty || getRandomSpecialty(),
          insurance: hospital.insurance || ['NHIF', 'Private Pay'],
          rating: typeof hospital.rating === 'number' ? hospital.rating : (Math.random() * 2 + 3), // 3-5 stars
          waitTime: hospital.waitTime || Math.floor(Math.random() * 30) + 10, // 10-40 mins
          isOpen: hospital.isOpen !== undefined ? hospital.isOpen : Math.random() > 0.2,
          type: hospital.type || hospital.Type || 'Medical Clinic',
          county: hospital.county || hospital.County || 'Nairobi',
          latitude: hospital.latitude || hospital.lat || hospital.Latitude || -1.286389,
          longitude: hospital.longitude || hospital.lon || hospital.Longitude || 36.817223
        };
        
        console.log(`🏥 Processed hospital ${index + 1}:`, enrichedHospital.name);
        return enrichedHospital;
      }) : defaultHospitals;
      
      console.log(`🏥 Loaded ${enrichedData.length} hospitals`);
      setHospitals(enrichedData);
      
    } catch (error) {
      console.error('🏥 Hospital loading error:', error);
      Alert.alert(
        'Info', 
        'Using sample data. Real hospital data will load when backend is connected.',
        [{ text: 'OK' }]
      );
      setHospitals(defaultHospitals);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadHospitals();
    checkAPIStatus();
  };

  const getRandomSpecialty = () => {
    const specialties = [
      'Breast Cancer Center',
      'Women Health Specialist',
      'Comprehensive Care',
      'Oncology Center',
      'Mammography Expert'
    ];
    return specialties[Math.floor(Math.random() * specialties.length)];
  };

  const handleCall = (phoneNumber) => {
    Linking.openURL(`tel:${phoneNumber}`).catch(err => 
      Alert.alert('Error', 'Could not make a call')
    );
  };

  const handleDirections = (address) => {
    const encodedAddress = encodeURIComponent(address);
    Linking.openURL(`https://maps.google.com/?q=${encodedAddress}`).catch(err =>
      Alert.alert('Error', 'Could not open maps')
    );
  };

  const handleBookAppointment = (hospital) => {
    Alert.alert(
      'Book Appointment',
      `Would you like to book an appointment at ${hospital.name}?`,
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Call Now', onPress: () => handleCall(hospital.phone) },
        { text: 'Visit Website', onPress: () => Linking.openURL('https://example.com') }
      ]
    );
  };

  const renderHospitalItem = ({ item, index }) => (
    <Animated.View 
      style={[
        styles.hospitalCard,
        { 
          opacity: fadeAnim,
          transform: [{
            translateY: fadeAnim.interpolate({
              inputRange: [0, 1],
              outputRange: [50, 0]
            })
          }]
        }
      ]}
    >
      {/* Hospital Header */}
      <View style={styles.hospitalHeader}>
        <View style={styles.hospitalMainInfo}>
          <View style={styles.nameContainer}>
            <Text style={styles.hospitalName}>{item.name}</Text>
            {item.isOpen ? (
              <View style={styles.openBadge}>
                <Ionicons name="time" size={12} color="white" />
                <Text style={styles.openText}>OPEN</Text>
              </View>
            ) : (
              <View style={styles.closedBadge}>
                <Text style={styles.closedText}>CLOSED</Text>
              </View>
            )}
          </View>
          <Text style={styles.hospitalSpecialty}>{item.specialty}</Text>
        </View>
        
        <View style={styles.ratingContainer}>
          <Ionicons name="star" size={16} color="#FFD700" />
          <Text style={styles.ratingText}>{(item.rating || 4.0).toFixed(1)}</Text>
        </View>
      </View>

      {/* Details Grid */}
      <View style={styles.detailsGrid}>
        <View style={styles.detailItem}>
          <Ionicons name="location" size={16} color={API_CONFIG.COLORS.PRIMARY} />
          <Text style={styles.detailText} numberOfLines={2}>{item.address}</Text>
        </View>
        
        <View style={styles.detailItem}>
          <Ionicons name="call" size={16} color={API_CONFIG.COLORS.PRIMARY} />
          <Text style={styles.detailText}>{item.phone}</Text>
        </View>
        
        <View style={styles.detailItem}>
          <Ionicons name="time" size={16} color={API_CONFIG.COLORS.PRIMARY} />
          <Text style={styles.detailText}>{item.hours}</Text>
        </View>
        
        <View style={styles.detailItem}>
          <Ionicons name="medkit" size={16} color={API_CONFIG.COLORS.PRIMARY} />
          <Text style={styles.detailText} numberOfLines={1}>{Array.isArray(item.insurance) ? item.insurance.join(', ') : item.insurance}</Text>
        </View>
      </View>

      {/* Services */}
      <View style={styles.servicesContainer}>
        <Text style={styles.servicesLabel}>Specialized Services:</Text>
        <View style={styles.servicesTags}>
          {item.services.split(', ').map((service, idx) => (
            <View key={idx} style={styles.serviceTag}>
              <Text style={styles.serviceText}>{service.trim()}</Text>
            </View>
          ))}
        </View>
      </View>

      {/* Action Buttons */}
      <View style={styles.actionButtons}>
        <TouchableOpacity 
          style={[styles.actionButton, styles.secondaryButton]}
          onPress={() => handleDirections(item.address)}
        >
          <Ionicons name="navigate" size={16} color={API_CONFIG.COLORS.PRIMARY} />
          <Text style={styles.secondaryButtonText}>Directions</Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={[styles.actionButton, styles.secondaryButton]}
          onPress={() => handleCall(item.phone)}
        >
          <Ionicons name="call" size={16} color={API_CONFIG.COLORS.PRIMARY} />
          <Text style={styles.secondaryButtonText}>Call</Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={[styles.actionButton, styles.primaryButton]}
          onPress={() => handleBookAppointment(item)}
        >
          <Ionicons name="calendar" size={16} color="white" />
          <Text style={styles.primaryButtonText}>Book Visit</Text>
        </TouchableOpacity>
      </View>

      {/* Wait Time Info */}
      <View style={styles.waitTimeContainer}>
        <Ionicons name="information-circle" size={14} color="#666" />
        <Text style={styles.waitTimeText}>
          Average wait time: {item.waitTime} minutes
        </Text>
      </View>
    </Animated.View>
  );

  const renderFilterChip = (filter) => (
    <TouchableOpacity
      key={filter.id}
      style={[
        styles.filterChip,
        selectedFilter === filter.id && styles.filterChipActive
      ]}
      onPress={() => setSelectedFilter(filter.id)}
    >
      <Text style={styles.filterIcon}>{filter.icon}</Text>
      <Text style={[
        styles.filterText,
        selectedFilter === filter.id && styles.filterTextActive
      ]}>
        {filter.label}
      </Text>
    </TouchableOpacity>
  );

  const NetworkDebugInfo = () => (
    <View style={styles.debugContainer}>
      <Text style={styles.debugText}>
        API Status: {apiStatus} | Hospitals: {hospitals.length}
      </Text>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color={API_CONFIG.COLORS.PRIMARY} />
        <Text style={styles.loadingText}>Finding healthcare facilities near you...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerContent}>
          <View>
            <Text style={styles.title}>🏥 Healthcare Facilities</Text>
            <Text style={styles.subtitle}>
              Find breast cancer screening and support centers
            </Text>
          </View>
          <TouchableOpacity style={styles.locationButton}>
            <Ionicons name="navigate" size={20} color={API_CONFIG.COLORS.PRIMARY} />
            <Text style={styles.locationText}>Near Me</Text>
          </TouchableOpacity>
        </View>

        {/* Quick Stats */}
        <View style={styles.statsContainer}>
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>{hospitals.length}</Text>
            <Text style={styles.statLabel}>Facilities</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>
              {hospitals.filter(h => h.isOpen).length}
            </Text>
            <Text style={styles.statLabel}>Open Now</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>
              {hospitals.filter(h => (h.rating || 0) >= 4).length}
            </Text>
            <Text style={styles.statLabel}>Top Rated</Text>
          </View>
        </View>
      </View>

      {/* Network Debug Info */}
      <NetworkDebugInfo />

      {/* Filter Chips */}
      <ScrollView 
        horizontal 
        showsHorizontalScrollIndicator={false}
        style={styles.filtersContainer}
        contentContainerStyle={styles.filtersContent}
      >
        {filters.map(renderFilterChip)}
      </ScrollView>

      {/* Hospital List */}
      <FlatList
        data={hospitals}
        renderItem={renderHospitalItem}
        keyExtractor={item => item.id.toString()}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            colors={[API_CONFIG.COLORS.PRIMARY]}
          />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Ionicons name="search" size={64} color="#E0E0E0" />
            <Text style={styles.emptyTitle}>No facilities found</Text>
            <Text style={styles.emptyText}>
              Try adjusting your filters or check back later for updated listings.
            </Text>
          </View>
        }
      />
    </View>
  );
}

// Enhanced default data with Kenyan hospitals
const defaultHospitals = [
  {
    id: 1,
    name: 'Nairobi Women\'s Hospital',
    address: 'James Gichuru Road, Lavington, Nairobi, Kenya',
    phone: '+254 20 272 6000',
    services: 'Mammography, Ultrasound, Biopsy, Breast Surgery, Oncology',
    hours: '24/7',
    specialty: 'Comprehensive Women\'s Healthcare',
    insurance: ['NHIF', 'Madison', 'Jubilee', 'AAR', 'Private Pay'],
    rating: 4.8,
    waitTime: 15,
    isOpen: true,
    type: 'National Hospital',
    county: 'Nairobi',
    latitude: -1.2684,
    longitude: 36.7965
  },
  {
    id: 2,
    name: 'Aga Khan University Hospital',
    address: '3rd Parklands Avenue, Nairobi, Kenya',
    phone: '+254 20 366 2000',
    services: 'Breast Screening, Genetic Testing, Surgical Oncology, Radiation Therapy',
    hours: 'Mon-Sun: 6AM-10PM',
    specialty: 'Comprehensive Cancer Care',
    insurance: ['NHIF', 'Jubilee', 'AAR', 'CIC', 'Liberty'],
    rating: 4.9,
    waitTime: 20,
    isOpen: true,
    type: 'National Hospital',
    county: 'Nairobi',
    latitude: -1.2545,
    longitude: 36.8004
  },
  {
    id: 3,
    name: 'Kenyatta National Hospital',
    address: 'Hospital Road, Nairobi, Kenya',
    phone: '+254 20 272 6300',
    services: 'Mammography, Clinical Breast Exam, Biopsy, Cancer Treatment',
    hours: '24/7',
    specialty: 'National Referral Hospital',
    insurance: ['NHIF', 'All major providers'],
    rating: 4.5,
    waitTime: 30,
    isOpen: true,
    type: 'National Hospital',
    county: 'Nairobi',
    latitude: -1.3045,
    longitude: 36.8075
  },
  {
    id: 4,
    name: 'Mombasa Hospital',
    address: 'Mama Ngina Drive, Mombasa, Kenya',
    phone: '+254 41 231 2191',
    services: 'Breast Screening, Ultrasound, Women\'s Health, Consultation',
    hours: 'Mon-Sun: 7AM-9PM',
    specialty: 'Coastal Healthcare Services',
    insurance: ['NHIF', 'Madison', 'Jubilee'],
    rating: 4.3,
    waitTime: 25,
    isOpen: true,
    type: 'County Hospital',
    county: 'Mombasa',
    latitude: -4.0547,
    longitude: 39.6636
  },
  {
    id: 5,
    name: 'Nakuru General Hospital',
    address: 'Hospital Road, Nakuru, Kenya',
    phone: '+254 51 221 0000',
    services: 'Breast Screening, Clinical Exams, Basic Diagnostics',
    hours: 'Mon-Sun: 24/7',
    specialty: 'Regional Healthcare Services',
    insurance: ['NHIF', 'Private Pay'],
    rating: 4.2,
    waitTime: 35,
    isOpen: true,
    type: 'County Hospital',
    county: 'Nakuru',
    latitude: -0.3031,
    longitude: 36.0800
  }
];

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA',
  },
  header: {
    backgroundColor: 'white',
    paddingHorizontal: 20,
    paddingTop: 60,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#E8E8E8',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    maxWidth: '80%',
  },
  locationButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F0F4FF',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
    gap: 6,
  },
  locationText: {
    fontSize: 14,
    color: API_CONFIG.COLORS.PRIMARY,
    fontWeight: '500',
  },
  statsContainer: {
    flexDirection: 'row',
    backgroundColor: '#F8F9FA',
    borderRadius: 12,
    padding: 12,
  },
  statItem: {
    flex: 1,
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 20,
    fontWeight: 'bold',
    color: API_CONFIG.COLORS.PRIMARY,
    marginBottom: 2,
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
  },
  statDivider: {
    width: 1,
    backgroundColor: '#E0E0E0',
    marginHorizontal: 8,
  },
  debugContainer: {
    backgroundColor: '#f0f0f0',
    padding: 8,
    margin: 16,
    borderRadius: 8,
  },
  debugText: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
  },
  filtersContainer: {
    backgroundColor: 'white',
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  filtersContent: {
    paddingHorizontal: 16,
    paddingVertical: 12,
    gap: 8,
  },
  filterChip: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F8F9FA',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#E8E8E8',
    gap: 6,
    marginRight: 8,
  },
  filterChipActive: {
    backgroundColor: API_CONFIG.COLORS.PRIMARY,
    borderColor: API_CONFIG.COLORS.PRIMARY,
  },
  filterIcon: {
    fontSize: 14,
  },
  filterText: {
    fontSize: 14,
    color: '#666',
    fontWeight: '500',
  },
  filterTextActive: {
    color: 'white',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F8F9FA',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
  listContent: {
    padding: 16,
  },
  hospitalCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  hospitalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  hospitalMainInfo: {
    flex: 1,
    marginRight: 12,
  },
  nameContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
    flexWrap: 'wrap',
  },
  hospitalName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginRight: 8,
    flex: 1,
  },
  openBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#4CAF50',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
    gap: 4,
  },
  openText: {
    fontSize: 10,
    color: 'white',
    fontWeight: 'bold',
  },
  closedBadge: {
    backgroundColor: '#F44336',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  closedText: {
    fontSize: 10,
    color: 'white',
    fontWeight: 'bold',
  },
  hospitalSpecialty: {
    fontSize: 14,
    color: API_CONFIG.COLORS.PRIMARY,
    fontWeight: '500',
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFF9C4',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
    gap: 4,
  },
  ratingText: {
    fontSize: 12,
    color: '#333',
    fontWeight: 'bold',
  },
  detailsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    marginBottom: 16,
  },
  detailItem: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    minWidth: '45%',
    gap: 6,
  },
  detailText: {
    fontSize: 12,
    color: '#666',
    flex: 1,
  },
  servicesContainer: {
    marginBottom: 16,
  },
  servicesLabel: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  servicesTags: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
  },
  serviceTag: {
    backgroundColor: '#F0F4FF',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  serviceText: {
    fontSize: 10,
    color: API_CONFIG.COLORS.PRIMARY,
    fontWeight: '500',
  },
  actionButtons: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 12,
  },
  actionButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 10,
    borderRadius: 10,
    gap: 6,
  },
  secondaryButton: {
    backgroundColor: '#F8F9FA',
    borderWidth: 1,
    borderColor: '#E8E8E8',
  },
  primaryButton: {
    backgroundColor: API_CONFIG.COLORS.PRIMARY,
  },
  secondaryButtonText: {
    fontSize: 12,
    color: API_CONFIG.COLORS.PRIMARY,
    fontWeight: '500',
  },
  primaryButtonText: {
    fontSize: 12,
    color: 'white',
    fontWeight: '500',
  },
  waitTimeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  waitTimeText: {
    fontSize: 11,
    color: '#666',
    fontStyle: 'italic',
  },
  emptyContainer: {
    alignItems: 'center',
    padding: 40,
  },
  emptyTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#666',
    marginTop: 16,
    marginBottom: 8,
  },
  emptyText: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
    lineHeight: 20,
  },
});