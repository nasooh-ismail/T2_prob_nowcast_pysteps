"""
Author Name: Kevin Junior
Co-Author: Nasooh Ismail
Project: Weather Forecast Data extraction from Weather Stations in Hubei
Input: raw obs files in /obs_data/yyyymmddHHMMSS.csv , stationshape.csv(contains shape of all the stations)
Output: 'user_entered'.csv(unfiltered station_dictionary), station_dictionary.csv(filtered), obs_t2.csv
Version: 1.4
Update:
1.0 -->
Basic data extraction from each of the station sensor data, extracting time, temp and station id
1.1 -->
Added ability to select the number of 'unique' stationid to be extracted through the number
of timesteps available
1.2 -->
Added the ability to extract station id with the lat and lon
1.3 -->
Added config file to extract different types of columns from the original dataset
Added Simple Bash UI
1.4 -->
Added the ability to filter out stations based on the given lat and lon limits (through config)
Combined both temp and column extraction program.
"""

import array
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pyproj import CRS, Transformer

# Input Files
obs_data_path = ('./input/obs_data/')

# config
limit = 720 #number of timesteps available in the station
extract_col = ['station_id', 'lat', 'lon', 'alt'] # Column names to be extracted
lat_uplimit = 42.7 #upper limit for latitude
lat_lowlimit = 37.4 #lower limite for latitude
lon_uplimit = 119.4 #upper limit for longitude
lon_lowlimit = 113.2 #lower limite for longitude
start_time_temp = '2020-07-29'
end_time_temp = '2020-08-30'

def extract_unique_id(x):

    filter_df = x

    #extract only the unique ID into a new dataframe column
    unique_id = filter_df['station_id']
    unique_id = unique_id.reset_index(drop=True)
    print(unique_id)
    print(unique_id.describe)

    #check for any duplicates in unique ID
    print(unique_id.duplicated().sum())

    #convert the unique id from dataframe into series
    unique_id_series = unique_id.squeeze()
    return unique_id_series

def station_col():
  
    #read in stationshape.csv
    stremove_df = pd.read_csv('./input/stationshape.csv')
    #print(df)
    print(stremove_df)

    # Extract unique station ID
    print(stremove_df['shape'].describe())
    filter_df = stremove_df.loc[stremove_df['shape'] >= limit]
    print(filter_df)

    #extract only the unique ID into a new dataframe column
    #convert the unique id from dataframe into series
    unique_id_series = extract_unique_id(filter_df)

    # concat all data files and Add time stamp to the concat data
    time_list = pd.date_range(start='2020-07-29', end='2020-07-29 00:01:00', freq='1H')
    time_list_str = time_list.strftime('%Y%m%d%H00')

    all_data_frames = pd.DataFrame(columns=extract_col)
    print(all_data_frames)

    # Loop to extract all the
    for sttime in time_list_str:
        if (os.path.exists(obs_data_path + sttime + '.csv')) and sttime == '202007290000':
            df = pd.read_csv(obs_data_path + sttime + '.csv')
            for x, id in enumerate(unique_id_series):
                if (df['station_id'] == id).any():
                    df_filter = df.loc[df['station_id'] == id, extract_col]
                    # ADD BLOCK TO SELECT SET OF SELECTED STATIONS
                    #print(df_filter)
                    all_data_frames.loc[x] = df_filter.squeeze()
                    #print(all_data_frames)
                else:
                    all_data_frames.loc[x] = (id, np.NaN, np.NaN, np.NaN)

        elif (os.path.exists(obs_data_path + sttime + '.csv')):
            df = pd.read_csv(obs_data_path + sttime + '.csv')
            #print(all_data_frames)
            # create a temporary storage space for t2
            col_temp = pd.DataFrame(columns=extract_col)
            for x, id in enumerate(unique_id_series):
                if (df['station_id'] == id).any():
                    df_filter2 = df.loc[df['station_id'] == id, extract_col]
                    # ADD BLOCK TO SELECT SET OF SELECTED STATIONS
                    #print(df_filter2.describe)
                    col_temp = pd.concat([col_temp, df_filter2], ignore_index=True)
                    #print(t2_temp)
                else:
                    col_temp.loc[x] = (id, np.NaN, np.NaN, np.NaN)
            #add temp to new column in all data frames
            all_data_frames = pd.concat([all_data_frames, col_temp], axis=0, ignore_index=True)

        else:
            break

    # Save Prompt
    print(all_data_frames)
    save_con = input("Do you want to save this Dataframe? (Y/N)")
    if save_con == 'Y'.casefold():
        save_file_name = input("Please input filename: ")
        if type(save_file_name) == str:
            date_time_con = input("Do you want to include date-time? (Y/N)")
            if date_time_con == 'Y'.casefold():
                all_data_frames.to_csv(save_file_name + '{}.csv'
                                       .format(pd.datetime.now().strftime("%Y-%m-%d %H%M%S")))
            elif date_time_con == 'N'.casefold():
                all_data_frames.to_csv(save_file_name + '.csv')
            else:
                Exception("An error has occured in the input."
                          "Please check your input")
                return TypeError
        else:
            Exception("An error has occured in the input."
                      "Please check your input")
            return TypeError
    elif save_con == 'N'.casefold():
        print("You have chosen not to save. The program will now close.")
    else:
        Exception("An error has occured in the input."
                  "Please check your input")
        return TypeError

    return all_data_frames

def temp_extract(x):
    # get unique station id input for the extraction process
    filter_df = x

    unique_id_series = extract_unique_id(x)

    # concat all data files and Add time stamp to the concat data
    time_list = pd.date_range(start=start_time_temp, end=end_time_temp, freq='1H')
    time_list_str = time_list.strftime('%Y%m%d%H00')

    all_data_frames = pd.DataFrame(columns=['station_id', 'T2'])
    print(all_data_frames)

    for sttime in time_list_str:
        if (os.path.exists(obs_data_path + sttime + '.csv')) and sttime == '202007290000':
            df = pd.read_csv(obs_data_path + sttime + '.csv', usecols=['station_id', 'T2'])
            for x, id in enumerate(unique_id_series):
                if (df['station_id'] == id).any():
                    df_filter = df.loc[df['station_id'] == id, ['station_id', 'T2']]
                    # ADD BLOCK TO SELECT SET OF SELECTED STATIONS
                    #print(df_filter)
                    all_data_frames.loc[x] = df_filter.squeeze()
                    #print(all_data_frames)
                else:
                    all_data_frames.loc[x] = (id, np.NaN)

        elif (os.path.exists(obs_data_path + sttime + '.csv')):
            df = pd.read_csv(obs_data_path + sttime + '.csv', usecols=['station_id', 'T2'])
            #print(all_data_frames)
            # create a temporary storage space for t2
            t2_temp = pd.DataFrame(columns=['T2'])
            for id in unique_id_series:
                df_filter2 = df.loc[df['station_id'] == id, ['T2']]
                # ADD BLOCK TO SELECT SET OF SELECTED STATIONS
                #print(df_filter2.describe)
                t2_temp = pd.concat([t2_temp, df_filter2], ignore_index=True)
                #print(t2_temp)

            #add temp to new column in all data frames
            all_data_frames = pd.concat([all_data_frames, t2_temp], axis=1, ignore_index=True)

        else:
            #all_data_frames.to_csv('t2data.csv')
            break

    print(all_data_frames)
    return all_data_frames

def main():
    # Run extract station unique id with required columns
    station_col_df = station_col()
    print(f'stationcol station: \n{station_col_df}')

    # Remove all latitudes and longitudes outside of the range
    filtered_station = station_col_df[(station_col_df['lat'] >= lat_lowlimit) & (station_col_df['lat'] <= lat_uplimit)
    & (station_col_df['lon'] >= lon_lowlimit) & (station_col_df['lon'] <= lon_uplimit)]

    print(f'filtered station: \n{filtered_station}')

    filtered_station.to_csv('station_dictionary.csv')
    print('filtered_station_id successfully saved\n\n')

    # Use the unique_id from the filtered station to use as
    t2_station_df = temp_extract(filtered_station)

    # transpose the t2 dataframe
    t2_station_df_trans = t2_station_df.transpose()
    print(t2_station_df_trans)

    # make the station id as the column header
    headers = t2_station_df_trans.iloc[0]
    t2_station_df_trans_new = pd.DataFrame(t2_station_df_trans.values[1:], columns=headers)

    # Export transposed to another file
    t2_station_df_trans_new.to_csv('obs_t2.csv')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
