import ee
import geemap

try:
    # Initialize Earth Engine
    ee.Initialize()
    print("Earth Engine initialized successfully!")
    
    # Test the connection by getting some data
    # Get a Landsat image
    image = ee.Image('LANDSAT/LC08/C02/T1_TOA/LC08_044034_20140318')
    print("\nSuccessfully retrieved a Landsat image!")
    
    # Create an interactive map
    Map = geemap.Map()
    Map.add_layer(image, {'bands': ['B4', 'B3', 'B2'], 'max': 0.3}, 'Landsat image')
    Map.centerObject(image, 8)
    
    # Save the map
    Map.save("test_map.html")
    print("\nMap saved as 'test_map.html'")
    
except ee.EEException as e:
    print("\nError: Earth Engine authentication required!")
    print("Please run the following command to authenticate:")
    print("\nee.Authenticate()")
    
    # Try to authenticate
    try:
        ee.Authenticate()
        print("\nAfter authentication, please run this script again.")
    except Exception as auth_error:
        print(f"\nAuthentication error: {auth_error}")
        print("Please make sure you have a Google Earth Engine account.")
        print("Sign up at: https://signup.earthengine.google.com/")
        
except Exception as e:
    print(f"\nUnexpected error: {e}")
    print("Please make sure you have the required packages installed:")
    print("pip install earthengine-api geemap")
