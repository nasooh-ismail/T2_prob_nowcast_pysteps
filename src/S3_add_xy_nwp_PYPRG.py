
import pandas as pd
import pyproj
import numpy as np

# Define the input and output coordinate systems
in_proj = pyproj.Proj(proj='latlong', datum='WGS84')
out_proj = pyproj.Proj(proj='lcc', lat_1=38, lat_2=42, lat_0=40, lon_0=116.5, x_0=0, y_0=0, datum='WGS84')

# Read the CSV file using pandas
df = pd.read_csv('./output/station_dictionary.csv')

x_arr = np.array([])
y_arr = np.array([])
# Loop through each row in the DataFrame
for index, row in df.iterrows():
    # Get the latitude and longitude values from the current row
    lat = float(row['lat'])
    lon = float(row['lon'])
    
    # Transform the coordinates to x and y in the output coordinate system
    x, y = pyproj.transform(in_proj, out_proj, lon, lat)
    
    # Assign the x and y coordinates to the specified columns
    x_arr = np.append(x_arr, x)
    y_arr = np.append(y_arr, y)


df.insert(4, "x", x_arr)
df.insert(5, "y", y_arr)

print(df)
# Write the updated DataFrame to the CSV file
df.to_csv('./output/station_dictionary.csv', index=False)
