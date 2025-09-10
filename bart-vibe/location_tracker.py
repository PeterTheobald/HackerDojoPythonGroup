#!/usr/bin/env python3
"""
BART and Caltrain Location Data Extractor

This program fetches real-time train locations from:
- BART GTFS-Realtime API 
- 511 Caltrain GTFS-Realtime API

Outputs simplified location data for map display.
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, List
from google.transit import gtfs_realtime_pb2

class LocationTracker:
    def __init__(self, caltrain_api_key: str = None):
        """Initialize the Location Tracker"""
        self.bart_trip_updates_url = "http://api.bart.gov/gtfsrt/tripupdate.aspx"
        self.caltrain_api_key = caltrain_api_key
        self.caltrain_vehicle_url = "https://api.511.org/transit/VehiclePositions"
        
        # BART station coordinates (approximate center positions)
        self.bart_station_coords = {
            # Pittsburg/Bay Point Line (Yellow)
            'A10': {'lat': 38.0187, 'lon': -121.9453, 'name': 'Pittsburg/Bay Point'},
            'A20': {'lat': 38.0033, 'lon': -122.0253, 'name': 'North Concord'},
            'A30': {'lat': 37.9737, 'lon': -122.0297, 'name': 'Concord'},
            'A40': {'lat': 37.9527, 'lon': -122.0565, 'name': 'Pleasant Hill'},
            'A50': {'lat': 37.9066, 'lon': -122.0654, 'name': 'Walnut Creek'},
            'A60': {'lat': 37.8933, 'lon': -122.1237, 'name': 'Lafayette'},
            'A70': {'lat': 37.8784, 'lon': -122.1837, 'name': 'Orinda'},
            'A80': {'lat': 37.8445, 'lon': -122.2516, 'name': 'Rockridge'},
            'A90': {'lat': 37.8297, 'lon': -122.2661, 'name': 'MacArthur'},
            
            # Antioch eBART Extension (Yellow Line)
            'A05': {'lat': 38.0049, 'lon': -121.8057, 'name': 'Antioch'},
            'A06': {'lat': 37.9955, 'lon': -121.8806, 'name': 'Hillcrest'},
            'A07': {'lat': 38.0187, 'lon': -121.9453, 'name': 'Pittsburg Center'},
            
            # San Francisco Stations (Blue/Green/Yellow/Red Lines)
            'S10': {'lat': 37.7927, 'lon': -122.3967, 'name': 'Embarcadero'},
            'S20': {'lat': 37.7894, 'lon': -122.4017, 'name': 'Montgomery'},
            'S30': {'lat': 37.7844, 'lon': -122.4079, 'name': 'Powell'},
            'S40': {'lat': 37.7801, 'lon': -122.4135, 'name': 'Civic Center'},
            'S50': {'lat': 37.7656, 'lon': -122.4197, 'name': '16th Street'},
            'S60': {'lat': 37.7527, 'lon': -122.4184, 'name': '24th Street'},
            'S70': {'lat': 37.7334, 'lon': -122.4337, 'name': 'Glen Park'},
            'S80': {'lat': 37.7212, 'lon': -122.4474, 'name': 'Balboa Park'},
            'S90': {'lat': 37.7062, 'lon': -122.4692, 'name': 'Daly City'},
            
            # Oakland/East Bay Main Line
            'B10': {'lat': 37.7975, 'lon': -122.2654, 'name': 'Lake Merritt'},
            'B20': {'lat': 37.7749, 'lon': -122.2244, 'name': 'Fruitvale'},
            'B30': {'lat': 37.7540, 'lon': -122.1969, 'name': 'Coliseum'},
            
            # Berkeley/Richmond Line (Red/Orange)
            'D10': {'lat': 37.8700, 'lon': -122.2680, 'name': 'Berkeley'},
            'D20': {'lat': 37.8741, 'lon': -122.2834, 'name': 'North Berkeley'},
            'D30': {'lat': 37.9003, 'lon': -122.2992, 'name': 'El Cerrito Plaza'},
            'D40': {'lat': 37.9254, 'lon': -122.3173, 'name': 'El Cerrito del Norte'},
            'D50': {'lat': 37.9372, 'lon': -122.3534, 'name': 'Richmond'},
            
            # East Bay Additional Stations
            'E10': {'lat': 37.8518, 'lon': -122.2699, 'name': 'Ashby'},
            'E20': {'lat': 37.8700, 'lon': -122.2680, 'name': 'Downtown Berkeley'},
            
            # Fremont/Warm Springs Line (Green/Orange)
            'F10': {'lat': 37.6975, 'lon': -122.0870, 'name': 'Castro Valley'},
            'F20': {'lat': 37.6999, 'lon': -121.9280, 'name': 'West Dublin/Pleasanton'},
            'F30': {'lat': 37.7016, 'lon': -121.9004, 'name': 'Dublin/Pleasanton'},
            
            # South Bay/Fremont Line
            'G10': {'lat': 37.6699, 'lon': -122.0873, 'name': 'Hayward'},
            'G20': {'lat': 37.6348, 'lon': -122.0577, 'name': 'South Hayward'},
            'G30': {'lat': 37.5933, 'lon': -122.0179, 'name': 'Union City'},
            'G40': {'lat': 37.5569, 'lon': -121.9763, 'name': 'Fremont'},
            'G50': {'lat': 37.5023, 'lon': -121.9395, 'name': 'Warm Springs/South Fremont'},
            
            # Peninsula/SFO Line
            'H10': {'lat': 37.6372, 'lon': -122.4165, 'name': 'San Bruno'},
            'H20': {'lat': 37.6576, 'lon': -122.4448, 'name': 'South San Francisco'},
            'H30': {'lat': 37.6845, 'lon': -122.4662, 'name': 'Colma'},
            'H40': {'lat': 37.7062, 'lon': -122.4692, 'name': 'Daly City'},
            'H50': {'lat': 37.7212, 'lon': -122.4474, 'name': 'Balboa Park'},
            
            # Airport Connector
            'K10': {'lat': 37.6003, 'lon': -122.3867, 'name': 'Millbrae'},
            'K20': {'lat': 37.6372, 'lon': -122.4165, 'name': 'San Bruno'},
            'L10': {'lat': 37.6159, 'lon': -122.3925, 'name': 'SFO Airport'},
            
            # Oakland Airport Connector
            'R10': {'lat': 37.7125, 'lon': -122.2126, 'name': 'Oakland Airport'},
            
            # Silicon Valley Extension (Green Line to Berryessa)
            'M10': {'lat': 37.4087, 'lon': -121.9190, 'name': 'Milpitas'},
            'M20': {'lat': 37.3694, 'lon': -121.9267, 'name': 'Berryessa/North San José'},
            
            # Additional East Bay stations that might be missing
            'C10': {'lat': 37.8041, 'lon': -122.2711, 'name': '12th St Oakland City Center'},
            'C20': {'lat': 37.8049, 'lon': -122.2719, 'name': '19th St Oakland'},
            'C30': {'lat': 37.8169, 'lon': -122.2681, 'name': 'MacArthur'},
            'C40': {'lat': 37.8534, 'lon': -122.2593, 'name': 'Rockridge'},
            
            # West Oakland
            'W10': {'lat': 37.8047, 'lon': -122.2951, 'name': 'West Oakland'},
            
            # Alternative codes that might be used for some stations
            'ANTC': {'lat': 38.0049, 'lon': -121.8057, 'name': 'Antioch'},
            'PCTR': {'lat': 38.0187, 'lon': -121.9453, 'name': 'Pittsburg Center'},
            
            # Additional station codes found in BART data
            'M60': {'lat': 37.3694, 'lon': -121.9267, 'name': 'Berryessa/North San José'},
            'M30': {'lat': 37.4087, 'lon': -121.9190, 'name': 'Milpitas'},
            'M50': {'lat': 37.5569, 'lon': -121.9763, 'name': 'Fremont'},
            'M80': {'lat': 37.5023, 'lon': -121.9395, 'name': 'Warm Springs/South Fremont'},
            'M90': {'lat': 37.5933, 'lon': -122.0179, 'name': 'Union City'},
            'M16': {'lat': 37.6348, 'lon': -122.0577, 'name': 'South Hayward'},
            
            # More K-line (Peninsula)
            'K30': {'lat': 37.6845, 'lon': -122.4662, 'name': 'Colma'},
            
            # R-line stations  
            'R20': {'lat': 37.7125, 'lon': -122.2126, 'name': 'Oakland Airport'},
            'R50': {'lat': 37.7540, 'lon': -122.1969, 'name': 'Coliseum'},
            'R60': {'lat': 37.7749, 'lon': -122.2244, 'name': 'Fruitvale'},
            
            # C-line (Oakland area)
            'C50': {'lat': 37.8049, 'lon': -122.2719, 'name': '19th St Oakland'},
            'C80': {'lat': 37.8169, 'lon': -122.2681, 'name': 'MacArthur'},
            
            # Y-line stations (might be Antioch extension)
            'Y10': {'lat': 38.0049, 'lon': -121.8057, 'name': 'Antioch'},
            
            # W-line stations
            'W40': {'lat': 37.8047, 'lon': -122.2951, 'name': 'West Oakland'},
            
            # L-line (Airport related)
            'L20': {'lat': 37.6159, 'lon': -122.3925, 'name': 'SFO Airport'},
            'L30': {'lat': 37.6003, 'lon': -122.3867, 'name': 'Millbrae'},
            
            # E-line (East Bay)
            'E30': {'lat': 37.8518, 'lon': -122.2699, 'name': 'Ashby'},
            
            # Additional missing stations found
            'M70': {'lat': 37.5709, 'lon': -121.9787, 'name': 'Union City'},
            'W20': {'lat': 37.8047, 'lon': -122.2951, 'name': 'West Oakland'},  
            'C60': {'lat': 37.8518, 'lon': -122.2699, 'name': 'Ashby'},
            'M40': {'lat': 37.5349, 'lon': -121.8890, 'name': 'Newark'},
        }

    def get_bart_locations(self) -> List[Dict]:
        """Get BART train locations (estimated from next station, not real GPS)"""
        locations = []
        
        try:
            print("Fetching BART train locations...")
            print("  Note: BART doesn't provide real GPS coordinates, estimating from stations")
            response = requests.get(self.bart_trip_updates_url, timeout=10)
            response.raise_for_status()
            
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            for entity in feed.entity:
                if entity.HasField('trip_update'):
                    trip_update = entity.trip_update
                    
                    # Get the next stop to estimate train location
                    if trip_update.stop_time_update:
                        next_stop = trip_update.stop_time_update[0]
                        stop_id = next_stop.stop_id
                        
                        # Extract station code
                        station_code = stop_id.split('-')[0] if '-' in stop_id else stop_id
                        
                        if station_code in self.bart_station_coords:
                            coord = self.bart_station_coords[station_code]
                            
                            location = {
                                'system': 'BART',
                                'vehicle_id': trip_update.trip.trip_id,
                                'latitude': coord['lat'],
                                'longitude': coord['lon'],
                                'station': coord['name'],
                                'delay_seconds': next_stop.arrival.delay if next_stop.HasField('arrival') and next_stop.arrival.HasField('delay') else 0,
                                'gps_source': 'estimated_from_station'  # Indicate this is not real GPS
                            }
                            locations.append(location)
                        else:
                            # Log unknown station codes to help identify missing stations
                            print(f"  Unknown station code: {station_code} (full stop_id: {stop_id})")
            
            print(f"✓ Found {len(locations)} BART train locations (estimated)")
            
        except Exception as e:
            print(f"✗ Error fetching BART locations: {e}")
        
        return locations

    def get_caltrain_locations(self) -> List[Dict]:
        """Get Caltrain vehicle locations"""
        locations = []
        
        if not self.caltrain_api_key:
            print("✗ No Caltrain API key - skipping Caltrain data")
            return locations
        
        try:
            print("Fetching Caltrain vehicle locations...")
            
            # Try different parameter combinations for 511.org API
            params_list = [
                {'api_key': self.caltrain_api_key, 'agency': 'CT'},
                {'api_key': self.caltrain_api_key, 'operator_id': 'CT'},
                {'api_key': self.caltrain_api_key, 'agency': 'Caltrain'},
                {'api_key': self.caltrain_api_key}
            ]
            
            for i, params in enumerate(params_list):
                try:
                    print(f"  Trying parameter set {i+1}...")
                    response = requests.get(self.caltrain_vehicle_url, params=params, timeout=10)
                    
                    if response.status_code == 200:
                        print(f"  ✓ Success with parameter set {i+1}")
                        
                        # Try to parse as GTFS-RT
                        try:
                            feed = gtfs_realtime_pb2.FeedMessage()
                            feed.ParseFromString(response.content)
                            
                            for entity in feed.entity:
                                if entity.HasField('vehicle') and entity.vehicle.HasField('position'):
                                    vehicle = entity.vehicle
                                    pos = vehicle.position
                                    
                                    if pos.HasField('latitude') and pos.HasField('longitude'):
                                        location = {
                                            'system': 'Caltrain',
                                            'vehicle_id': vehicle.vehicle.id if vehicle.vehicle.HasField('id') else f"train_{entity.id}",
                                            'latitude': pos.latitude,
                                            'longitude': pos.longitude,
                                            'speed_mps': pos.speed if pos.HasField('speed') else None,
                                            'bearing': pos.bearing if pos.HasField('bearing') else None
                                        }
                                        locations.append(location)
                            break
                            
                        except Exception as parse_error:
                            print(f"  ✗ Parse error: {parse_error}")
                            # Try to see what we actually got
                            print(f"  Response content type: {response.headers.get('content-type', 'unknown')}")
                            print(f"  Response length: {len(response.content)} bytes")
                            
                    else:
                        print(f"  ✗ HTTP {response.status_code}: {response.reason}")
                        
                except requests.exceptions.RequestException as req_error:
                    print(f"  ✗ Request error: {req_error}")
                    continue
            
            print(f"✓ Found {len(locations)} Caltrain vehicle locations")
            
        except Exception as e:
            print(f"✗ Error fetching Caltrain locations: {e}")
        
        return locations

    def save_locations(self, bart_locations: List[Dict], caltrain_locations: List[Dict]):
        """Save location data to JSON file"""
        timestamp = datetime.now()
        
        data = {
            'timestamp': timestamp.isoformat(),
            'total_vehicles': len(bart_locations) + len(caltrain_locations),
            'bart_count': len(bart_locations),
            'caltrain_count': len(caltrain_locations),
            'locations': bart_locations + caltrain_locations
        }
        
        filename = f"transit_locations_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Location data saved to {filename}")
            return filename
        except Exception as e:
            print(f"✗ Error saving data: {e}")
            return None

def main():
    """Main function"""
    print("🗺️  Transit Location Data Extractor")
    print("=" * 40)
    
    # Get API key from environment
    caltrain_api_key = os.getenv('CALTRAIN_API_KEY')
    
    tracker = LocationTracker(caltrain_api_key)
    
    # Fetch location data
    bart_locations = tracker.get_bart_locations()
    caltrain_locations = tracker.get_caltrain_locations()
    
    # Display summary
    total = len(bart_locations) + len(caltrain_locations)
    print(f"\n📍 LOCATION SUMMARY:")
    print(f"   BART trains: {len(bart_locations)}")
    print(f"   Caltrain vehicles: {len(caltrain_locations)}")
    print(f"   Total vehicles: {total}")
    
    if total > 0:
        # Show sample locations
        print(f"\n📋 SAMPLE LOCATIONS:")
        all_locations = bart_locations + caltrain_locations
        for i, loc in enumerate(all_locations[:3], 1):
            station_info = f" near {loc['station']}" if 'station' in loc else ""
            print(f"   {i}. {loc['system']} {loc['vehicle_id']}: ({loc['latitude']:.4f}, {loc['longitude']:.4f}){station_info}")
        
        if len(all_locations) > 3:
            print(f"   ... and {len(all_locations) - 3} more vehicles")
        
        # Save data
        filename = tracker.save_locations(bart_locations, caltrain_locations)
        if filename:
            print(f"\n✅ Ready for map display! Use data from: {filename}")
    else:
        print("\n⚠️  No location data found")

if __name__ == "__main__":
    main()
