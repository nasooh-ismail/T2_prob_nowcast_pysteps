"""

Author Name: Nasooh Ismail
Version: 1.0
Input: obs_t2.csv, station_dictionary.csv
Output: obs_t2.csv, station_dictionary.csv(overwrite)
Update:
as the original T2 data set has a lot of missin or error values , we need to clean and remove the stations with more than X timestamps 
missing or error, and overwrite the obs_t2.csv file, and remove the stations from station_dictionary.csv file so both of the files will have
the same station_id's

"""

import pandas as pd
import numpy as np

df = pd.read_csv('./output/obs_t2.csv')
df = df.iloc[:, 1:]

# df contains 99999.0 and -45 values and missing values
df = df.replace([99999.0, -45], np.nan)

# Count occurrences of "9999", "-45", and missing values in each station
count_dict = {}
for column in df.columns:
    missing_count = df[column].isna().sum()
    err_count = df[column].isin([99999.0, -45]).sum()
    count_dict[column] = {'missing_count': missing_count, 'err_count': err_count}

# Set condition for more than 48 hours of missing or wrong data
threshold = 48
stations_exceeding_threshold = [station for station, count in count_dict.items()
                                if count['missing_count'] + count['err_count'] > threshold]

# Print the list of station names and the count of stations exceeding the threshold
#print("Stations exceeding the threshold:")
#for station in stations_exceeding_threshold:
#    print(station)
#num_stations_exceeding_threshold = len(stations_exceeding_threshold)
#print("Total number of stations exceeding the threshold:", num_stations_exceeding_threshold)

# Remove stations exceeding the threshold from the DataFrame
df = df.drop(stations_exceeding_threshold, axis=1)

# Calculate basic statistics for each station
#station_statistics = df.describe()
# Print the basic statistics for each station
#print("Basic statistics for each station:")
#print(station_statistics)

#after the stations have been removed we start to fill in the data set 
# Fill missing values with the mean of the values above and below
df_filled = df.copy()  # Create a copy of the DataFrame
for column in df_filled.columns:
    column_values = df_filled[column].values
    is_missing = np.isnan(column_values)
    
    prev_value = np.nan
    for i in range(len(column_values)):
        if is_missing[i]:
            # Find the next non-missing value
            j = i + 1
            while j < len(column_values) and is_missing[j]:
                j += 1
            # Fill missing values with the mean of the previous and next non-missing values
            if prev_value is np.nan and j == len(column_values):
                # Handle case where missing values are at the beginning and end
                df_filled[column].fillna((column_values[j - 1] + column_values[0]) / 2, inplace=True)
            elif prev_value is np.nan:
                # Handle case where missing values are at the beginning
                df_filled[column].fillna(column_values[j], inplace=True)
            elif j == len(column_values):
                # Handle case where missing values are at the end
                df_filled[column].fillna(prev_value, inplace=True)
            else:
                # Fill missing values with the mean of the previous and next non-missing values
                df_filled[column].fillna((prev_value + column_values[j]) / 2, inplace=True)
        else:
            # Update the previous non-missing value
            prev_value = column_values[i]

# Print the updated DataFrame with statistics
#print("DataFrame with filled missing values:")
#print(df_filled)
# Calculate basic statistics for each station
#station_statistics = df_filled.describe()
# Print the basic statistics for each station
#print("Basic statistics for each station:")
#print(station_statistics)

#overwrite obs_t2.csv
df_filled.to_csv('./output/obs_t2.csv')

########################################################################

#after we get a clean t2 dataset, we make the station dictionary have the same station_ids as new df
station_dict = pd.read_csv("./output/station_dictionary.csv")

# Get the list of station IDs that were removed in df_fillled and remove the rows
removed_station_ids = stations_exceeding_threshold
station_dict_filtered = station_dict[~station_dict['station_id'].isin(removed_station_ids)]
station_dict_filtered = station_dict_filtered.iloc[:, 1:]  # Remove the first column

#print statistics and check if they both a the same
#print(station_dict_filtered['station_id'].describe())
#print(df_filled.describe())

# overwrite the station_dictionary.csv
station_dict_filtered.to_csv("./output/station_dictionary.csv", index=False)