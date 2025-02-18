import ee
import pandas as pd
from datetime import datetime, timedelta
import geemap
from tqdm import tqdm
import calendar
import time

# Initialize Earth Engine
ee.Initialize()

def get_daily_temp(date, geometry):
    """Get maximum temperature for a specific date"""
    start_date = date.strftime('%Y-%m-%d')
    end_date = (date + timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Get ERA5-Land data
    collection = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY') \
        .filterDate(start_date, end_date) \
        .select('temperature_2m')
    
    if collection.size().getInfo() == 0:
        return None
    
    # Get maximum temperature and convert to Celsius
    max_temp = collection.max()
    celsius_temp = max_temp.subtract(273.15)
    
    # Get regional mean
    mean_temp = celsius_temp.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=11132
    ).getInfo()
    
    return mean_temp.get('temperature_2m')

# Define Tshwane boundaries
tshwane_center = ee.Geometry.Point([28.188, -25.746])
tshwane_box = ee.Geometry.Rectangle([
    28.0, -25.9,  # Lower left
    28.4, -25.6   # Upper right
])

# Define the time period (last year)
end_date = datetime.now() - timedelta(days=1)  # Yesterday
start_date = end_date.replace(year=end_date.year - 1)  # One year ago

print(f"Fetching temperature data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

# Generate list of dates to process
dates_to_process = []
current_date = start_date
while current_date <= end_date:
    dates_to_process.append(current_date)
    current_date += timedelta(days=1)

# Process data day by day with progress bar
temperature_data = []
for date in tqdm(dates_to_process, desc="Processing days"):
    try:
        temp = get_daily_temp(date, tshwane_box)
        if temp is not None:
            temperature_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'tmax': round(temp, 2)
            })
        time.sleep(0.1)  # Small delay to avoid rate limiting
    except Exception as e:
        print(f"\nError processing {date.strftime('%Y-%m-%d')}: {str(e)}")
        continue

# Convert to pandas DataFrame
df = pd.DataFrame(temperature_data)
if len(df) > 0:
    df['date'] = pd.to_datetime(df['date'])
    # Format date as "DD Month YYYY"
    df['formatted_date'] = df['date'].dt.strftime('%d %B %Y')
    # Reorder columns to show formatted date first
    df = df[['formatted_date', 'tmax']]
    df = df.sort_values('formatted_date')
    
    # Save to Excel with better column names
    output_file = 'tshwane_temperatures.xlsx'
    df.columns = ['Date', 'Maximum Temperature (°C)']
    df.to_excel(output_file, index=False)
    print(f"\nData saved to {output_file}")
    
    # Print some basic statistics
    print("\nTemperature Statistics:")
    print(f"Data coverage: {len(df)} out of {len(dates_to_process)} days ({len(df)/len(dates_to_process)*100:.1f}%)")
    print(f"Average maximum temperature: {df['Maximum Temperature (°C)'].mean():.1f}°C")
    print(f"Highest maximum temperature: {df['Maximum Temperature (°C)'].max():.1f}°C on {df.loc[df['Maximum Temperature (°C)'].idxmax(), 'Date']}")
    print(f"Lowest maximum temperature: {df['Maximum Temperature (°C)'].min():.1f}°C on {df.loc[df['Maximum Temperature (°C)'].idxmin(), 'Date']}")
    
    # Create a visualization of the temperature trend
    print("\nCreating temperature visualization...")
    Map = geemap.Map()

    # Get the most recent temperature data
    recent_temp = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY') \
        .filterDate(
            end_date.strftime('%Y-%m-%d'),
            (end_date + timedelta(days=1)).strftime('%Y-%m-%d')
        ) \
        .select('temperature_2m') \
        .map(lambda image: image.subtract(273.15)) \
        .max()

    # Add the temperature layer to the map
    vis_params = {
        'min': 15,
        'max': 35,
        'palette': ['blue', 'white', 'red']
    }

    Map.centerObject(tshwane_center, 10)
    Map.add_layer(recent_temp.clip(tshwane_box), vis_params, 'Temperature (°C)')

    # Save the map
    Map.save('tshwane_temperature_map.html')
    print("Temperature map saved as 'tshwane_temperature_map.html'")
else:
    print("\nNo data was collected. Please check the error messages above.")
