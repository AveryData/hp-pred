# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 15:29:33 2023

@author: avery
"""

import pandas as pd



df = pd.read_csv('eng_data.csv') #This is in seconds 


# Fix date
starter_date = "2018-04-26"
df['Date'] = starter_date
df['Date'] = pd.to_datetime(df['Date']) + pd.to_timedelta(df['Time'], unit='minutes')

df = df.iloc[::60,:]
df.to_csv('HourlyData.csv')