
import pandas as pd
import pyproj
import numpy as np
import geopandas as gpd
from pyproj import CRS, Transformer

# Read the CSV file using pandas
gdf = pd.read_csv('./output/station_dictionary.csv')

# Define the input coordinate system
in_crs = CRS.from_epsg(4326)  # WGS84 CRS

# Define the output coordinate system
out_crs = CRS.from_string('+proj=lcc +lat_1=38 +lat_2=42 +lat_0=40 +lon_0=116.5 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs')

# Create a Transformer object for coordinate transformation
transformer = Transformer.from_crs(in_crs, out_crs, always_xy=True)

# Loop through each station
for index, row in gdf.iterrows():
    # Get the latitude and longitude values from the current row
    lat = row['lat']
    lon = row['lon']
    
    # Perform coordinate transformation
    x, y = transformer.transform(lon, lat)
    
    # Update the x and y coordinates in the GeoDataFrame
    gdf.at[index, 'x'] = x
    gdf.at[index, 'y'] = y


# Write the updated GeoDataFrame to the CSV file
print(gdf)
gdf.to_csv('output/station_dictionary.csv', index=False)

