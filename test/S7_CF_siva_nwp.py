
import pandas as pd
import numpy as np
import xarray as xr
import datetime as dt
from datetime import datetime
from pandas import to_datetime as to_datetime
import os
import re

""" #DEFINE THE TIME TO GET CF FOR
CF_spec_time = '2020-08-01 14:00'
CF_spec_time = datetime.strptime(CF_spec_time, '%Y-%m-%d %H:%M')
CF_spec_time

# Load station dictionary from CSV
station_df = pd.read_csv('./github_offline_test/output/station_dictionary.csv')

# Create a DataFrame to store the results
results_df = pd.DataFrame({'station_id': station_df['station_id']})

# Loop through the nc files
for nc_file in [
    './github_offline_test/output/siva/SIVA_T_202008010900+00000.nc',
    './github_offline_test/output/siva/SIVA_T_202008011000+00000.nc',
    './github_offline_test/output/siva/SIVA_T_202008011100+00000.nc',
    './github_offline_test/output/siva/SIVA_T_202008011200+00000.nc',
    './github_offline_test/output/siva/SIVA_T_202008011300+00000.nc',
    './github_offline_test/output/siva/SIVA_T_202008011400+00000.nc'
]:
    # Load the nc file using xarray
    ds = xr.open_dataset(nc_file)
    
    # Loop through each station in the station dictionary
    for _, station in station_df.iterrows():
        lat = station['y']
        lon = station['x']
        station_id = station['station_id']
        
        # Get the T value for the specific lat and lon from the nc file
        t_value = ds['T'].sel(y=lat, x=lon, method='nearest').values.item()
        
        # Add the T value to the results DataFrame
        results_df.loc[results_df['station_id'] == station_id, nc_file] = t_value
    
    # Close the nc file
    ds.close()

# Calculate the average of each T value for each station
results_df['average'] = results_df.iloc[:, 1:].mean(axis=1)

# Print the results DataFrame
print(results_df['average'].describe())

#results_df.to_csv('./siva.csv')
 """

 #### ADD A PART TO CLEAN RESULT DF BY REMOVING OTHER COLUMNS AND TRASNPOSING AND ADDING THE TIMESTEOPS TO 1ST COLUM 2ND ROW

#open  csv files
nwp_input = pd.read_csv('./github_offline_test/output/nwp_csv/202008010000_t2_nwp.csv')
siva_input = pd.read_csv('./github_offline_test/output/siva/siva.csv')
station_dictionary = pd.read_csv('./github_offline_test/output/station_dictionary.csv')
#assign empty arrays to fill in for calcualuted CF for each station
CF_array = np.array([])


station_id = station_dictionary['station_id']
for x, id in enumerate(station_id):
        # extract temperatures from each station ID for OBS
        siva = siva_input['%s' % id]
        #obs = y[start_obs_time:end_obs_time]
        #obs = obs.mean()
        # extract temperatures from each station ID for NWP
        z = nwp_input['%s' % id]
        nwp = z[14]
        #compute CF and fill empty array 
        CF = siva-nwp
        CF_array = np.append(CF_array, CF)

#create a dataframw with only station_id, lat and lon
CF_df = station_dictionary
# Remove column name 'A'
CF_df = CF_df.drop(['alt', 'x', 'y'], axis=1)
CF_df.insert(1, "CF", CF_array)
print(CF_df['CF'].describe())

#CF_df.to_csv('./github_offline_test/output/CF_siva_nwp.csv')
