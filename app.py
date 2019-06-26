import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import matplotlib.pyplot as plt

home_values = pd.read_csv('Zip_Zhvi_AllHomes.csv', encoding="ISO-8859-1")
# home_values[home_values['RegionName'] == 98117]
def prophet_df_from_zillow_row(row):
    if row > 11111:
        row = home_values[home_values['RegionName'] == row].copy()
        row = row.T
        row = row.drop(['RegionID', 'RegionName', 'City', 'State', 'Metro', 'CountyName', 'SizeRank'])
        row = row.reset_index()
        row = row.rename(columns={'index': 'ds', list(row)[1]: 'y'})
        row['ds'] = pd.to_datetime(row['ds'])
        return row
    else:
        return "Invalid Zip"

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
    dcc.Input(id='zip-code', value=98272, type='number'),
    html.Div(id='my-div'),
    dcc.Graph(id='pred-graph')
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
        

if __name__ == '__main__':
    app.run_server(debug=True)