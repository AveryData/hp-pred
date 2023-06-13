# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 16:15:24 2023

@author: avery
"""

import streamlit as st 
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide")
import plotly.graph_objects as go
from prophet import Prophet
from pandas import to_datetime
import ruptures as rpt
import numpy as np



df = pd.read_csv('HourlyData.csv')

# start = 0
# end  = len(df)
# starting_pt = 3000
# ending_pt = 13000


col11, col22 = st.columns(2)
with col11:
    st.title("Continuous Oil Tank Hydraulic System Monitoring App 🏭")

with col22:
    st.info('''This app assists industrial systems run more efficiently by
            detecting significant changes in operating conditions & predicting
            future values using machine learning. Start by selecting a column
            of interest, selecting how far in the future you want to predict,
            and how sensitive to changes you'd like to search for.
            ''', icon="ℹ️")


col1, col2, col3 = st.columns(3)

with col1: 
    option = st.selectbox(
        'What variable is of interest?',
        (df.columns[2:-1]))


with col2: 
    future_minute = st.slider('How far in the future should we predict? (Hours)', 5, 2205, 168)
    
    
with col3: 
    rpt_aggression = st.slider('How sensitive to changes do we want to be? 1 = very sensitive', 1, 10, 5)

#df = df.loc[min_idx:max_idx,:]
df = df[["Date", option]]
df.columns = ['ds','y']
df['ds']= to_datetime(df['ds'], format='mixed')




y_data = df['y']

# from statsmodels.tsa.arima.model import ARIMA
# model = ARIMA(y_data, order=(5,1,0))
# model_fit = model.fit()
# output = model_fit.forecast()[0]



model = Prophet()
model.add_seasonality(name='minutely', period=2205, fourier_order=7)
model.fit(df)


# Graph the original data 
fig = px.line( x=df["ds"], y=df["y"], title=option)




future_dates = []
for i in range(0,future_minute-1):
    future_dates.append(df.iloc[-1,0] +  pd.to_timedelta(i, unit='hour'))
    

future_dates_series = pd.DataFrame(future_dates)
future_dates_series.columns = ["ds"]
forecast = model.predict(future_dates_series)

# add all the traces
fig.add_trace(go.Scatter(
    name = 'prediction',
    mode = 'lines',
    x = list(future_dates),
    y = list(forecast['yhat']),
    line= dict(color='green')
))


fig.add_trace(go.Scatter(
    name= 'lower band',
    mode = 'lines',
    x = list(future_dates),
    y = list(forecast['yhat_lower']),
    line= dict(color='#1705ff'),
))

fig.add_trace(go.Scatter(
    name = 'upper band',
    mode = 'lines',
    x = list(future_dates),
    y = list(forecast['yhat_upper']),
    line= dict(color='#1705ff'),
    fill = 'tonexty'
))




# Highlight all the chane points
algo = rpt.Pelt(model="rbf").fit(np.array(df["y"].tolist()))
result = algo.predict(pen=rpt_aggression)
for i in result:
    fig.add_vline(x=df["ds"][i-1], line_width=2, line_dash="dash", line_color="red")
    
    
fig.update_layout(
    xaxis_title="Date")


st.plotly_chart(fig, use_container_width=True)

st.error('''Significant changes are shown with dashed red lines.
         Future values are shown with a green line, with an upper and lower 
         confidence interval. The futher in the future you predict, the more
         uncertain the predictions become.''', icon="📊")
