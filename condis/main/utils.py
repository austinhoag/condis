from datetime import datetime,timedelta
import pandas as pd
import numpy as np
import requests
from functools import reduce
time_format = '%-I %p' # e.g. "4 AM"

def hit_grid_api(**grid_params):
    """ Make GET request to weather API gridpoints endpoint
    To retrieve times within the grid_params"""
    grid_id = grid_params['grid_id']
    grid_x  = grid_params['grid_x']
    grid_y  = grid_params['grid_y']
    min_temp = grid_params['min_temp']
    max_temp = grid_params['max_temp']
    min_humidity = grid_params['min_humidity']
    max_humidity = grid_params['max_humidity']
    min_precip = grid_params['min_precip']
    max_precip = grid_params['max_precip']
    min_time = grid_params['min_time']
    max_time = grid_params['max_time']
    response = requests.get(f'https://api.weather.gov/gridpoints/{grid_id}/{grid_x},{grid_y}')
    # Handle bad responses from the weather API
    if response.status_code != 200:
        return response.status_code
    # Convert response to python dict
    j=response.json()
    # Get all properties and then extract the ones I will use
    properties=j['properties']
    temp_dicts=properties['temperature']
    hum_dicts=properties['relativeHumidity']
    precip_dicts=properties['probabilityOfPrecipitation']
    
    def calc_msr_duration(x):
        duration_str = str(x).split('P')[-1]
        if "D" in duration_str:
            n_days = int(duration_str[0])
            if 'H' in duration_str:
                n_hours = int(duration_str.split("T")[-1].split('H')[0])
            else:
                n_hours = 0
            n_hours += n_days*24
        else:
            n_hours = int(str(x).split('PT')[-1].split('H')[0])
        return n_hours

    def init_temp_df():
        temp_lists=temp_dicts['values']
        df_temp=pd.DataFrame(temp_lists)
        df_temp['temp_f']=df_temp['value']*9/5.+32
        df_temp['timestamp']=pd.to_datetime(df_temp['validTime'].map(lambda x: str(x).split('+')[0]))
        # set to local time from UTC (default)
        df_temp['timestamp']-=timedelta(hours=4)
        df_temp['msr_duration']=df_temp['validTime'].map(lambda x: calc_msr_duration(x))
        df_temp.drop(['validTime','value'],axis=1,inplace=True)
        df_temp = df_temp[['timestamp','msr_duration','temp_f']]
        return df_temp

    def init_hum_df():
        hum_lists=hum_dicts['values']
        df_hum=pd.DataFrame(hum_lists)
        df_hum['relativeHumidity'] = df_hum['value']
        df_hum['timestamp']=pd.to_datetime(df_hum['validTime'].map(lambda x: str(x).split('+')[0]))
        # set to local time from UTC (default)
        df_hum['timestamp']-=timedelta(hours=4)
        df_hum['msr_duration']=df_hum['validTime'].map(lambda x: calc_msr_duration(x))
        df_hum.drop(['validTime','value'],axis=1,inplace=True)
        df_hum = df_hum[['timestamp','msr_duration','relativeHumidity']]
        return df_hum

    def init_precip_df():
        precip_lists=precip_dicts['values']
        df_precip=pd.DataFrame(precip_lists)
        df_precip['probabilityOfPrecipitation'] = df_precip['value']
        df_precip['timestamp']=pd.to_datetime(df_precip['validTime'].map(lambda x: str(x).split('+')[0]))
        # set to local time from UTC (default)
        df_precip['timestamp']-=timedelta(hours=4)
        df_precip['msr_duration']=df_precip['validTime'].map(lambda x: calc_msr_duration(x))
        df_precip.drop(['validTime','value'],axis=1,inplace=True)
        df_precip = df_precip[['timestamp','msr_duration','probabilityOfPrecipitation']]
        return df_precip

    # initialize all dataframes
    df_temp = init_temp_df()
    df_hum = init_hum_df()
    df_precip = init_precip_df()
    # Expand all dataframes
    df_temp_expanded = expand_dataframe(df_temp)
    df_hum_expanded = expand_dataframe(df_hum)
    df_precip_expanded = expand_dataframe(df_precip)
    # Merge all three 
    dfs = [df_temp_expanded,df_hum_expanded,df_precip_expanded]
    df_final = reduce(lambda left,right: pd.merge(left,right,on='timestamp'), dfs)
    # Only show future times
    now = datetime.now()
    future_mask = df_final['timestamp']>now
    df_final = df_final[future_mask]
    # Now mask the forecast based on the user input
    temp_mask = (df_final['temp_f'] >= min_temp) & (df_final['temp_f'] <= max_temp)
    hum_mask = (df_final['relativeHumidity'] >= min_humidity) & (df_final['relativeHumidity'] <= max_humidity) 
    precip_mask = (df_final['probabilityOfPrecipitation'] >= min_precip) & \
        (df_final['probabilityOfPrecipitation'] <= max_precip)
    time_mask = df_final['timestamp'].dt.strftime('%H:%M').between(min_time,max_time)
    good_condis_mask = (temp_mask) & (hum_mask) & (precip_mask) & (time_mask)
    df_good_condis = df_final[good_condis_mask]
    if len(df_good_condis) == 0:
        return []
    # Split up into groups by neighboring hours
    groups=splitme_zip(np.array(df_good_condis.index),d=1)
    all_print_strs = []
    for group in groups:
        mask = df_good_condis.index.isin(group)
        group_df = df_good_condis[mask]
        if len(group) > 1:
            first_timestamp = group_df['timestamp'].iloc[0]
            first_weekday = first_timestamp.day_name()
            first_date = first_timestamp.date().strftime('%m/%d/%Y')
            first_time = first_timestamp.time() 
            last_timestamp = group_df['timestamp'].iloc[-1]
            last_timestamp += timedelta(hours=1)
            last_weekday = last_timestamp.day_name()
            last_date = last_timestamp.date().strftime('%m/%d/%Y')
            last_time = last_timestamp.time() 

            if first_date == last_date:
                print_str = f"{first_weekday}, {first_date}, from {first_time.strftime(time_format)} to {last_time.strftime(time_format)} "
            else:
                print_str = (f"From {first_time.strftime(time_format)} on {first_weekday},"
                            f" {first_date} to {last_time.strftime(time_format)} on {last_weekday}, {last_date} ")
        else:
            """ Give as a range from hour X to hour X+1 """
            timestamp = group_df['timestamp'].iloc[0]
            first_weekday = timestamp.day_name()
            first_date = timestamp.date().strftime('%m/%d/%Y')
            first_time = timestamp.time()

            next_timestamp = timestamp + timedelta(hours=1)
            next_weekday = next_timestamp.day_name()

            next_date = next_timestamp.date().strftime('%m/%d/%Y')
            next_time = next_timestamp.time()        
            if first_date == next_date:
                print_str = f"{first_weekday}, {first_date}, from {first_time.strftime(time_format)} to {next_time.strftime(time_format)} "
            else:
                print_str = (f"From {first_time.strftime(time_format)} on {first_weekday},"
                            f" {first_date} to {next_time.strftime(time_format)} on {next_weekday}, {next_date} ")  
        all_print_strs.append(print_str)
    return all_print_strs

def expand_dataframe(df):
    """For any rows where the duration of the measurement
    is over more than one hour, make a new row duplicate row 
    (but with incremented timestamp) for each hour in the duration"""
    dfc = df.copy() # makes a copy so the original is not affected
    mask = dfc['msr_duration'] > 1
    n_rows_multiple_durations = len(dfc[mask]) # variable to store the number of rows where the measurement stands for multiple hours
    counter = 0
    while n_rows_multiple_durations > 0:
        # Make a new dataframe that is just the rows with multiples
        new_dfc = dfc.loc[mask].copy()
        # set all of the masked rows in the original dataframe to 1 since we will combine back with this dfc in the end
        dfc['msr_duration'][mask]=1
        # In this new dataframe, increment the timestamp by 1 hour and decrement the msr_duration by 1 hour
        new_dfc['timestamp'] += timedelta(hours=1)
        new_dfc['msr_duration']-=1
        # concatenate this new dfc that we have transformed back with the original, and overwrite the original
        dfc = pd.concat([dfc,new_dfc])
        # calculate the new mask of multiples on this concatenated array
        mask = dfc['msr_duration'] > 1
        n_rows_multiple_durations = len(dfc[mask])
        counter+=1
    # Finally sort by timestamp so the rows fall back in order
    dfc = dfc.sort_values('timestamp')
    # set the index to a proper increasing numerical index without duplicates
    dfc.index = list(range(len(dfc)))
    dfc.drop(['msr_duration'],axis=1,inplace=True)
    return dfc

def splitme_zip(a,d):
    """ 
    Given an array (a), make a list of lists
    where each sublist is the array elements that 
    are closer than or equal to d in numerical value. 

    Only really useful if array is sorted
    
    a: numpy array
    d: tolerable gap between elements
    """
    m = np.concatenate(([True],a[1:] > a[:-1] + d,[True]))
    idx = np.flatnonzero(m)
    l = a.tolist()
    return [l[i:j] for i,j in zip(idx[:-1],idx[1:])]