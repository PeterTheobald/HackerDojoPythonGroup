# Real-time BART and Caltrain Location Tracker

This program fetches real-time train locations from BART and Caltrain APIs and displays them on an interactive map.

## Features

- ✅ Fetches real-time BART train data (estimated positions from stations)
- ✅ Fetches real-time Caltrain data with GPS coordinates
- ✅ Interactive Leaflet map display
- ✅ Auto-refresh capability
- ✅ Saves data to JSON files with timestamps

## Setup

1. **Install dependencies**:
   ```bash
   uv add requests gtfs-realtime-bindings protobuf
   ```

2. **Get a 511.org API key** (for Caltrain data):
   - Visit: https://511.org/open-data/token
   - Register for a free API key
   - Set the environment variable:
     ```bash
     export CALTRAIN_API_KEY='your_api_key_here'
     ```

## Usage

### Collect Transit Data
Set your Caltrain API key using the secrets file:
```bash
source bart_secrets.sh
```

Run the location tracker:
```bash
uv run location_tracker.py
```

### View on Interactive Map
Start the web server:
```bash
uv run server.py
```

This will:
- Start a local web server on port 8000
- Automatically open the map in your browser
- Display real-time train locations
- Auto-refresh every 30 seconds

## Map Features

🗺️ **Interactive Map**:
- 🔵 Blue dots = BART trains (estimated positions)
- 🟠 Orange dots = Caltrain vehicles (GPS positions)
- Click markers for detailed information
- Auto-refresh button and live updates

📊 **Real-time Data**:
- Train/vehicle counts by system
- Delay information for BART
- Speed and bearing data for Caltrain
- Last update timestamp

## APIs Used

### BART GTFS-Realtime API
- **Endpoint**: `http://api.bart.gov/gtfsrt/tripupdate.aspx`
- **Format**: GTFS-Realtime protobuf
- **Authentication**: None required
- **Data**: Trip updates, estimated arrivals

### 511.org Caltrain API
- **Endpoint**: `https://api.511.org/transit/VehiclePositions`
- **Format**: GTFS-Realtime protobuf
- **Authentication**: API key required
- **Data**: Real-time vehicle positions, trip information

## Output Files

The program generates timestamped JSON files:
- `bart_data_YYYYMMDD_HHMMSS.json` - Complete BART data
- `caltrain_data_YYYYMMDD_HHMMSS.json` - Complete Caltrain data
- `transit_summary_YYYYMMDD_HHMMSS.json` - Summary statistics

## Example Output

```
🚆 Real-time BART and Caltrain Location Tracker
==================================================
Fetching real-time transit data...

Fetching BART trip updates...
✓ Found 45 BART trains

Fetching Caltrain vehicle positions...
✓ Found 12 Caltrain vehicles

============================================================
REAL-TIME TRANSIT DATA SUMMARY
============================================================

🚇 BART TRAINS:
   Total trains found: 45
   1. Trip: 03SFO24, Route: 01, Vehicle: 1523
   2. Trip: 05DAL24, Route: 05, Vehicle: 2108
   ...

🚅 CALTRAIN TRAINS:
   Total vehicles found: 12
   1. Vehicle: 123, Trip: 456, Route: ct_local at (37.7749, -122.4194)
   2. Vehicle: 789, Trip: 012, Route: ct_bullet at (37.5630, -122.3255)
   ...
```

## Notes

- BART data is available 24/7 but train frequency varies by time of day
- Caltrain data requires a free API key from 511.org
- The program handles API errors gracefully and will show partial results
- Data is saved in JSON format for further analysis or visualization

## Next Steps

This data can be used to:
- Create a real-time map visualization
- Build arrival prediction systems
- Analyze transit patterns and frequencies
- Integrate with other Bay Area transit APIs
