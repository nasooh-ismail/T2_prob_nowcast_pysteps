# T2_prob_nowcast_pysteps

This is a project to do a probabilistic nowcast for 2meter temperature for the hubei reigion

explanation of directories / files are named as follows:

src/ (contains python scripts to generate all the CSV files)

S1_station_dictionary_and_t2_extractt.py
  generates a concated csv called obs_t2.csv based on the shape(how many timesteps of data available) from the raw obs data files and generates a station_dictionary
  
S2_clean_obs_t2_and_station_dictionary.py
  further cleans the obs_t2.csv
  replaces 99999.0 and -45 values with Nan
  remeoves stations with more then 48 timesteps of Nan present in it
  updated the station_dictionary with the removed stations
  
S3_add_xy_nwp_GPDS.py
  adds the projected x and y cordinate to the station dictionary by using geopandas with the specifications from geo_siva.nc file
  
S3_add_xy_nwp_PYPRG.py
  does the same thing as the previous script but used pyproj libaray
  
S4_extract_dailydata_from_obs_t2.py
  extracts each days temperature from the obs_t2.csv, and saves each days csv seperately

S5_extract_data_from_nc.py
  extracts temperature from each nc file for all the stations and generates a csv seperatly for each file


notebook/ (cotainsnjupyter notebooks to generate plots/CF feilds)

S6_get_station_timeseries_plot.ipynb
  plots a timeseries for one station using the csv data files

data/ (containsthe data files)
data/obs (contains obs csv files)
station_dictionary.csv
  contains all the metadata (station_id,lat,lon,x,y,alt) for all the stations
t2_obs.csv
  a concated csv which contains temperature for all timesteps anf for all stations
yyyymmdd_obs_t2.csv files
  one file for each day 

data/nwp (contains forecast nwp csv files)
yyyymmddHHMM_nwp_t2.csv files
  each file for each nwp output nc files (HHMM is the run time for specifc file)

data/nwp_obs (is an empty directory for now)

test/ (contains scripts to test, is empty for now)

run/ (contains bash files for software development, is empty for now)





