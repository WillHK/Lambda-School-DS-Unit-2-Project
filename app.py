import os
from dotenv import load_dotenv

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.offline as py_off
from plotly.graph_objs import *

import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import matplotlib.pyplot as plt
load_dotenv()

home_values = pd.read_csv('Zip_Zhvi_AllHomes.csv', encoding="ISO-8859-1")
zip_lat_lng = pd.read_csv("https://gist.githubusercontent.com/erichurst/7882666/raw/5bdc46db47d9515269ab12ed6fb2850377fd869e/US%2520Zip%2520Codes%2520from%25202013%2520Government%2520Data")

# home_values[home_values['RegionName'] == 98117]
def prophet_df_from_zillow_row(row):
    row = home_values[home_values['RegionName'] == row].copy()
    row = row.T
    row = row.drop(['RegionID', 'RegionName', 'City', 'State', 'Metro', 'CountyName', 'SizeRank'])
    row = row.reset_index()
    row = row.rename(columns={'index': 'ds', list(row)[1]: 'y'})
    row['ds'] = pd.to_datetime(row['ds'])
    return row


def prophet_prediction(row):
    m = Prophet(seasonality_mode='multiplicative')
    m.fit(row)
    future = m.make_future_dataframe(periods=120, freq='M')
    forecast = m.predict(future)
    return plot_plotly(m, forecast)
    # fig = plt.figure(figsize=(15,8), dpi=1000)
    # ax = fig.add_subplot(111)
    # plt.title("Housing Cost Projections")
    # fig1 = m.plot(forecast, ax=ax, xlabel="Year", ylabel="Housing Cost in USD")
    # return fig1

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Home Value Projection'),
    html.H6('Enter a US Zip Code'),
    dcc.Input(id='zip-code', value=98272, type='number'),
    html.H6('In how many years do you want to retire?'),
    dcc.Slider(min=1, max=10, step=0.5, value=5),
    html.Div(id='my-div'),
    dcc.Graph(id='pred-graph'),
    dcc.Graph(id='zip-map')
])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='zip-code', component_property='value')]
)
def update_output_div(input_value):
    row = prophet_df_from_zillow_row(input_value)
    if isinstance(row, pd.DataFrame):
        return 'Property Value Projection for {}'.format(input_value)
    else:
        return 'Invalid Zip'

@app.callback(
    Output(component_id='pred-graph', component_property='figure'),
    [Input(component_id='zip-code', component_property='value')]
)
def extract_zip_display_graph(input_value):
    row = prophet_df_from_zillow_row(input_value)
    if isinstance(row, pd.DataFrame):
        return prophet_prediction(row)
    else:
        return {}
        
@app.callback(
    Output(component_id='zip-map', component_property='figure'),
    [Input(component_id='zip-code', component_property='value')]
)
def zoom_map_on_zip(input_value):
    data = []

    data.append(
        Scattermapbox(
            lon=zip_lat_lng['LNG'].values,
            lat=zip_lat_lng['LAT'].values,
            text=zip_lat_lng['ZIP'].values,
            mode='markers',
            name="Zip Codes",
            marker=scattermapbox.Marker(
                color="#ffffff"
            )
        )
    )

    layout = Layout(
        margin=dict(t=0,b=0,r=0,l=0),
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=os.getenv("MAPBOX_ACCESS_TOKEN"),
            bearing=0,
            center=dict(
                lat=zip_lat_lng[zip_lat_lng['ZIP'] == input_value]['LAT'].values[0],
                lon=zip_lat_lng[zip_lat_lng['ZIP'] == input_value]['LNG'].values[0]
            ),
            pitch=0,
            zoom=9,
            style='dark'
        )
    )
    fig = Figure(data=data, layout=layout)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)