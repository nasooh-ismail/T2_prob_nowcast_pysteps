import pandas as pd
import numpy as np
import xarray as xr
import datetime as dt
from datetime import datetime
from pandas import to_datetime as to_datetime
import os
import re

#open obs csv and set a datetime index (UTC)
obs_input = pd.read_csv('/Users/nasoohismail/T2_prob_nowcast_pysteps/data/obs/obs_t2.csv')
start_date = pd.to_datetime('2020-07-28 16:00') #convert 2020/07/30 00:00 to UTC = 2020/07/28 16:00
end_date = start_date + pd.DateOffset(hours=767)
date_index = pd.date_range(start=start_date, end=end_date, freq='H')
obs_input = obs_input.set_index(date_index)

#open nwp csv
nwp_input = pd.read_csv('/Users/nasoohismail/T2_prob_nowcast_pysteps/data/nwp/202008010000_t2_nwp.csv')


#open staioon_dictionary
station_dictionary = pd.read_csv('/Users/nasoohismail/T2_prob_nowcast_pysteps/data/obs/station_dictionary.csv')

#DEFINE THE TIME TO GET CF FOR
CF_spec_time = '2020-08-01 14:00'
CF_spec_time = datetime.strptime(CF_spec_time, '%Y-%m-%d %H:%M')
CF_spec_time



#define time for obs
start_obs_time = CF_spec_time - pd.DateOffset(hours = 5) #to get mean of the previous six hours
end_obs_time = CF_spec_time
#define times for nwp #no need to get mean of 6 hours for nwp
nwp_time =  CF_spec_time


#assign empty arrays to fill in for calcualuted CF for each station
CF_array = np.array([])

y = obs_input['54638']
y = y[start_obs_time:end_obs_time]
y = y.mean()

z = nwp_input['54638']
z = z[14] #at 14:00 08/01




station_id = station_dictionary['station_id']
for x, id in enumerate(station_id):
        # extract temperatures from each station ID for OBS
        y = obs_input['%s' % id]
        obs = y[start_obs_time:end_obs_time]
        obs = obs.mean()
        # extract temperatures from each station ID for NWP
        z = nwp_input['%s' % id]
        nwp = z[14]
        #compute CF and fill empty array 
        CF = obs-nwp
        print(CF)
        CF_array = np.append(CF_array, CF)

#create a dataframw with only station_id, lat and lon
CF_df = station_dictionary
# Remove column name 'A'
CF_df = CF_df.drop(['alt', 'x', 'y'], axis=1)
CF_df.insert(1, "CF", CF_array)
print(CF_df)
CF_df.to_csv('/Users/nasoohismail/T2_prob_nowcast_pysteps/test/CF.csv')