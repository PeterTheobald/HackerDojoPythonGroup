import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

# App title
st.title("🌍 Earthquake Data Visualization")

# Load earthquake data
@st.cache_data
def load_data():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.csv"
    data = pd.read_csv(url)
    data["time"] = pd.to_datetime(data["time"])
    return data

data = load_data()

# Sidebar controls
st.sidebar.header("Filter Data")
min_magnitude = st.sidebar.slider("Minimum Magnitude", 2.5, 10.0, 4.0, step=0.1)
date_range = st.sidebar.date_input(
    "Select Date Range",
    [data["time"].min().date(), data["time"].max().date()],
)

# Extract start and end date
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = data["time"].min().date()
    end_date = data["time"].max().date()

# Filter data
filtered_data = data[
    (data["mag"] >= min_magnitude) &
    (data["time"].dt.date >= start_date) &
    (data["time"].dt.date <= end_date)
]

# Precompute radius for Pydeck
if not filtered_data.empty:
    filtered_data["radius"] = filtered_data["mag"] ** 2 * 1000  # Precompute radius

# Map visualization
st.header("Earthquakes Map")
if not filtered_data.empty:
    st.map(filtered_data[["latitude", "longitude"]])
else:
    st.write("No data available for the selected filters.")

# Advanced Pydeck visualization
st.header("Advanced Visualization")
if not filtered_data.empty:
    # Define Pydeck layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered_data,
        get_position=["longitude", "latitude"],
        get_radius="radius",  # Use precomputed radius column
        get_fill_color="[255, 140, 0, 160]",  # Semi-transparent orange
        pickable=True,
    )

    # Define view state
    view_state = pdk.ViewState(
        latitude=filtered_data["latitude"].mean(),
        longitude=filtered_data["longitude"].mean(),
        zoom=3,
        pitch=50,
    )

    # Render Pydeck chart
    deck = pdk.Deck(layers=[layer], initial_view_state=view_state)
    st.pydeck_chart(deck)
else:
    st.write("No data available to display on the advanced map.")

# Additional insights
st.subheader("Filtered Data")
st.write(filtered_data)

