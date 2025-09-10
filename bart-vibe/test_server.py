#!/usr/bin/env python3
"""
Unit tests for the server module
"""

import pytest
import tempfile
import os
import json
import threading
import time
import requests
from unittest.mock import patch, Mock
from pathlib import Path

# Import the module under test
from server import TransitHTTPRequestHandler, start_server


class TestTransitHTTPRequestHandler:
    """Test the custom HTTP request handler"""
    
    def test_cors_headers(self):
        """Test that CORS headers are added correctly"""
        # Create a more complete mock handler
        handler = Mock(spec=TransitHTTPRequestHandler)
        handler.send_header = Mock()
        handler.request_version = 'HTTP/1.1'  # Add required attribute
        handler.wfile = Mock()  # Add wfile attribute
        
        # Mock the parent class method
        with patch('http.server.SimpleHTTPRequestHandler.end_headers'):
            # Call the real end_headers method
            TransitHTTPRequestHandler.end_headers(handler)
            
            # Check that CORS headers were sent
            expected_calls = [
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'Content-Type')
            ]
            
            for header, value in expected_calls:
                handler.send_header.assert_any_call(header, value)


class TestServerFunctions:
    """Test server utility functions"""
    
    def test_start_server_with_mock(self):
        """Test server startup with mocked components"""
        with patch('server.socketserver.TCPServer') as mock_server:
            with patch('server.webbrowser.open') as mock_browser:
                with patch('server.Path.glob') as mock_glob:
                    with patch('builtins.print') as mock_print:
                        # Mock data files
                        mock_glob.return_value = [
                            Path('transit_locations_20250909_120000.json'),
                            Path('transit_locations_20250909_130000.json')
                        ]
                        
                        # Mock server context manager
                        mock_server_instance = Mock()
                        mock_server.return_value.__enter__.return_value = mock_server_instance
                        mock_server_instance.serve_forever.side_effect = KeyboardInterrupt()
                        
                        # Run the server function
                        start_server()
                        
                        # Verify server was created with correct parameters
                        mock_server.assert_called_once_with(("", 8000), TransitHTTPRequestHandler)
                        
                        # Verify browser was opened
                        mock_browser.assert_called_once_with('http://localhost:8000/map.html')
                        
                        # Verify print statements
                        mock_print.assert_called()


class TestServerIntegration:
    """Integration tests for the server"""
    
    def setup_method(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test data files
        self.create_test_data_files()
    
    def teardown_method(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.test_dir)
    
    def create_test_data_files(self):
        """Create test transit data files"""
        test_data = {
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
        
        # Create multiple data files to test file discovery
        filenames = [
            'transit_locations_20250909_120000.json',
            'transit_locations_20250909_130000.json',
            'transit_locations_20250909_140000.json'
        ]
        
        for filename in filenames:
            with open(filename, 'w') as f:
                json.dump(test_data, f)
        
        # Create the map.html file
        self.create_test_map_html()
    
    def create_test_map_html(self):
        """Create a test map.html file"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Map</title></head>
        <body>
            <div id="map"></div>
            <button id="refresh-btn" onclick="loadTransitData()">Refresh</button>
            <div id="test-output"></div>
            <script>
                // Mock loadTransitData function for testing
                function loadTransitData() {
                    document.getElementById('test-output').textContent = 'Refresh clicked';
                    return fetch('./transit_locations_20250909_140000.json')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('test-output').textContent = 
                                'Loaded ' + data.total_vehicles + ' vehicles';
                            return data;
                        });
                }
            </script>
        </body>
        </html>
        """
        
        with open('map.html', 'w') as f:
            f.write(html_content)
    
    @patch('server.webbrowser.open')
    def test_server_serves_files(self, mock_browser):
        """Test that server serves files correctly"""
        import http.server
        import socketserver
        import threading
        import time
        
        # Start server in a separate thread
        server_thread = None
        
        try:
            # Create server
            handler = TransitHTTPRequestHandler
            server = socketserver.TCPServer(("", 8001), handler)  # Use different port
            
            def run_server():
                server.serve_forever()
            
            server_thread = threading.Thread(target=run_server)
            server_thread.daemon = True
            server_thread.start()
            
            # Give server time to start
            time.sleep(0.5)
            
            # Test serving map.html
            response = requests.get('http://localhost:8001/map.html', timeout=5)
            assert response.status_code == 200
            assert 'Test Map' in response.text
            
            # Test serving JSON data file
            response = requests.get('http://localhost:8001/transit_locations_20250909_140000.json', timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data['total_vehicles'] == 2
            assert len(data['locations']) == 2
            
            # Test CORS headers
            assert response.headers.get('Access-Control-Allow-Origin') == '*'
            
        finally:
            if server_thread:
                server.shutdown()
                server.server_close()


if __name__ == '__main__':
    pytest.main([__file__])
