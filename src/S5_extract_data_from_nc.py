import xarray as xr
import pandas as pd
from datetime import datetime, timedelta
import os
import glob
import numpy as np

# Path to the folder containing NWP NetCDF files
folder_path = './SIVA/'

# Path to the station dictionary CSV file
station_file_path = './station_dictionary.csv'

# Output folder
output_folder = './nwp_csv'

# Read the station dictionary CSV file
station_df = pd.read_csv(station_file_path)

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Get the list of NWP NetCDF files in the folder
nc_files = glob.glob(os.path.join(folder_path, '*.nc'))

# Loop through each NWP NetCDF file
for file_path in nc_files:
    # Open the NetCDF file
    dataset = xr.open_dataset(file_path)

    # Get the temperature data for all timesteps
    temperature = dataset['T2']

    # Get the time values
    timesteps = dataset['t']

    # Create a DataFrame to store the results
    result_df = pd.DataFrame({'valid_time': timesteps})

    # Iterate through each station in the station dictionary
    for idx, station_row in station_df.iterrows():
        station_id = station_row['station_id']
        target_lat = station_row['y']
        target_lon = station_row['x']

        # First, find the index of the grid point nearest a specific lat/lon.   
        abslat = np.abs(dataset.y - target_lat)
        abslon = np.abs(dataset.x - target_lon)
        c = np.maximum(abslon, abslat)
        xloc = np.where(c == np.min(c))
        yloc = np.where(c == np.min(c))
        # Extract the temperature values for the nearest grid point
        subset = dataset.sel(x=xloc, y=yloc)
        temperature_values = subset.T2
        #print(temperature_values)

        # Add the station's temperature values to the result DataFrame
        result_df[station_id] = temperature_values


    # Get the date and time from the NetCDF file name
    nc_file_name = os.path.basename(file_path)
    datetime_str = nc_file_name.split('_')[1].split('.')[0]
    nc_datetime = datetime.strptime(datetime_str, '%Y%m%d%H%M')

    # Add the run_time column to the result DataFrame
    result_df['run_time'] = nc_datetime

    # Rearrange the columns in the result DataFrame
    columns = ['valid_time', 'run_time'] + list(station_df['station_id'])
    result_df = result_df[columns]

    # Close the NetCDF file
    dataset.close()

   

    # Generate the output CSV file name
    output_file_name = nc_datetime.strftime('%Y%m%d%H%M') + '_t2_nwp.csv'

    # Save the result DataFrame to the output CSV file
    output_file_path = os.path.join(output_folder, output_file_name)
    result_df.to_csv(output_file_path, index=False)

    print(f"Output CSV file saved at: {output_file_path}")

