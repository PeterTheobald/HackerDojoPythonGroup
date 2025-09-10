#!/usr/bin/env python3
"""
Real-time BART and Caltrain Location Tracker

This program fetches real-time train locations from:
- BART GTFS-Realtime API
- 511 Caltrain GTFS-Realtime API

Displays train information and saves data to files.
"""

import requests
import json
import time
import os
from datetime import datetime
from typing import Dict, List, Optional
from google.transit import gtfs_realtime_pb2

class TransitTracker:
    def __init__(self, caltrain_api_key: Optional[str] = None):
        """
        Initialize the Transit Tracker
        
        Args:
            caltrain_api_key: API key for 511.org (required for Caltrain data)
        """
        # BART GTFS-RT URLs (no API key required)
        self.bart_trip_updates_url = "http://api.bart.gov/gtfsrt/tripupdate.aspx"
        # Note: Vehicle positions may not be available from BART's GTFS-RT feed
        self.bart_vehicle_positions_url = "http://api.bart.gov/gtfsrt/vehiclepositions.aspx"
        self.bart_alerts_url = "http://api.bart.gov/gtfsrt/alerts.aspx"
        
        # 511 Caltrain GTFS-RT URLs (API key required)
        self.caltrain_api_key = caltrain_api_key
        self.caltrain_base_url = "https://api.511.org/transit/VehiclePositions"
        self.caltrain_trip_updates_url = "https://api.511.org/transit/TripUpdates"
        
        # Headers for requests
        self.headers = {
            'User-Agent': 'Transit-Tracker/1.0 (Educational Project)'
        }
        
        # Basic BART station mapping (partial list for common stations)
        self.bart_stations = {
            'A10': 'Pittsburg/Bay Point', 'A20': 'North Concord', 'A30': 'Concord',
            'A40': 'Pleasant Hill', 'A50': 'Walnut Creek', 'A60': 'Lafayette',
            'A70': 'Orinda', 'A80': 'Rockridge', 'A90': 'MacArthur',
            'S10': 'Embarcadero', 'S20': 'Montgomery', 'S30': 'Powell',
            'S40': 'Civic Center', 'S50': '16th Street', 'S60': '24th Street',
            'S70': 'Glen Park', 'S80': 'Balboa Park', 'S90': 'Daly City',
            'B10': 'Lake Merritt', 'B20': 'Fruitvale', 'B30': 'Coliseum',
            'D10': 'Berkeley', 'D20': 'North Berkeley', 'D30': 'El Cerrito Plaza',
            'D40': 'El Cerrito del Norte', 'D50': 'Richmond',
            'E10': 'Ashby', 'E20': 'Downtown Berkeley', 'E30': 'North Berkeley',
            'F10': 'Castro Valley', 'F20': 'West Dublin', 'F30': 'Dublin/Pleasanton',
            'G10': 'Hayward', 'G20': 'South Hayward', 'G30': 'Union City',
            'G40': 'Fremont', 'H10': 'San Bruno', 'H20': 'South San Francisco',
            'H30': 'Colma', 'H40': 'Daly City', 'H50': 'Balboa Park',
            'K10': 'Millbrae', 'K20': 'San Bruno', 'L10': 'SFO Airport',
            'R10': 'Oakland Airport'
        }

    def get_station_name(self, stop_id: str) -> str:
        """Convert BART stop ID to readable station name"""
        if not stop_id or stop_id == 'Unknown':
            return stop_id
        
        # Extract station code (remove direction suffix like -1, -2)
        station_code = stop_id.split('-')[0] if '-' in stop_id else stop_id
        
        return self.bart_stations.get(station_code, stop_id)

    def fetch_bart_data(self) -> Dict:
        """Fetch BART real-time data"""
        bart_data = {
            'timestamp': datetime.now().isoformat(),
            'trip_updates': None,
            'alerts': None,
            'trains': [],
            'error': None
        }
        
        try:
            print("Fetching BART trip updates...")
            response = requests.get(self.bart_trip_updates_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse GTFS-RT protobuf data
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            bart_data['trip_updates'] = {
                'feed_timestamp': feed.header.timestamp,
                'entities_count': len(feed.entity)
            }
            
            # Extract train information with more detailed parsing
            for entity in feed.entity:
                if entity.HasField('trip_update'):
                    trip_update = entity.trip_update
                    
                    # Get basic trip info
                    trip_id = trip_update.trip.trip_id if trip_update.trip.HasField('trip_id') else 'Unknown'
                    route_id = trip_update.trip.route_id if trip_update.trip.HasField('route_id') else 'Unknown'
                    
                    # Check for vehicle info
                    vehicle_id = 'Unknown'
                    if trip_update.HasField('vehicle'):
                        if trip_update.vehicle.HasField('id'):
                            vehicle_id = trip_update.vehicle.id
                        elif trip_update.vehicle.HasField('label'):
                            vehicle_id = trip_update.vehicle.label
                    
                    # Get stop time updates with more details
                    stop_updates = []
                    for stop_update in trip_update.stop_time_update:
                        stop_info = {
                            'stop_id': stop_update.stop_id if stop_update.HasField('stop_id') else 'Unknown',
                            'arrival_delay': stop_update.arrival.delay if stop_update.HasField('arrival') and stop_update.arrival.HasField('delay') else None,
                            'arrival_time': stop_update.arrival.time if stop_update.HasField('arrival') and stop_update.arrival.HasField('time') else None,
                            'departure_delay': stop_update.departure.delay if stop_update.HasField('departure') and stop_update.departure.HasField('delay') else None,
                            'departure_time': stop_update.departure.time if stop_update.HasField('departure') and stop_update.departure.HasField('time') else None
                        }
                        stop_updates.append(stop_info)
                    
                    train_info = {
                        'entity_id': entity.id,
                        'trip_id': trip_id,
                        'route_id': route_id,
                        'vehicle_id': vehicle_id,
                        'stop_updates_count': len(trip_update.stop_time_update),
                        'stop_updates': stop_updates[:3]  # Show first 3 stops for brevity
                    }
                    bart_data['trains'].append(train_info)
            
            print(f"✓ Found {len(bart_data['trains'])} BART trains with trip updates")
            
        except Exception as e:
            error_msg = f"Error fetching BART data: {str(e)}"
            print(f"✗ {error_msg}")
            bart_data['error'] = error_msg
        
        return bart_data

    def fetch_bart_vehicle_positions(self) -> Dict:
        """Fetch BART vehicle positions for actual train locations"""
        vehicle_data = {
            'timestamp': datetime.now().isoformat(),
            'vehicles': [],
            'error': None
        }
        
        try:
            print("Fetching BART vehicle positions...")
            response = requests.get(self.bart_vehicle_positions_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse GTFS-RT protobuf data
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            # Extract vehicle position information
            for entity in feed.entity:
                if entity.HasField('vehicle'):
                    vehicle = entity.vehicle
                    
                    # Get vehicle info
                    vehicle_id = 'Unknown'
                    if vehicle.vehicle.HasField('id'):
                        vehicle_id = vehicle.vehicle.id
                    elif vehicle.vehicle.HasField('label'):
                        vehicle_id = vehicle.vehicle.label
                    
                    # Get trip info
                    trip_id = vehicle.trip.trip_id if vehicle.HasField('trip') and vehicle.trip.HasField('trip_id') else 'Unknown'
                    route_id = vehicle.trip.route_id if vehicle.HasField('trip') and vehicle.trip.HasField('route_id') else 'Unknown'
                    
                    # Get position info
                    latitude = vehicle.position.latitude if vehicle.HasField('position') and vehicle.position.HasField('latitude') else None
                    longitude = vehicle.position.longitude if vehicle.HasField('position') and vehicle.position.HasField('longitude') else None
                    bearing = vehicle.position.bearing if vehicle.HasField('position') and vehicle.position.HasField('bearing') else None
                    speed = vehicle.position.speed if vehicle.HasField('position') and vehicle.position.HasField('speed') else None
                    
                    # Get timestamp
                    timestamp = vehicle.timestamp if vehicle.HasField('timestamp') else None
                    
                    vehicle_info = {
                        'entity_id': entity.id,
                        'vehicle_id': vehicle_id,
                        'trip_id': trip_id,
                        'route_id': route_id,
                        'latitude': latitude,
                        'longitude': longitude,
                        'bearing': bearing,
                        'speed': speed,
                        'timestamp': timestamp
                    }
                    vehicle_data['vehicles'].append(vehicle_info)
            
            print(f"✓ Found {len(vehicle_data['vehicles'])} BART vehicles with positions")
            
        except Exception as e:
            error_msg = f"Error fetching BART vehicle positions: {str(e)}"
            print(f"✗ {error_msg}")
            vehicle_data['error'] = error_msg
        
        return vehicle_data

    def fetch_caltrain_data(self) -> Dict:
        """Fetch Caltrain real-time data from 511.org"""
        caltrain_data = {
            'timestamp': datetime.now().isoformat(),
            'vehicle_positions': None,
            'trip_updates': None,
            'trains': [],
            'error': None
        }
        
        if not self.caltrain_api_key:
            error_msg = "Caltrain API key not provided. Get one from https://511.org/open-data/token"
            print(f"✗ {error_msg}")
            caltrain_data['error'] = error_msg
            return caltrain_data
        
        try:
            # Fetch vehicle positions
            print("Fetching Caltrain vehicle positions...")
            params = {
                'api_key': self.caltrain_api_key,
                'operator_id': 'CT',  # Caltrain operator ID
                'format': 'gtfs-rt'
            }
            
            response = requests.get(self.caltrain_base_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse GTFS-RT protobuf data
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            caltrain_data['vehicle_positions'] = {
                'feed_timestamp': feed.header.timestamp,
                'entities_count': len(feed.entity)
            }
            
            # Extract train information
            for entity in feed.entity:
                if entity.HasField('vehicle'):
                    vehicle = entity.vehicle
                    train_info = {
                        'vehicle_id': vehicle.vehicle.id if vehicle.vehicle.HasField('id') else 'Unknown',
                        'trip_id': vehicle.trip.trip_id if vehicle.HasField('trip') and vehicle.trip.HasField('trip_id') else 'Unknown',
                        'route_id': vehicle.trip.route_id if vehicle.HasField('trip') and vehicle.trip.HasField('route_id') else 'Unknown',
                        'latitude': vehicle.position.latitude if vehicle.HasField('position') and vehicle.position.HasField('latitude') else None,
                        'longitude': vehicle.position.longitude if vehicle.HasField('position') and vehicle.position.HasField('longitude') else None,
                        'timestamp': vehicle.timestamp if vehicle.HasField('timestamp') else None
                    }
                    caltrain_data['trains'].append(train_info)
            
            print(f"✓ Found {len(caltrain_data['trains'])} Caltrain vehicles")
            
        except Exception as e:
            error_msg = f"Error fetching Caltrain data: {str(e)}"
            print(f"✗ {error_msg}")
            caltrain_data['error'] = error_msg
        
        return caltrain_data

    def display_results(self, bart_data: Dict, bart_vehicles: Dict, caltrain_data: Dict):
        """Display the fetched train data"""
        print("\n" + "="*70)
        print("REAL-TIME TRANSIT DATA SUMMARY")
        print("="*70)
        
        # BART Trip Updates
        print(f"\n🚇 BART TRIP UPDATES:")
        if bart_data['error']:
            print(f"   Error: {bart_data['error']}")
        else:
            print(f"   Total trips found: {len(bart_data['trains'])}")
            for i, train in enumerate(bart_data['trains'][:3], 1):  # Show first 3
                stops_info = ""
                if train['stop_updates']:
                    first_stop = train['stop_updates'][0]
                    station_name = self.get_station_name(first_stop['stop_id'])
                    delay_info = f" (delay: {first_stop['arrival_delay']}s)" if first_stop['arrival_delay'] else ""
                    stops_info = f", Next: {station_name}{delay_info}"
                print(f"   {i}. Trip: {train['trip_id']}, Vehicle: {train['vehicle_id']}, Stops: {train['stop_updates_count']}{stops_info}")
            if len(bart_data['trains']) > 3:
                print(f"   ... and {len(bart_data['trains']) - 3} more trips")
        
        # BART Vehicle Positions
        print(f"\n🚇 BART VEHICLE POSITIONS:")
        if bart_vehicles['error']:
            print(f"   Error: {bart_vehicles['error']}")
        else:
            print(f"   Total vehicles found: {len(bart_vehicles['vehicles'])}")
            for i, vehicle in enumerate(bart_vehicles['vehicles'][:5], 1):  # Show first 5
                location = ""
                if vehicle['latitude'] and vehicle['longitude']:
                    location = f" at ({vehicle['latitude']:.4f}, {vehicle['longitude']:.4f})"
                speed_info = f", Speed: {vehicle['speed']:.1f} m/s" if vehicle['speed'] else ""
                print(f"   {i}. Vehicle: {vehicle['vehicle_id']}, Trip: {vehicle['trip_id']}{location}{speed_info}")
            if len(bart_vehicles['vehicles']) > 5:
                print(f"   ... and {len(bart_vehicles['vehicles']) - 5} more vehicles")
        
        # Caltrain Results
        print(f"\n🚅 CALTRAIN TRAINS:")
        if caltrain_data['error']:
            print(f"   Error: {caltrain_data['error']}")
        else:
            print(f"   Total vehicles found: {len(caltrain_data['trains'])}")
            for i, train in enumerate(caltrain_data['trains'][:5], 1):  # Show first 5
                location = ""
                if train['latitude'] and train['longitude']:
                    location = f" at ({train['latitude']:.4f}, {train['longitude']:.4f})"
                print(f"   {i}. Vehicle: {train['vehicle_id']}, Trip: {train['trip_id']}, Route: {train['route_id']}{location}")
            if len(caltrain_data['trains']) > 5:
                print(f"   ... and {len(caltrain_data['trains']) - 5} more vehicles")

    def save_data(self, bart_data: Dict, bart_vehicles: Dict, caltrain_data: Dict):
        """Save the data to JSON files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save BART trip updates
        bart_filename = f"bart_trips_{timestamp}.json"
        try:
            with open(bart_filename, 'w') as f:
                json.dump(bart_data, f, indent=2, default=str)
            print(f"✓ BART trip data saved to {bart_filename}")
        except Exception as e:
            print(f"✗ Error saving BART trip data: {e}")
        
        # Save BART vehicle positions
        bart_vehicles_filename = f"bart_vehicles_{timestamp}.json"
        try:
            with open(bart_vehicles_filename, 'w') as f:
                json.dump(bart_vehicles, f, indent=2, default=str)
            print(f"✓ BART vehicle data saved to {bart_vehicles_filename}")
        except Exception as e:
            print(f"✗ Error saving BART vehicle data: {e}")
        
        # Save Caltrain data
        caltrain_filename = f"caltrain_data_{timestamp}.json"
        try:
            with open(caltrain_filename, 'w') as f:
                json.dump(caltrain_data, f, indent=2, default=str)
            print(f"✓ Caltrain data saved to {caltrain_filename}")
        except Exception as e:
            print(f"✗ Error saving Caltrain data: {e}")
        
        # Save combined summary
        summary_data = {
            'timestamp': datetime.now().isoformat(),
            'bart_trips': {
                'count': len(bart_data['trains']) if not bart_data['error'] else 0,
                'error': bart_data['error']
            },
            'bart_vehicles': {
                'count': len(bart_vehicles['vehicles']) if not bart_vehicles['error'] else 0,
                'error': bart_vehicles['error']
            },
            'caltrain': {
                'trains_count': len(caltrain_data['trains']) if not caltrain_data['error'] else 0,
                'error': caltrain_data['error']
            }
        }
        
        summary_filename = f"transit_summary_{timestamp}.json"
        try:
            with open(summary_filename, 'w') as f:
                json.dump(summary_data, f, indent=2)
            print(f"✓ Summary saved to {summary_filename}")
        except Exception as e:
            print(f"✗ Error saving summary: {e}")

def main():
    """Main function"""
    print("🚆 Real-time BART and Caltrain Location Tracker")
    print("=" * 50)
    
    # Initialize tracker
    # Get Caltrain API key from environment variable
    caltrain_api_key = os.getenv('CALTRAIN_API_KEY')
    
    if not caltrain_api_key:
        print("⚠️  Note: No Caltrain API key found in environment variable 'CALTRAIN_API_KEY'.")
        print("   To get Caltrain data:")
        print("   1. Obtain a free API key from: https://511.org/open-data/token")
        print("   2. Set the environment variable: export CALTRAIN_API_KEY='your_key_here'")
        print("   3. Run the program again\n")
    
    tracker = TransitTracker(caltrain_api_key=caltrain_api_key)
    
    # Fetch data
    print("Fetching real-time transit data...\n")
    bart_data = tracker.fetch_bart_data()
    bart_vehicles = tracker.fetch_bart_vehicle_positions()
    caltrain_data = tracker.fetch_caltrain_data()
    
    # Display results
    tracker.display_results(bart_data, bart_vehicles, caltrain_data)
    
    # Save data to files
    print(f"\n📁 Saving data to files...")
    tracker.save_data(bart_data, bart_vehicles, caltrain_data)
    
    print(f"\n✨ Complete! Data fetched at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
