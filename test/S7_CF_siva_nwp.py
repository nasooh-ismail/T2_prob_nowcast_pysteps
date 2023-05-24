

import pandas as pd
import xarray as xr

# Load station dictionary from CSV
station_df = pd.read_csv('/Users/nasoohismail/T2_prob_nowcast_pysteps/data/obs/station_dictionary.csv')

# Create a DataFrame to store the results
results_df = pd.DataFrame({'station_id': station_df['station_id']})

# Loop through the nc files
for nc_file in [
    '/Users/nasoohismail/T2_prob_nowcast_pysteps/data/nwp_grids/siva_ana/SIVA_T_202008010900+00000.nc',
    '/Users/nasoohismail/T2_prob_nowcast_pysteps/data/nwp_grids/siva_ana/SIVA_T_202008011000+00000.nc',
    '/Users/nasoohismail/T2_prob_nowcast_pysteps/data/nwp_grids/siva_ana/SIVA_T_202008011100+00000.nc',
    '/Users/nasoohismail/T2_prob_nowcast_pysteps/data/nwp_grids/siva_ana/SIVA_T_202008011200+00000.nc',
    '/Users/nasoohismail/T2_prob_nowcast_pysteps/data/nwp_grids/siva_ana/SIVA_T_202008011300+00000.nc',
    '/Users/nasoohismail/T2_prob_nowcast_pysteps/data/nwp_grids/siva_ana/SIVA_T_202008011400+00000.nc'
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
print(results_df)

#results_df.to_csv('test.csv')
