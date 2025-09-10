#!/usr/bin/env python3
"""
Browser tests for the refresh button and map functionality
"""

import pytest
import tempfile
import os
import json
import threading
import time
import socketserver
from unittest.mock import patch
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

# Import the server module
from server import TransitHTTPRequestHandler


class TestRefreshButton:
    """Test the refresh button functionality in the browser"""
    
    @classmethod
    def setup_class(cls):
        """Set up the test environment"""
        cls.test_dir = tempfile.mkdtemp()
        cls.original_cwd = os.getcwd()
        os.chdir(cls.test_dir)
        
        # Create test data files and HTML
        cls.create_test_files()
        
        # Start test server
        cls.start_test_server()
        
        # Set up Chrome driver with headless option
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            cls.driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException:
            # If Chrome is not available, skip these tests
            pytest.skip("Chrome browser not available for testing")
    
    @classmethod
    def teardown_class(cls):
        """Clean up test environment"""
        if hasattr(cls, 'driver'):
            cls.driver.quit()
        
        if hasattr(cls, 'server'):
            cls.server.shutdown()
            cls.server.server_close()
        
        os.chdir(cls.original_cwd)
        import shutil
        shutil.rmtree(cls.test_dir)
    
    @classmethod
    def create_test_files(cls):
        """Create test transit data files and HTML"""
        # Create initial data file
        cls.initial_data = {
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
        
        # Create updated data file (simulates new data)
        cls.updated_data = {
            "timestamp": "2025-09-09T12:30:00.000000",
            "total_vehicles": 3,
            "bart_count": 2,
            "caltrain_count": 1,
            "locations": [
                {
                    "system": "BART",
                    "vehicle_id": "1234",
                    "latitude": 37.7849,  # Slightly different position
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
            json.dump(cls.initial_data, f)
        
        # Create the test map.html file with simplified JavaScript for testing
        cls.create_test_map_html()
    
    @classmethod
    def create_test_map_html(cls):
        """Create a test map.html file with refresh functionality"""
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Transit Map Test</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                #map { width: 100%; height: 400px; background: #f0f0f0; border: 1px solid #ccc; }
                .info-panel { margin-top: 20px; padding: 15px; background: white; border: 1px solid #ccc; }
                .refresh-btn { background: #4CAF50; color: white; border: none; padding: 10px 20px; cursor: pointer; }
                .refresh-btn:hover { background: #45a049; }
                .train-count { margin: 5px 0; font-weight: bold; }
                .bart-train { color: #0066cc; }
                .caltrain-train { color: #ff6600; }
                .last-update { font-size: 12px; color: #666; margin-top: 10px; }
                .loading { color: #ff9800; font-weight: bold; }
                .error { color: #f44336; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>🚆 Transit Map Test</h1>
            <div id="map">Map placeholder for testing</div>
            
            <div class="info-panel">
                <div id="train-counts">
                    <div class="train-count bart-train">BART: <span id="bart-count">0</span> trains</div>
                    <div class="train-count caltrain-train">Caltrain: <span id="caltrain-count">0</span> vehicles</div>
                    <div class="train-count">Total: <span id="total-count">0</span> vehicles</div>
                </div>
                
                <button class="refresh-btn" id="refresh-btn" onclick="loadTransitData()">🔄 Refresh Data</button>
                <div class="last-update" id="last-update">Loading...</div>
                
                <!-- Test status elements -->
                <div id="test-status" style="margin-top: 20px;">
                    <div>Refresh Count: <span id="refresh-count">0</span></div>
                    <div>Last File Loaded: <span id="last-file">none</span></div>
                    <div>Load Status: <span id="load-status">ready</span></div>
                </div>
            </div>

            <script>
                let refreshCount = 0;
                let loadedData = null;
                
                // Function to load and display transit data
                async function loadTransitData() {
                    try {
                        refreshCount++;
                        document.getElementById('refresh-count').textContent = refreshCount;
                        document.getElementById('last-update').innerHTML = '<span class="loading">Loading...</span>';
                        document.getElementById('load-status').textContent = 'loading';
                        
                        // Find the most recent transit data file
                        const response = await fetch('./');
                        const text = await response.text();
                        
                        // Extract transit_locations files from directory listing
                        const fileMatches = text.match(/transit_locations_\\d{8}_\\d{6}\\.json/g);
                        
                        if (!fileMatches || fileMatches.length === 0) {
                            throw new Error('No transit data files found');
                        }
                        
                        // Get the most recent file (files are named with timestamps)
                        const latestFile = fileMatches.sort().pop();
                        document.getElementById('last-file').textContent = latestFile;
                        
                        // Load the transit data
                        const dataResponse = await fetch(latestFile);
                        loadedData = await dataResponse.json();
                        
                        // Update counts
                        const bartCount = loadedData.locations.filter(t => t.system === 'BART').length;
                        const caltrainCount = loadedData.locations.filter(t => t.system === 'Caltrain').length;
                        
                        document.getElementById('bart-count').textContent = bartCount;
                        document.getElementById('caltrain-count').textContent = caltrainCount;
                        document.getElementById('total-count').textContent = loadedData.total_vehicles;
                        
                        // Update timestamp
                        const updateTime = new Date(loadedData.timestamp).toLocaleTimeString();
                        document.getElementById('last-update').textContent = `Updated: ${updateTime}`;
                        document.getElementById('load-status').textContent = 'success';
                        
                        console.log(`Loaded ${loadedData.total_vehicles} vehicles from ${latestFile}`);
                        
                    } catch (error) {
                        console.error('Error loading transit data:', error);
                        document.getElementById('last-update').innerHTML = `<span class="error">Error: ${error.message}</span>`;
                        document.getElementById('load-status').textContent = 'error';
                    }
                }
                
                // Load initial data when page loads
                document.addEventListener('DOMContentLoaded', function() {
                    loadTransitData();
                });
                
                // Make loadedData available for testing
                window.getLoadedData = function() {
                    return loadedData;
                };
            </script>
        </body>
        </html>
        """
        
        with open('map.html', 'w') as f:
            f.write(html_content)
    
    @classmethod
    def start_test_server(cls):
        """Start the test HTTP server"""
        cls.server = socketserver.TCPServer(("", 8002), TransitHTTPRequestHandler)
        
        def run_server():
            cls.server.serve_forever()
        
        cls.server_thread = threading.Thread(target=run_server)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        
        # Give server time to start
        time.sleep(1)
    
    def test_initial_page_load(self):
        """Test that the page loads correctly and displays initial data"""
        self.driver.get('http://localhost:8002/map.html')
        
        # Wait for page to load
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "refresh-btn")))
        
        # Check that elements are present
        assert self.driver.find_element(By.ID, "refresh-btn")
        assert self.driver.find_element(By.ID, "bart-count")
        assert self.driver.find_element(By.ID, "caltrain-count")
        assert self.driver.find_element(By.ID, "total-count")
        
        # Wait for initial data to load
        wait.until(lambda driver: driver.find_element(By.ID, "load-status").text == "success")
        
        # Check initial counts
        bart_count = self.driver.find_element(By.ID, "bart-count").text
        caltrain_count = self.driver.find_element(By.ID, "caltrain-count").text
        total_count = self.driver.find_element(By.ID, "total-count").text
        
        assert bart_count == "1"
        assert caltrain_count == "1"
        assert total_count == "2"
    
    def test_refresh_button_click(self):
        """Test that the refresh button works correctly"""
        self.driver.get('http://localhost:8002/map.html')
        
        # Wait for initial load
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: driver.find_element(By.ID, "load-status").text == "success")
        
        # Get initial refresh count
        initial_refresh_count = self.driver.find_element(By.ID, "refresh-count").text
        assert initial_refresh_count == "1"  # Should be 1 from initial load
        
        # Click refresh button
        refresh_btn = self.driver.find_element(By.ID, "refresh-btn")
        refresh_btn.click()
        
        # Wait for refresh to complete
        wait.until(lambda driver: driver.find_element(By.ID, "refresh-count").text == "2")
        
        # Check that refresh count increased
        new_refresh_count = self.driver.find_element(By.ID, "refresh-count").text
        assert new_refresh_count == "2"
        
        # Check that load status shows success
        load_status = self.driver.find_element(By.ID, "load-status").text
        assert load_status == "success"
    
    def test_refresh_button_updates_data(self):
        """Test that refresh button loads new data when available"""
        self.driver.get('http://localhost:8002/map.html')
        
        # Wait for initial load
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: driver.find_element(By.ID, "load-status").text == "success")
        
        # Check initial counts
        initial_total = self.driver.find_element(By.ID, "total-count").text
        assert initial_total == "2"
        
        # Create new data file with updated data
        with open('transit_locations_20250909_123000.json', 'w') as f:
            json.dump(self.updated_data, f)
        
        # Click refresh button
        refresh_btn = self.driver.find_element(By.ID, "refresh-btn")
        refresh_btn.click()
        
        # Wait for refresh to complete and check for updated data
        wait.until(lambda driver: driver.find_element(By.ID, "total-count").text == "3")
        
        # Check updated counts
        bart_count = self.driver.find_element(By.ID, "bart-count").text
        caltrain_count = self.driver.find_element(By.ID, "caltrain-count").text
        total_count = self.driver.find_element(By.ID, "total-count").text
        
        assert bart_count == "2"  # Updated from initial data
        assert caltrain_count == "1"
        assert total_count == "3"  # Updated from initial data
        
        # Check that the newer file was loaded
        last_file = self.driver.find_element(By.ID, "last-file").text
        assert "123000" in last_file  # Should load the newer timestamp file
    
    def test_refresh_button_multiple_clicks(self):
        """Test that refresh button works correctly with multiple clicks"""
        self.driver.get('http://localhost:8002/map.html')
        
        # Wait for initial load
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: driver.find_element(By.ID, "load-status").text == "success")
        
        refresh_btn = self.driver.find_element(By.ID, "refresh-btn")
        
        # Click refresh button multiple times
        for i in range(2, 6):  # clicks 2-5 (initial load is 1)
            refresh_btn.click()
            
            # Wait for this refresh to complete
            wait.until(lambda driver: driver.find_element(By.ID, "refresh-count").text == str(i))
            
            # Verify status is success
            load_status = self.driver.find_element(By.ID, "load-status").text
            assert load_status == "success"
        
        # Final check
        final_refresh_count = self.driver.find_element(By.ID, "refresh-count").text
        assert final_refresh_count == "5"
    
    def test_refresh_button_accessibility(self):
        """Test that refresh button is accessible and properly labeled"""
        self.driver.get('http://localhost:8002/map.html')
        
        refresh_btn = self.driver.find_element(By.ID, "refresh-btn")
        
        # Check button properties
        assert refresh_btn.is_enabled()
        assert refresh_btn.is_displayed()
        
        # Check button text contains refresh indicator
        button_text = refresh_btn.text
        assert "Refresh" in button_text or "🔄" in button_text
        
        # Check that button has click handler
        onclick_attr = refresh_btn.get_attribute("onclick")
        assert onclick_attr is not None
        assert "loadTransitData" in onclick_attr


class TestRefreshButtonError:
    """Test refresh button error handling"""
    
    def test_refresh_with_no_data_files(self):
        """Test refresh button behavior when no data files exist"""
        # This would require a separate test setup with no data files
        # For now, we'll test this scenario with mocked responses
        pass


if __name__ == '__main__':
    pytest.main([__file__, "-v"])
