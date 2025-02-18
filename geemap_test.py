import ee
import geemap

try:
    # Initialize Earth Engine
    ee.Initialize()
    
    # Create a map
    Map = geemap.Map()
    
    # Add a simple dataset to verify access
    dem = ee.Image('USGS/SRTMGL1_003')
    Map.addLayer(dem, {'min': 0, 'max': 4000}, 'SRTM DEM')
    
    print("Successfully connected to Earth Engine and loaded data!")
    
except Exception as e:
    print("Error:")
    print(str(e))
