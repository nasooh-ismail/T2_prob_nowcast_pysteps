"""

Author Name: Nasooh Ismail
Version: 1.0
Input: station_dictionary.csv
Output: obs_t2.csv, station_dictionary.csv(overwrite)
Update:
this script will extract daily data from the obs_t2.csv and save each days data in a seperate file with the file name <yyyymmdd>_t2_obs.csv
wriiten by nasooh for the project probilistic_nowcasting

"""

import pandas as pd
import numpy as np
from pytz import UTC
import os


df = pd.read_csv('./output/obs_t2.csv')
df = df.iloc[:, 1:]
start_date = pd.to_datetime('2020-07-28 16:00') #convert 2020/07/30 00:00 to UTC = 2020/07/28 16:00
end_date = start_date + pd.DateOffset(hours=767)
date_index = pd.date_range(start=start_date, end=end_date, freq='H')

# Assign the datetime index to the DataFrame
df.index = date_index

# Display the updated DataFrame
print(df.head())


# Create the output directory if it doesn't exist
output_dir = './output/obs_csv'
os.makedirs(output_dir, exist_ok=True)

# Convert the index to a pandas DatetimeIndex
df.index = pd.DatetimeIndex(df.index)

# Iterate over each day and save data for each station as a separate CSV file
for date in pd.DatetimeIndex(df.index):
    # Filter the DataFrame for the current date
    date_data = df[df.index.date == date]
    
    # Extract the year, month, and day for the file name
    year = str(date.year)
    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)
    
    # Generate the file name
    file_name = f'{year}{month}{day}_t2_obs.csv'
    
    # Create the full file path
    file_path = os.path.join(output_dir, file_name)
    
    # Save the data for the current date as a CSV file
    date_data.to_csv(file_path, index_label='valid_time')
