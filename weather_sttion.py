import pandas as pd
import folium
import requests
from io import StringIO

print("Downloading station data...")
# Download ISD station inventory
url = "https://www.ncei.noaa.gov/pub/data/noaa/isd-history.csv"
response = requests.get(url)
stations_df = pd.read_csv(StringIO(response.text))
print(f"Downloaded {len(stations_df)} total stations")

# Filter for African stations (rough bounding box)
african_stations = stations_df[
    (stations_df['LAT'].between(-40, 40)) & 
    (stations_df['LON'].between(-20, 50)) &
    (stations_df['END'] >= 2020)  # Filter for recently active stations
]
print(f"Found {len(african_stations)} African stations")

# Create a simple folium map
m = folium.Map(location=[0, 20], zoom_start=4)

print("Adding stations to map...")
# Add weather stations to the map
for idx, row in african_stations.iterrows():
    # Determine if station is currently active
    is_active = str(row['END']) >= '2024'
    color = 'blue' if is_active else 'red'
    
    folium.CircleMarker(
        location=[row['LAT'], row['LON']],
        radius=6,
        color=color,
        fill=True,
        popup=f"Station: {row['STATION NAME']}<br>" \
              f"USAF-WBAN: {row['USAF']}-{row['WBAN']}<br>" \
              f"Period: {row['BEGIN']}-{row['END']}<br>" \
              f"Elevation: {row['ELEV(M)']}m",
        weight=2
    ).add_to(m)

# Add a legend
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; right: 50px; width: 150px; height: 90px; 
            border:2px solid grey; z-index:9999; background-color:white;
            opacity:0.8;
            font-size:12px;
            padding: 10px">
            <b>Weather Stations</b><br>
            <i class="fa fa-circle" style="color:blue"></i> Active Station (2024)<br>
            <i class="fa fa-circle" style="color:red"></i> Historical Station
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

print("Saving map...")
# Save the map
m.save('african_weather_stations.html')
print("Map saved as 'african_weather_stations.html'")
