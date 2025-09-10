#!/usr/bin/env python3
"""
Unit tests for the Location Tracker module
"""

import pytest
import json
import os
import tempfile
import requests
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import requests_mock

# Import the module under test
from location_tracker import LocationTracker


class TestLocationTracker:
    """Test the LocationTracker class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key_123"
        self.tracker = LocationTracker(caltrain_api_key=self.api_key)
    
    def test_init(self):
        """Test LocationTracker initialization"""
        assert self.tracker.caltrain_api_key == self.api_key
        assert "bart.gov" in self.tracker.bart_trip_updates_url
        assert "511.org" in self.tracker.caltrain_vehicle_url
        assert len(self.tracker.bart_station_coords) > 0
    
    def test_init_without_api_key(self):
        """Test initialization without API key"""
        tracker = LocationTracker()
        assert tracker.caltrain_api_key is None
    
    def test_bart_station_coordinates_exist(self):
        """Test that BART station coordinates are properly loaded"""
        coords = self.tracker.bart_station_coords
        
        # Check some key stations exist
        assert 'S10' in coords  # Embarcadero
        assert 'A10' in coords  # Pittsburg/Bay Point
        assert 'A05' in coords  # Antioch
        
        # Check coordinate structure
        for station_code, data in coords.items():
            assert 'lat' in data
            assert 'lon' in data
            assert 'name' in data
            assert isinstance(data['lat'], (int, float))
            assert isinstance(data['lon'], (int, float))
            assert isinstance(data['name'], str)
    
    @requests_mock.Mocker()
    def test_fetch_bart_locations_success(self, m):
        """Test successful BART data fetching"""
        # Mock GTFS-RT protobuf data
        mock_response = b'\x08\x01\x12\x1a\n\x04test\x12\x12\x08\x00\x12\x0e\n\x04A10-1\x1a\x06\x08\xc0\x84\x03'
        
        m.get(self.tracker.bart_trip_updates_url, content=mock_response)
        
        # Mock the protobuf parsing
        with patch('location_tracker.gtfs_realtime_pb2.FeedMessage') as mock_feed:
            mock_entity = Mock()
            mock_entity.id = "test_trip"
            mock_entity.HasField.return_value = True
            mock_entity.trip_update.stop_time_update = [Mock()]
            mock_entity.trip_update.stop_time_update[0].stop_id = "A10-1"
            mock_entity.trip_update.stop_time_update[0].departure.delay = 300
            mock_entity.trip_update.vehicle.id = "1234"
            
            mock_feed_instance = Mock()
            mock_feed_instance.entity = [mock_entity]
            mock_feed.return_value = mock_feed_instance
            
            locations = self.tracker.fetch_bart_locations()
            
            assert len(locations) == 1
            assert locations[0]['vehicle_id'] == "1234"
            assert locations[0]['station'] == "Pittsburg/Bay Point"
            assert locations[0]['delay_seconds'] == 300
    
    @requests_mock.Mocker()
    def test_fetch_bart_locations_network_error(self, m):
        """Test BART data fetching with network error"""
        m.get(self.tracker.bart_trip_updates_url, exc=requests.exceptions.RequestException)
        
        locations = self.tracker.fetch_bart_locations()
        assert locations == []
    
    @requests_mock.Mocker()
    def test_fetch_caltrain_locations_success(self, m):
        """Test successful Caltrain data fetching"""
        mock_response = b'\x08\x01\x12\x1a\n\x04test\x12\x12\x08\x00\x12\x0e\n\x041234\x1a\x06\x08\xc0\x84\x03'
        
        m.get(self.tracker.caltrain_vehicle_url, content=mock_response)
        
        # Mock the protobuf parsing
        with patch('location_tracker.gtfs_realtime_pb2.FeedMessage') as mock_feed:
            mock_entity = Mock()
            mock_entity.id = "test_vehicle"
            mock_entity.HasField.return_value = True
            mock_entity.vehicle.vehicle.id = "1234"
            mock_entity.vehicle.position.latitude = 37.7749
            mock_entity.vehicle.position.longitude = -122.4194
            mock_entity.vehicle.position.speed = 15.0
            mock_entity.vehicle.position.bearing = 90.0
            
            mock_feed_instance = Mock()
            mock_feed_instance.entity = [mock_entity]
            mock_feed.return_value = mock_feed_instance
            
            locations = self.tracker.fetch_caltrain_locations()
            
            assert len(locations) == 1
            assert locations[0]['vehicle_id'] == "1234"
            assert locations[0]['latitude'] == 37.7749
            assert locations[0]['longitude'] == -122.4194
            assert locations[0]['speed_mps'] == 15.0
            assert locations[0]['bearing'] == 90.0
    
    @requests_mock.Mocker()
    def test_fetch_caltrain_locations_no_api_key(self, m):
        """Test Caltrain data fetching without API key"""
        tracker = LocationTracker()  # No API key
        locations = tracker.fetch_caltrain_locations()
        assert locations == []
    
    def test_save_location_data(self):
        """Test saving location data to JSON file"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            os.chdir(tmp_dir)
            
            test_data = {
                'timestamp': '2025-09-09T12:00:00',
                'total_vehicles': 2,
                'bart_count': 1,
                'caltrain_count': 1,
                'locations': [
                    {
                        'system': 'BART',
                        'vehicle_id': '1234',
                        'latitude': 37.7749,
                        'longitude': -122.4194,
                        'station': 'Embarcadero',
                        'delay_seconds': 0,
                        'gps_source': 'estimated_from_station'
                    },
                    {
                        'system': 'Caltrain',
                        'vehicle_id': '5678',
                        'latitude': 37.5052,
                        'longitude': -122.2751,
                        'speed_mps': 20.0,
                        'bearing': 180.0,
                        'gps_source': 'gps'
                    }
                ]
            }
            
            filename = self.tracker.save_location_data(test_data)
            
            # Check file was created
            assert os.path.exists(filename)
            assert filename.startswith('transit_locations_')
            assert filename.endswith('.json')
            
            # Check file contents
            with open(filename, 'r') as f:
                saved_data = json.load(f)
            
            assert saved_data == test_data
    
    @patch('location_tracker.LocationTracker.fetch_bart_locations')
    @patch('location_tracker.LocationTracker.fetch_caltrain_locations')
    def test_collect_all_locations(self, mock_caltrain, mock_bart):
        """Test collecting data from both BART and Caltrain"""
        mock_bart.return_value = [
            {
                'system': 'BART',
                'vehicle_id': '1234',
                'latitude': 37.7749,
                'longitude': -122.4194,
                'station': 'Embarcadero',
                'delay_seconds': 0,
                'gps_source': 'estimated_from_station'
            }
        ]
        
        mock_caltrain.return_value = [
            {
                'system': 'Caltrain',
                'vehicle_id': '5678',
                'latitude': 37.5052,
                'longitude': -122.2751,
                'speed_mps': 20.0,
                'bearing': 180.0,
                'gps_source': 'gps'
            }
        ]
        
        data = self.tracker.collect_all_locations()
        
        assert data['total_vehicles'] == 2
        assert data['bart_count'] == 1
        assert data['caltrain_count'] == 1
        assert len(data['locations']) == 2
        assert 'timestamp' in data
    
    def test_unknown_station_handling(self):
        """Test handling of unknown BART station codes"""
        # Mock a trip update with unknown station
        with patch('location_tracker.gtfs_realtime_pb2.FeedMessage') as mock_feed:
            mock_entity = Mock()
            mock_entity.id = "test_trip"
            mock_entity.HasField.return_value = True
            mock_entity.trip_update.stop_time_update = [Mock()]
            mock_entity.trip_update.stop_time_update[0].stop_id = "UNKNOWN-1"
            mock_entity.trip_update.stop_time_update[0].departure.delay = 0
            mock_entity.trip_update.vehicle.id = "1234"
            
            mock_feed_instance = Mock()
            mock_feed_instance.entity = [mock_entity]
            mock_feed.return_value = mock_feed_instance
            
            with patch('requests.get') as mock_get:
                mock_get.return_value.content = b'mock_data'
                
                # Capture print output to check unknown station logging
                with patch('builtins.print') as mock_print:
                    locations = self.tracker.fetch_bart_locations()
                    
                    # Should print unknown station warning
                    mock_print.assert_called()
                    print_calls = [str(call) for call in mock_print.call_args_list]
                    unknown_call = any("Unknown station code: UNKNOWN" in call for call in print_calls)
                    assert unknown_call


class TestDataValidation:
    """Test data validation and structure"""
    
    def test_station_coordinates_format(self):
        """Test that all station coordinates are in valid ranges"""
        tracker = LocationTracker()
        
        for station_code, coords in tracker.bart_station_coords.items():
            # Bay Area latitude range (approximately)
            assert 37.0 <= coords['lat'] <= 38.5, f"Invalid latitude for {station_code}"
            # Bay Area longitude range (approximately)
            assert -123.0 <= coords['lon'] <= -121.0, f"Invalid longitude for {station_code}"
            assert len(coords['name']) > 0, f"Empty name for {station_code}"
    
    def test_antioch_stations_included(self):
        """Test that Antioch line stations are included"""
        tracker = LocationTracker()
        coords = tracker.bart_station_coords
        
        # Check for key Antioch line stations
        assert 'A05' in coords or 'ANTC' in coords  # Antioch
        assert coords.get('A05', coords.get('ANTC', {})).get('name') == 'Antioch'


if __name__ == '__main__':
    pytest.main([__file__])
