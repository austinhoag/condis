from datetime import datetime,timedelta
import pandas as pd
import numpy as np

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