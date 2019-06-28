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

home_values = pd.read_csv('../Zip_Zhvi_AllHomes.csv', encoding="ISO-8859-1")
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
    forecast = forecast[(forecast['ds'] > '2009') & (forecast['ds'] < str(retirement_date))] 
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

def zoom_map_on_zip(input_value, retirement_distance):
    # retirement_date = 2019 + retirement_distance
    data = []
    # projections = []

    center_lat = zip_lat_lng[zip_lat_lng['ZIP'] == input_value]['LAT'].values[0]
    center_lon = zip_lat_lng[zip_lat_lng['ZIP'] == input_value]['LNG'].values[0]
    # for i in range(len(zip_lat_lng.LAT)):
    #     if (zip_lat_lng.iloc[i].LAT >= center_lat-1.0 and zip_lat_lng.iloc[i].LAT <= center_lat+1.0) and (zip_lat_lng.iloc[i].LNG >= center_lon - 1.0 and zip_lat_lng.iloc[i].LNG <= center_lon + 1.0):
    #         projections.append(get_prediction_price(int(zip_lat_lng.iloc[i].ZIP), retirement_date))
    #     else:
    #         projections.append(0)
    # zip_lat_lng['PROJECTIONS'] = projections

    data.append(
        Scattermapbox(
            lon=zip_lat_lng['LNG'].values,
            lat=zip_lat_lng['LAT'].values,
            text=zip_lat_lng['ZIP'].values,
            mode='markers+text',
            name="Zip Codes",
            marker=scattermapbox.Marker(
                color="#ffffff"
            )
        )
    )

    # for i in range(len(data[0].lat)):
        # print("Type of center: {}".format(type(center_lat)))
        # # print("Type of market: {}".format(type(data[0].lat[i])))
        # if (data[0].lat[i] >= center_lat-1.0 and data[0].lat[i] <= center_lat+1.0) and (data[0].lon[i] >= center_lon - 1.0 and data[0].lon[i] <= center_lon + 1.0):
        #     data[0].text += " {}".format(get_prediction_price(input_value, retirement_date))
        # print(data[0].lat[0])
        # if is_within_1_degree({'lat': center_lat, 'lon': center_lon}, {'lat': data[0].lat[i], 'lon': data[0].lon[i]}):
        #     print('True')

    layout = Layout(
        margin=dict(t=0,b=0,r=0,l=0),
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=os.getenv("MAPBOX_ACCESS_TOKEN"),
            bearing=0,
            center=dict(
                lat=center_lat,
                lon=center_lon
            ),
            pitch=0,
            zoom=9,
            style='dark'
        )
    )
    fig = Figure(data=data, layout=layout)
    return fig