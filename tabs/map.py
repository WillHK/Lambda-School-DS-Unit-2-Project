from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import os
import sys
sys.path.append('../libs')

import plotly.offline as py_off
from plotly.graph_objs import *

import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import matplotlib.pyplot as plt
import pickle

from app import app
from helper_functions import *

layout = html.Div([
    html.H2('Retirement Hunt'),
    html.Div([
        html.Div([
            html.H6('Enter a US Zip Code'),
            dcc.Input(id='zip-code', value=98272, type='number'),
            html.Br(),
            html.H6('In how many years do you want to retire?'),
            dcc.Slider(id='retirement-slider',min=1, max=10, step=0.5, value=5),
            html.Div(id='retirement-label')
        ], className="six columns"),
        html.Div([
            html.H4('Map of local area'),
            dcc.Graph(id='zip-map')
        ], className="six columns")
    ], className="row"),
    html.Div(id='my-div'),
    dcc.Graph(id='pred-graph'),
    html.Div("Data acquired from Zillow.com/data on June 19th, 2019. Aggregated data on this page is made freely available by Zillow for non-commercial use.")
], className="container")

@app.callback(
    Output(component_id="retirement-label", component_property='children'),
    [Input(component_id='retirement-slider', component_property='value')]
)
def update_slider_label(retirement_distance):
    return f'{retirement_distance} years'

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='zip-code', component_property='value')]
)
def update_output_div(input_value):
    row = prophet_df_from_zillow_row(input_value)
    print(isinstance(row, pd.DataFrame))
    if isinstance(row, pd.DataFrame):
        return 'Property Value Projection for {}'.format(input_value)
    else:
        return 'Invalid Zip'

@app.callback(
    Output(component_id='pred-graph', component_property='figure'),
    [Input(component_id='zip-code', component_property='value'),
     Input(component_id='retirement-slider', component_property='value')]
)
def extract_zip_display_graph(input_value, retirement_distance):
    retirement_date = 2019 + retirement_distance
    row = prophet_df_from_zillow_row(input_value)
    if isinstance(row, pd.DataFrame):
        return prophet_prediction(row, input_value, retirement_date)
    else:
        return {}
        
@app.callback(
    Output(component_id='zip-map', component_property='figure'),
    [Input(component_id='zip-code', component_property='value'),
     Input(component_id='retirement-slider', component_property='value')]
)