import os
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server

style = {'maxWidth': '960px', 'margin': 'auto'}

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-intro', children=[
        dcc.Tab(label='Intro', value='tab-intro'),
        dcc.Tab(label='Map', value='tab-map')
    ]),
    html.Div(id='tabs-content')
])

from tabs import intro, map

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-intro': return intro.layout
    elif tab == 'tab-map': return map.layout

if __name__ == '__main__':
    app.run_server(debug=True)