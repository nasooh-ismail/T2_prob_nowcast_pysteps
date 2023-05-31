import xarray as xr
import matplotlib.pyplot as plt
import datetime

# Load the nc file
data = xr.open_dataset('./github_offline_test/output/nwp/T2_202008010000.nc')

# Extract the variables
T2 = data['T2']
lat = data['y']
lon = data['x']
time = data['t']

# Specify the desired date and time
desired_date = datetime.datetime(2020, 8, 1, 9, 0)

# Find the index of the desired date and time in the time array
desired_index = (time == desired_date).argmax()

# Extract the T2 values for the desired date and time
T2_desired = T2[desired_index]

# Plot the T2 values
plt.figure()
plt.pcolormesh(lon, lat, T2_desired, shading='auto', cmap='bwr')
plt.colorbar(label='T2')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title(f'T2 at {desired_date}')
plt.show()


import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np

# Open the nc file
dataset = nc.Dataset('./github_offline_test/output/siva/SIVA_T_202008010900+00000.nc')

# Assuming you have variables 'lat', 'lon', and 'data' in the nc file
# Replace them with the actual variable names in your nc file

# Read the latitude and longitude values
lat = dataset.variables['y'][:]
lon = dataset.variables['x'][:]

# Read the data variable
data = dataset.variables['T'][:]

# Close the nc file
dataset.close()

# Create a grid of latitude and longitude values
lon, lat = np.meshgrid(lon, lat)

# Plot the data
plt.contourf(lon, lat, data, cmap='bwr', shading='auto')

# Add colorbar
plt.colorbar()

# Add labels and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('T2 at 2020-08-01 09:00 siva_analysis')

# Show the plot
plt.show()
