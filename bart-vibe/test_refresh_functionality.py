#!/usr/bin/env python3
"""
Simple unit tests for refresh button functionality without requiring browser automation
"""

import pytest
import tempfile
import os
import json
import threading
import time
import socketserver
from unittest.mock import patch, Mock
from pathlib import Path
import requests

# Import the server module
from server import TransitHTTPRequestHandler


class TestRefreshButtonSimple:
    """Test refresh button functionality using HTTP requests instead of browser automation"""
    
    def setup_method(self):
        """Set up test environment for each test"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test data files
        self.create_test_data_files()
        
        # Start test server
        self.start_test_server()
    
    def teardown_method(self):
        """Clean up test environment"""
        if hasattr(self, 'server'):
            self.server.shutdown()
            self.server.server_close()
        
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.test_dir)
    
    def create_test_data_files(self):
        """Create test transit data files"""
        # Create initial data file
        initial_data = {
            "timestamp": "2025-09-09T12:00:00.000000",
            "total_vehicles": 2,
            "bart_count": 1,
            "caltrain_count": 1,
            "locations": [
                {
                    "system": "BART",
                    "vehicle_id": "1234",
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "station": "Embarcadero",
                    "delay_seconds": 0,
                    "gps_source": "estimated_from_station"
                },
                {
                    "system": "Caltrain",
                    "vehicle_id": "5678",
                    "latitude": 37.5052,
                    "longitude": -122.2751,
                    "speed_mps": 20.0,
                    "bearing": 180.0,
                    "gps_source": "gps"
                }
            ]
        }
        
        # Create updated data file (simulates new data after refresh)
        updated_data = {
            "timestamp": "2025-09-09T12:30:00.000000",
            "total_vehicles": 3,
            "bart_count": 2,
            "caltrain_count": 1,
            "locations": [
                {
                    "system": "BART",
                    "vehicle_id": "1234",
                    "latitude": 37.7849,  # Moved position
                    "longitude": -122.4094,
                    "station": "Montgomery",
                    "delay_seconds": 120,
                    "gps_source": "estimated_from_station"
                },
                {
                    "system": "BART",
                    "vehicle_id": "9999",  # New train
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "station": "Embarcadero",
                    "delay_seconds": 0,
                    "gps_source": "estimated_from_station"
                },
                {
                    "system": "Caltrain",
                    "vehicle_id": "5678",
                    "latitude": 37.5152,  # Moved position
                    "longitude": -122.2651,
                    "speed_mps": 25.0,
                    "bearing": 180.0,
                    "gps_source": "gps"
                }
            ]
        }
        
        # Save initial data file
        with open('transit_locations_20250909_120000.json', 'w') as f:
            json.dump(initial_data, f)
        
        # Save updated data file (for refresh test)
        with open('transit_locations_20250909_123000.json', 'w') as f:
            json.dump(updated_data, f)
        
        # Create a simple HTML file that the refresh button would be in
        self.create_test_html()
    
    def create_test_html(self):
        """Create a minimal HTML file for testing"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Transit Map Test</title></head>
        <body>
            <button id="refresh-btn" onclick="loadTransitData()">🔄 Refresh Data</button>
            <div id="bart-count">0</div>
            <div id="caltrain-count">0</div>
            <div id="total-count">0</div>
        </body>
        </html>
        """
        
        with open('map.html', 'w') as f:
            f.write(html_content)
    
    def start_test_server(self):
        """Start the test HTTP server"""
        # Try different ports to avoid conflicts, using a wider range
        import random
        base_port = random.randint(8005, 8050)
        
        for port in range(base_port, base_port + 20):
            try:
                self.port = port
                self.server = socketserver.TCPServer(("", port), TransitHTTPRequestHandler)
                break
            except OSError:
                continue
        else:
            raise Exception("Could not find available port")
        
        def run_server():
            self.server.serve_forever()
        
        self.server_thread = threading.Thread(target=run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        # Give server time to start
        time.sleep(0.5)
    
    def test_map_html_served(self):
        """Test that the map.html file is served correctly"""
        response = requests.get(f'http://localhost:{self.port}/map.html', timeout=5)
        assert response.status_code == 200
        assert 'Refresh Data' in response.text
        assert 'refresh-btn' in response.text
    
    def test_initial_data_file_served(self):
        """Test that initial transit data file is served correctly"""
        response = requests.get(f'http://localhost:{self.port}/transit_locations_20250909_120000.json', timeout=5)
        assert response.status_code == 200
        
        data = response.json()
        assert data['total_vehicles'] == 2
        assert data['bart_count'] == 1
        assert data['caltrain_count'] == 1
        assert len(data['locations']) == 2
    
    def test_updated_data_file_served(self):
        """Test that updated transit data file is served correctly (simulates refresh)"""
        response = requests.get(f'http://localhost:{self.port}/transit_locations_20250909_123000.json', timeout=5)
        assert response.status_code == 200
        
        data = response.json()
        assert data['total_vehicles'] == 3  # Updated count
        assert data['bart_count'] == 2      # Updated count
        assert data['caltrain_count'] == 1
        assert len(data['locations']) == 3  # More vehicles
    
    def test_directory_listing_shows_data_files(self):
        """Test that directory listing contains transit data files (for refresh file discovery)"""
        response = requests.get(f'http://localhost:{self.port}/', timeout=5)
        assert response.status_code == 200
        
        # Check that both data files are listed
        assert 'transit_locations_20250909_120000.json' in response.text
        assert 'transit_locations_20250909_123000.json' in response.text
    
    def test_cors_headers_on_data_files(self):
        """Test that CORS headers are present on data files (required for refresh button AJAX)"""
        response = requests.get(f'http://localhost:{self.port}/transit_locations_20250909_120000.json', timeout=5)
        
        assert response.headers.get('Access-Control-Allow-Origin') == '*'
        assert 'Access-Control-Allow-Methods' in response.headers
    
    def test_refresh_button_file_discovery_simulation(self):
        """Test the logic that the refresh button uses to find the latest file"""
        # Get directory listing
        response = requests.get(f'http://localhost:{self.port}/', timeout=5)
        html_content = response.text
        
        # Simulate the JavaScript file discovery logic
        import re
        file_matches = re.findall(r'transit_locations_\d{8}_\d{6}\.json', html_content)
        
        assert len(file_matches) >= 2  # Should find both files
        
        # Get the most recent file (files are named with timestamps)
        latest_file = sorted(file_matches)[-1]
        assert latest_file == 'transit_locations_20250909_123000.json'  # Should be the newer one
    
    def test_refresh_button_data_update_simulation(self):
        """Test that refresh button logic would get updated data"""
        # First request - simulate initial load
        initial_response = requests.get(f'http://localhost:{self.port}/transit_locations_20250909_120000.json', timeout=5)
        initial_data = initial_response.json()
        
        # Second request - simulate refresh button click with newer file
        refresh_response = requests.get(f'http://localhost:{self.port}/transit_locations_20250909_123000.json', timeout=5)
        refresh_data = refresh_response.json()
        
        # Verify the data changed (what refresh button would detect)
        assert initial_data['total_vehicles'] != refresh_data['total_vehicles']
        assert initial_data['bart_count'] != refresh_data['bart_count']
        assert len(initial_data['locations']) != len(refresh_data['locations'])
        
        # Verify specific changes
        assert initial_data['total_vehicles'] == 2
        assert refresh_data['total_vehicles'] == 3
        assert initial_data['bart_count'] == 1
        assert refresh_data['bart_count'] == 2


class TestRefreshButtonLogic:
    """Test the logical components that the refresh button depends on"""
    
    def test_file_timestamp_sorting(self):
        """Test that transit files sort correctly by timestamp"""
        files = [
            'transit_locations_20250909_120000.json',
            'transit_locations_20250909_123000.json', 
            'transit_locations_20250909_115900.json',
            'transit_locations_20250909_124500.json'
        ]
        
        sorted_files = sorted(files)
        assert sorted_files[-1] == 'transit_locations_20250909_124500.json'  # Latest
        assert sorted_files[0] == 'transit_locations_20250909_115900.json'   # Earliest
    
    def test_transit_data_structure(self):
        """Test that transit data has the structure the refresh button expects"""
        test_data = {
            "timestamp": "2025-09-09T12:00:00.000000",
            "total_vehicles": 5,
            "bart_count": 3,
            "caltrain_count": 2,
            "locations": [
                {
                    "system": "BART",
                    "vehicle_id": "1234",
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "station": "Embarcadero",
                    "delay_seconds": 0,
                    "gps_source": "estimated_from_station"
                }
            ]
        }
        
        # Verify all required fields exist for refresh button
        assert 'timestamp' in test_data
        assert 'total_vehicles' in test_data
        assert 'bart_count' in test_data
        assert 'caltrain_count' in test_data
        assert 'locations' in test_data
        assert isinstance(test_data['locations'], list)
        
        # Verify location structure
        location = test_data['locations'][0]
        assert 'system' in location
        assert 'vehicle_id' in location
        assert 'latitude' in location
        assert 'longitude' in location


if __name__ == '__main__':
    pytest.main([__file__, "-v"])
