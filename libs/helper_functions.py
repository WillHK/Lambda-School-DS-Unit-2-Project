from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import os

import plotly.offline as py_off
from plotly.graph_objs import *

import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import matplotlib.pyplot as plt
import pickle

home_values = pd.read_csv('Zip_Zhvi_AllHomes.csv', encoding="ISO-8859-1")
zip_lat_lng = pd.read_csv("https://gist.githubusercontent.com/erichurst/7882666/raw/5bdc46db47d9515269ab12ed6fb2850377fd869e/US%2520Zip%2520Codes%2520from%25202013%2520Government%2520Data")

def prophet_prediction(row, zip_code, retirement_date='2029'):
    # if os.path.exists('pickles/{}_forecast.pkl'.format(zip_code)):
    # with open("pickles/{}_model.pkl".format(zip_code), 'rb') as f:
    #     unpickler = pickle.Unpickler(f)
    #     m = unpickler.load()
    m = Prophet(seasonality_mode='multiplicative')
    row = row[(row['ds'] > '2009')]
    m.fit(row)
    forecast = pd.read_pickle('pickles/{}_forecast.pkl'.format(zip_code))
    forecast = forecast[(forecast['ds'] > '2009') and (forecast['ds'] < str(retirement_date))] 
    return plot_plotly(m, forecast)
    # else
    #     m = Prophet(seasonality_mode='multiplicative')
    #     m.fit(row)
    #     future = m.make_future_dataframe(periods=120, freq='M')
    #     forecast = m.predict(future)
    #     return plot_plotly(m, forecast)

# def get_prediction_price(zip_code, retirement_date):
#     # p_df = prophet_df_from_zillow_row(zip_code)
#     forecast = pd.read_pickle('pickles/{}_forecast.pkl'.format(zip_code))
#     forecast = forecast[forecast['ds'] < str(retirement_date)]
#     # print(forecast.tail(1))
#     return forecast.tail(1)['yhat'].values[0]

# def is_within_1_degree(center, marker):
#     if (marker.lat >= center.lat-1 and marker.lat <= center.lat+1) and (marker.lon >= center.lon - 1 and marker.lon <= center.lon + 1):
#         return True
#     else:
#         return False

def prophet_df_from_zillow_row(row):
    row = home_values[home_values['RegionName'] == row].copy()
    row = row.T
    row = row.drop(['RegionID', 'RegionName', 'City', 'State', 'Metro', 'CountyName', 'SizeRank'])
    row = row.reset_index()
    row = row.rename(columns={'index': 'ds', list(row)[1]: 'y'})
    row['ds'] = pd.to_datetime(row['ds'])
    return row
