import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  Alert,
  TouchableOpacity
} from 'react-native';
import { getHospitals } from '../services/api';
import { API_CONFIG } from '../services/apiConstants';

export default function HospitalsScreen() {
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHospitals();
  }, []);

  const loadHospitals = async () => {
    try {
      setLoading(true);
      const data = await getHospitals();
      setHospitals(Array.isArray(data) ? data : []);
    } catch (error) {
      Alert.alert('Error', 'Failed to load hospitals data');
      setHospitals([]);
    } finally {
      setLoading(false);
    }
  };

  const renderHospitalItem = ({ item, index }) => (
    <TouchableOpacity style={styles.hospitalCard}>
      <View style={styles.hospitalHeader}>
        <Text style={styles.hospitalName}>{item.name || `Hospital ${index + 1}`}</Text>
        <Text style={styles.distance}>{item.distance || '5km'}</Text>
      </View>
      
      <Text style={styles.hospitalAddress}>
        {item.address || '123 Medical Center Drive'}
      </Text>
      
      <Text style={styles.hospitalPhone}>
        {item.phone || '+1 (555) 123-4567'}
      </Text>
      
      <View style={styles.servicesContainer}>
        <Text style={styles.servicesLabel}>Services:</Text>
        <Text style={styles.servicesText}>
          {item.services || 'Mammography, Screening, Consultation'}
        </Text>
      </View>
      
      <View style={styles.hoursContainer}>
        <Text style={styles.hoursText}>
          Hours: {item.hours || 'Mon-Fri: 8AM-6PM'}
        </Text>
      </View>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color={API_CONFIG.COLORS.PRIMARY} />
        <Text style={styles.loadingText}>Loading hospitals...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>🏥 Nearby Screening Facilities</Text>
        <Text style={styles.subtitle}>
          Find breast cancer screening centers near you
        </Text>
      </View>

      <FlatList
        data={hospitals.length > 0 ? hospitals : defaultHospitals}
        renderItem={renderHospitalItem}
        keyExtractor={(item, index) => index.toString()}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.listContent}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>No hospitals data available</Text>
          </View>
        }
      />
    </View>
  );
}

// Default data in case API returns empty
const defaultHospitals = [
  {
    name: 'City General Hospital',
    address: '123 Medical Center Drive',
    phone: '+1 (555) 123-4567',
    services: 'Mammography, Ultrasound, Biopsy',
    hours: 'Mon-Fri: 8AM-6PM, Sat: 9AM-1PM'
  },
  {
    name: 'Women Health Center',
    address: '456 Health Avenue',
    phone: '+1 (555) 234-5678',
    services: 'Breast Screening, Consultation, Support',
    hours: 'Mon-Fri: 7AM-7PM'
  },
  {
    name: 'Community Medical Center',
    address: '789 Care Boulevard',
    phone: '+1 (555) 345-6789',
    services: 'Mammography, Early Detection, Education',
    hours: 'Mon-Sun: 24/7 Emergency'
  }
];

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: API_CONFIG.COLORS.BACKGROUND,
  },
  header: {
    padding: 20,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: API_CONFIG.COLORS.BACKGROUND,
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  listContent: {
    padding: 16,
  },
  hospitalCard: {
    backgroundColor: '#FFFFFF',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    borderLeftWidth: 4,
    borderLeftColor: API_CONFIG.COLORS.PRIMARY,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
  },
  hospitalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  hospitalName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
  },
  distance: {
    fontSize: 14,
    color: API_CONFIG.COLORS.PRIMARY,
    fontWeight: 'bold',
  },
  hospitalAddress: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  },
  hospitalPhone: {
    fontSize: 14,
    color: '#333',
    marginBottom: 8,
    fontWeight: '500',
  },
  servicesContainer: {
    marginBottom: 8,
  },
  servicesLabel: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 2,
  },
  servicesText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 18,
  },
  hoursContainer: {
    paddingTop: 8,
    borderTopWidth: 1,
    borderTopColor: '#F0F0F0',
  },
  hoursText: {
    fontSize: 12,
    color: '#888',
    fontStyle: 'italic',
  },
  emptyContainer: {
    alignItems: 'center',
    padding: 40,
  },
  emptyText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
});