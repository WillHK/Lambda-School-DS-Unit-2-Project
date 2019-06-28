from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app

layout = html.Div(children=[html.H6("Plan your perfect retirement"),
            html.Img(src="/assets/beach_house.jpg"),
            html.Div("The coming years will see a record number of Americans retire as the Baby Boomer generation reaches their golden years."),
            html.Div("For many people retirement involves finding a warm sunny place to enjoy their sunset years,"),
            html.Div("but as the cost of buying a house continues it's march upwards it becomes even more important to find an affordable home."),
            html.Div("Retirement Hunt allows you to search by Zip Code and easily find the projected average home value in the region. Take advantage of the internet age and find the home for your old age."),
            html.Div("To use Retirement Hunt just click on the Map tab and enter a Zip Code you would like to explore."),
            html.Div("After entering a Zip Code You'll see a map of the area and a chart of projected Housing costs."),
            html.Div("You can also choose a length of time until you retire to see exactly how much your future home will cost."),
            html.H6("Future Features"),
            html.Div("An extremely important part of where you choose to live is the weather."),
            html.Div("In order to assist with finding the ideal location Retirement Hunt will supply weather predictions for the chosen retirement timeframe."),
            html.Div("Part of aging is needing access to world class healthcare, Retirement Hunt will show nearby healthcare facilities and other senior oriented services.")
])