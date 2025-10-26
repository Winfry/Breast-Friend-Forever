// mobile/src/screens/HospitalsScreen.js - Complete version
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Alert,
  Linking,
  ActivityIndicator,
  RefreshControl,
  Platform
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import MapView, { Marker, PROVIDER_GOOGLE } from 'react-native-maps';
import * as Location from 'expo-location';
import { GlobalStyles } from '../styles/GlobalStyles';
import apiService from '../utils/api';

const HospitalsScreen = () => {
  const [location, setLocation] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);
  const [selectedHospital, setSelectedHospital] = useState(null);
  const [refreshing, setRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [hospitals, setHospitals] = useState([]);

  // Sample hospital data - will be replaced with API call
  const sampleHospitals = [
    {
      id: 1,
      name: "City General Hospital",
      address: "123 Medical Center Dr, City, State 12345",
      phone: "(555) 123-4567",
      distance: "2.3",
      services: ["Mammography", "Breast Screening", "Oncology"],
      hours: "Mon-Fri: 8AM-6PM, Sat: 9AM-1PM",
      latitude: 37.7749,
      longitude: -122.4194,
      rating: 4.5,
      website: "https://citygeneral.com"
    },
    {
      id: 2,
      name: "Women's Health Center",
      address: "456 Health Plaza, City, State 12345",
      phone: "(555) 234-5678",
      distance: "3.1",
      services: ["3D Mammography", "Breast Ultrasound", "Biopsy"],
      hours: "Mon-Fri: 7AM-7PM, Sat-Sun: 9AM-3PM",
      latitude: 37.7849,
      longitude: -122.4294,
      rating: 4.8,
      website: "https://womenshealthcenter.com"
    },
    {
      id: 3,
      name: "Community Breast Center",
      address: "789 Care Avenue, City, State 12345",
      phone: "(555) 345-6789",
      distance: "4.2",
      services: ["Screening", "Diagnostic Imaging", "Support Groups"],
      hours: "Mon-Thu: 7:30AM-5PM, Fri: 7:30AM-4PM",
      latitude: 37.7649,
      longitude: -122.4094,
      rating: 4.6,
      website: "https://communitybreastcenter.org"
    }
  ];

  useEffect(() => {
    getLocation();
    loadHospitals();
  }, []);

  const getLocation = async () => {
    setLoading(true);
    try {
      let { status } = await Location.requestForegroundPermissionsAsync();
      
      if (status !== 'granted') {
        setErrorMsg('Permission to access location was denied');
        setHospitals(sampleHospitals);
        setLoading(false);
        return;
      }

      let location = await Location.getCurrentPositionAsync({});
      setLocation(location.coords);
    } catch (error) {
      setErrorMsg('Failed to get location');
      setHospitals(sampleHospitals);
      console.error('Location error:', error);
    }
    setLoading(false);
  };

  const loadHospitals = async () => {
    try {
      // TODO: Replace with actual API call
      // const hospitalsData = await apiService.getHospitals();
      // setHospitals(hospitalsData);
      setHospitals(sampleHospitals);
    } catch (error) {
      console.error('Failed to load hospitals:', error);
      setHospitals(sampleHospitals); // Fallback to sample data
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await getLocation();
    await loadHospitals();
    setRefreshing(false);
  };

  const callHospital = (phoneNumber) => {
    Linking.openURL(`tel:${phoneNumber}`).catch(err => 
      Alert.alert('Error', 'Could not make call')
    );
  };

  const openDirections = (hospital) => {
    const url = Platform.select({
      ios: `maps:0,0?q=${hospital.latitude},${hospital.longitude}(${hospital.name})`,
      android: `geo:0,0?q=${hospital.latitude},${hospital.longitude}(${hospital.name})`
    });
    
    Linking.openURL(url).catch(err => 
      Alert.alert('Error', 'Could not open maps')
    );
  };

  const openWebsite = (url) => {
    Linking.openURL(url).catch(err => 
      Alert.alert('Error', 'Could not open website')
    );
  };

  const renderHospitalCard = (hospital) => (
    <TouchableOpacity 
      key={hospital.id}
      style={[
        styles.hospitalCard,
        selectedHospital?.id === hospital.id && styles.selectedCard
      ]}
      onPress={() => setSelectedHospital(
        selectedHospital?.id === hospital.id ? null : hospital
      )}
    >
      <View style={styles.hospitalHeader}>
        <View style={styles.hospitalInfo}>
          <Text style={styles.hospitalName}>{hospital.name}</Text>
          <View style={styles.ratingContainer}>
            <Ionicons name="star" size={16} color="#FFD700" />
            <Text style={styles.rating}>{hospital.rating}</Text>
            <Text style={styles.distance}>{hospital.distance} miles away</Text>
          </View>
        </View>
        <Ionicons 
          name={selectedHospital?.id === hospital.id ? "chevron-up" : "chevron-down"} 
          size={24} 
          color="#666" 
        />
      </View>

      <Text style={styles.hospitalAddress}>{hospital.address}</Text>
      
      <View style={styles.servicesContainer}>
        {hospital.services.slice(0, 3).map((service, index) => (
          <View key={index} style={styles.serviceTag}>
            <Text style={styles.serviceText}>{service}</Text>
          </View>
        ))}
        {hospital.services.length > 3 && (
          <View style={styles.moreTag}>
            <Text style={styles.moreText}>+{hospital.services.length - 3} more</Text>
          </View>
        )}
      </View>

      <Text style={styles.hours}>{hospital.hours}</Text>

      {selectedHospital?.id === hospital.id && (
        <View style={styles.actionButtons}>
          <TouchableOpacity 
            style={styles.actionButton}
            onPress={() => callHospital(hospital.phone)}
          >
            <Ionicons name="call" size={20} color="#FF69B4" />
            <Text style={styles.actionText}>Call</Text>
          </TouchableOpacity>
          
          <TouchableOpacity 
            style={styles.actionButton}
            onPress={() => openDirections(hospital)}
          >
            <Ionicons name="navigate" size={20} color="#FF69B4" />
            <Text style={styles.actionText}>Directions</Text>
          </TouchableOpacity>
          
          <TouchableOpacity 
            style={styles.actionButton}
            onPress={() => openWebsite(hospital.website)}
          >
            <Ionicons name="globe" size={20} color="#FF69B4" />
            <Text style={styles.actionText}>Website</Text>
          </TouchableOpacity>
        </View>
      )}
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#FF69B4" />
        <Text style={styles.loadingText}>Finding healthcare providers near you...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerContent}>
          <Text style={styles.title}>🏥 Find Screening</Text>
          <Text style={styles.subtitle}>
            {location ? 'Healthcare providers near you' : 'Enable location for nearby providers'}
          </Text>
        </View>
        <TouchableOpacity style={styles.refreshButton} onPress={onRefresh}>
          <Ionicons name="refresh" size={24} color="white" />
        </TouchableOpacity>
      </View>

      {/* Map View */}
      <View style={styles.mapContainer}>
        {location ? (
          <MapView
            style={styles.map}
            provider={PROVIDER_GOOGLE}
            initialRegion={{
              latitude: location.latitude,
              longitude: location.longitude,
              latitudeDelta: 0.0922,
              longitudeDelta: 0.0421,
            }}
            showsUserLocation={true}
          >
            {/* User Location */}
            <Marker
              coordinate={{
                latitude: location.latitude,
                longitude: location.longitude,
              }}
              title="Your Location"
              pinColor="#FF69B4"
            />
            
            {/* Hospital Markers */}
            {hospitals.map(hospital => (
              <Marker
                key={hospital.id}
                coordinate={{
                  latitude: hospital.latitude,
                  longitude: hospital.longitude,
                }}
                title={hospital.name}
                description={hospital.address}
                onPress={() => setSelectedHospital(hospital)}
              >
                <View style={[
                  styles.marker,
                  selectedHospital?.id === hospital.id && styles.selectedMarker
                ]}>
                  <Ionicons name="medical" size={20} color="white" />
                </View>
              </Marker>
            ))}
          </MapView>
        ) : (
          <View style={styles.mapPlaceholder}>
            <Ionicons name="location-off" size={50} color="#ccc" />
            <Text style={styles.mapPlaceholderText}>
              Enable location to see providers near you
            </Text>
            <TouchableOpacity 
              style={styles.enableLocationButton}
              onPress={getLocation}
            >
              <Text style={styles.enableLocationText}>Enable Location</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>

      {/* Hospital List */}
      <View style={styles.listContainer}>
        <View style={styles.listHeader}>
          <Text style={styles.listTitle}>
            {hospitals.length} Screening Centers Nearby
          </Text>
        </View>

        <ScrollView
          style={styles.hospitalList}
          showsVerticalScrollIndicator={false}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              colors={['#FF69B4']}
            />
          }
        >
          {hospitals.map(renderHospitalCard)}
          
          {/* Additional Resources */}
          <View style={styles.resourcesCard}>
            <Text style={styles.resourcesTitle}>📋 Need Help Scheduling?</Text>
            <Text style={styles.resourcesText}>
              Many centers offer financial assistance and same-day appointments. 
              Don't hesitate to call and ask about available support programs.
            </Text>
            
            <View style={styles.resourceButtons}>
              <TouchableOpacity style={styles.resourceButton}>
                <Ionicons name="document-text" size={16} color="#FF69B4" />
                <Text style={styles.resourceButtonText}>Questions to Ask</Text>
              </TouchableOpacity>
              
              <TouchableOpacity style={styles.resourceButton}>
                <Ionicons name="heart" size={16} color="#FF69B4" />
                <Text style={styles.resourceButtonText}>Insurance Help</Text>
              </TouchableOpacity>
            </View>
          </View>
        </ScrollView>
      </View>
    </View>
  );
};

// ... (keep the same styles from previous version)
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFF0F5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#FFF0F5',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FF69B4',
    padding: 20,
    paddingTop: 60,
  },
  headerContent: {
    flex: 1,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.9)',
  },
  refreshButton: {
    padding: 8,
  },
  mapContainer: {
    height: 250,
    backgroundColor: '#f0f0f0',
  },
  map: {
    flex: 1,
  },
  mapPlaceholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f8f9fa',
  },
  mapPlaceholderText: {
    marginTop: 12,
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginHorizontal: 20,
  },
  enableLocationButton: {
    marginTop: 16,
    backgroundColor: '#FF69B4',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 20,
  },
  enableLocationText: {
    color: 'white',
    fontWeight: '600',
  },
  marker: {
    backgroundColor: '#FF69B4',
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 3,
    borderColor: 'white',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 5,
  },
  selectedMarker: {
    backgroundColor: '#EC4899',
    transform: [{ scale: 1.2 }],
  },
  listContainer: {
    flex: 1,
    backgroundColor: 'white',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    marginTop: -20,
    overflow: 'hidden',
  },
  listHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    paddingBottom: 10,
  },
  listTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
  },
  hospitalList: {
    flex: 1,
  },
  hospitalCard: {
    backgroundColor: 'white',
    marginHorizontal: 16,
    marginVertical: 6,
    padding: 16,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#f0f0f0',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  selectedCard: {
    borderColor: '#FF69B4',
    borderWidth: 2,
    backgroundColor: '#FFF0F5',
  },
  hospitalHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  hospitalInfo: {
    flex: 1,
  },
  hospitalName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 4,
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  rating: {
    fontSize: 14,
    color: '#666',
    fontWeight: '600',
    marginRight: 8,
  },
  distance: {
    fontSize: 14,
    color: '#FF69B4',
    fontWeight: '600',
  },
  hospitalAddress: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
    lineHeight: 20,
  },
  servicesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 8,
    gap: 6,
  },
  serviceTag: {
    backgroundColor: '#FFF0F5',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  serviceText: {
    fontSize: 12,
    color: '#FF69B4',
    fontWeight: '500',
  },
  moreTag: {
    backgroundColor: '#f8f9fa',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  moreText: {
    fontSize: 12,
    color: '#666',
    fontWeight: '500',
  },
  hours: {
    fontSize: 12,
    color: '#666',
    fontStyle: 'italic',
  },
  actionButtons: {
    flexDirection: 'row',
    marginTop: 12,
    gap: 8,
  },
  actionButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'white',
    padding: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#FF69B4',
    gap: 6,
  },
  actionText: {
    color: '#FF69B4',
    fontSize: 14,
    fontWeight: '600',
  },
  resourcesCard: {
    backgroundColor: '#FFF0F5',
    margin: 16,
    marginTop: 8,
    padding: 20,
    borderRadius: 16,
    borderWidth: 2,
    borderColor: '#FF69B4',
    borderStyle: 'dashed',
  },
  resourcesTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FF69B4',
    marginBottom: 8,
  },
  resourcesText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
    marginBottom: 16,
  },
  resourceButtons: {
    flexDirection: 'row',
    gap: 12,
  },
  resourceButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'white',
    padding: 12,
    borderRadius: 10,
    gap: 6,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  resourceButtonText: {
    color: '#FF69B4',
    fontSize: 14,
    fontWeight: '600',
  },
});

export default HospitalsScreen;