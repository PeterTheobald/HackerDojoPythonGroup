# app.py — Real-time Bay Area trains (BART + Caltrain) on a live map using 511.org SIRI VehicleMonitoring
# Run:  BART_511_API_KEY=YOUR_KEY bokeh serve --show app.py
# Deps: pip install bokeh requests

import os, math, time, json, threading
from functools import lru_cache
import requests
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.layouts import column
import json

API_KEY = os.getenv("BART_511_API_KEY") or os.getenv("FIVE11_API_KEY") or os.getenv("API_511_KEY")
if not API_KEY:
    print('ERROR You must supply a BART API key in BART_511_API_KEY')
    curdoc().add_root(Div(text="<b>Set env var BART_511_API_KEY (or FIVE11_API_KEY/API_511_KEY) with your 511 API token.</b>"))

BASE = "http://api.511.org/transit"

# --- small helpers ---
def wgs84_to_web_mercator(lon, lat):
    k = 6378137.0
    x = lon * (math.pi/180.0) * k
    y = math.log(math.tan((math.pi/4.0) + (lat * math.pi/360.0))) * k
    return x, y

HEADERS = {"Accept": "application/json"}

@lru_cache(maxsize=1)
def get_operator_ids():
    """Return {'BART': 'BA', 'Caltrain': '<id>'} by querying 511 Operators API once."""
    r = requests.get(f"{BASE}/operators", params={"api_key": API_KEY, "format": "json"}, headers=HEADERS, timeout=15)
    r.raise_for_status()
    ops = safe_json(r)
    # Response can be list or dict with 'content'; normalize to list of dicts with Id/Name keys.
    if isinstance(ops, dict) and "content" in ops:
        entries = ops["content"]
    else:
        entries = ops
    
    # Debug: print all operators to see what we get
    print("Available operators:")
    for op in entries:
        print(f"  ID: {op.get('Id')}, Name: {op.get('Name')}")
    
    # Look specifically for BART by exact name matches only
    bart = None
    for op in entries:
        name = op.get("Name", "")
        # Look for exact BART matches, not partial
        if name == "Bay Area Rapid Transit":
            bart = op["Id"]
            print(f"Found exact BART match: {op}")
            break
    
    # Force use of BA if no exact match (we know from output that BA = Bay Area Rapid Transit)
    if not bart:
        bart = "BA"
        print(f"Using fallback BART operator ID: BA")
    
    caltrain = next((o["Id"] for o in entries if "caltrain" in o.get("Name","").lower()), None)
    
    print(f"Final selected operators - BART: {bart}, Caltrain: {caltrain}")
    return {"BART": bart, "Caltrain": caltrain}

def fetch_vehicle_monitoring(operator_id):
    """Call SIRI VehicleMonitoring JSON; return list of dicts with lon/lat/line/veh/ts/bearing."""
    if not operator_id:
        return []
    print(f"Fetching vehicles for operator: {operator_id}")
    try:
        r = requests.get(f"{BASE}/VehicleMonitoring", params={"api_key": API_KEY, "agency": operator_id, "format": "json"}, headers=HEADERS, timeout=20)
        r.raise_for_status()
        
        # Check if response is the rate limit error
        if "exceeded" in r.text.lower():
            print(f"Rate limit exceeded for operator {operator_id}: {r.text}")
            return []
            
        data = safe_json(r)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for operator {operator_id}: {e}")
        return []
    # Navigate SIRI JSON safely
    sd = data.get("Siri", {}).get("ServiceDelivery", {})
    vmd = sd.get("VehicleMonitoringDelivery") or []
    if isinstance(vmd, dict):
        vmd = [vmd]
    out = []
    for delivery in vmd:
        for act in delivery.get("VehicleActivity", []) or []:
            mvj = act.get("MonitoredVehicleJourney", {})
            loc = mvj.get("VehicleLocation") or {}
            try:
                lat = float(loc.get("Latitude"))
                lon = float(loc.get("Longitude"))
            except (TypeError, ValueError):
                continue
            
            # Filter to Bay Area bounds: lat [36.8, 38.7], lon [-123.1, -121.2]
            if not (36.8 <= lat <= 38.7 and -123.1 <= lon <= -121.2):
                continue
            
            vehicle_data = {
                "lat": lat,
                "lon": lon,
                "line": str(mvj.get("LineRef") or ""),
                "vehicle": str(mvj.get("VehicleRef") or ""),
                "bearing": mvj.get("Bearing"),
                "updated": act.get("RecordedAtTime") or sd.get("ResponseTimestamp"),
            }
            
            # Debug: print a few sample coordinates to see if they look reasonable
            if len(out) < 3:  # Only print first few to avoid spam
                print(f"  Vehicle {vehicle_data['vehicle']} at lat={lat:.4f}, lon={lon:.4f}, line={vehicle_data['line']}")
            
            out.append(vehicle_data)
    
    print(f"Found {len(out)} vehicles for operator {operator_id}")
    return out

def safe_json(r):
    try:
        return r.json()
    except json.JSONDecodeError:
        return json.loads(r.content.decode("utf-8-sig"))

# --- Bokeh setup ---
if not API_KEY:
    curdoc().add_root(Div(text="<b>Set environment var BART_511_API_KEY (or FIVE11_API_KEY) with your 511 API token.</b>"))
    raise SystemExit

OPS = get_operator_ids()
TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

# Bay Area bounds (approx): lon [-123.1, -121.2], lat [36.8, 38.7]
x0,y0 = wgs84_to_web_mercator(-123.1, 36.8)
x1,y1 = wgs84_to_web_mercator(-121.2, 38.7)

p = figure(x_range=(x0, x1), y_range=(y0, y1), x_axis_type="mercator", y_axis_type="mercator", tools=TOOLS, title="BART + Caltrain (real-time)", sizing_mode="stretch_both")
p.add_tile("CartoDB Positron")

bart_src = ColumnDataSource(dict(x=[], y=[], line=[], vehicle=[], updated=[], agency=[]))
cal_src  = ColumnDataSource(dict(x=[], y=[], line=[], vehicle=[], updated=[], agency=[]))

bart_glyph = p.circle(x="x", y="y", size=10, fill_alpha=0.9, line_alpha=0.8, color="#1f77b4", legend_label="BART", source=bart_src)
cal_glyph  = p.square(x="x", y="y", size=10, fill_alpha=0.9, line_alpha=0.8, color="#d62728", legend_label="Caltrain", source=cal_src)

p.legend.location = "top_left"
p.add_tools(HoverTool(renderers=[bart_glyph, cal_glyph],
                      tooltips=[("Agency","@agency"),("Line","@line"),("Vehicle","@vehicle"),("Updated","@updated")]))
status_div = Div(text="")

layout = column(p, status_div, sizing_mode="stretch_both")  # ← fill vertically too
curdoc().clear()
curdoc().add_root(layout)

_lock = threading.Lock()

def refresh():
    try:
        bart = fetch_vehicle_monitoring(OPS.get("BART"))
        cal  = fetch_vehicle_monitoring(OPS.get("Caltrain"))
        
        # Debug what we're getting from each operator
        print(f"DEBUG: Raw BART data has {len(bart)} vehicles")
        print(f"DEBUG: Raw Caltrain data has {len(cal)} vehicles")
        
        # Show some sample BART data to verify we're getting actual trains
        for i, rec in enumerate(bart[:3]):
            print(f"  BART vehicle {i}: lat={rec['lat']:.4f}, lon={rec['lon']:.4f}, line='{rec['line']}', vehicle='{rec['vehicle']}'")
        
        bx, by, cx, cy = [], [], [], []
        for rec in bart:
            x,y = wgs84_to_web_mercator(rec["lon"], rec["lat"])
            bx.append(x); by.append(y)
        for rec in cal:
            x,y = wgs84_to_web_mercator(rec["lon"], rec["lat"])
            cx.append(x); cy.append(y)
        with _lock:
            bart_src.data = dict(
                x=bx, y=by,
                line=[r["line"] for r in bart],
                vehicle=[r["vehicle"] for r in bart],
                updated=[r["updated"] for r in bart],
                agency=["BART"]*len(bart),
            )
            cal_src.data = dict(
                x=cx, y=cy,
                line=[r["line"] for r in cal],
                vehicle=[r["vehicle"] for r in cal],
                updated=[r["updated"] for r in cal],
                agency=["Caltrain"]*len(cal),
            )
            status_div.text = f"Updated {time.strftime('%Y-%m-%d %H:%M:%S')} • BART: {len(bart_src.data['x'])} • Caltrain: {len(cal_src.data['x'])}"
    except Exception as e:
        status_div.text = f"<b>Error:</b> {e}"

# initial & periodic - refresh every 60 seconds to stay within rate limits
refresh()
curdoc().add_periodic_callback(refresh, 60_000)  # 60 seconds instead of 10

