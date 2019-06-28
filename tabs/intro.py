from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app

layout = [dcc.Markdown("""
### Plan your perfect retirement

The coming years will see a record number of Americans retire as the
Baby Boomer generation reaches their golden years. For many people
retirement involves finding a warm sunny place to enjoy their sunset years,
but as the cost of buying a house continues it's march upwards it becomes even
more important to find an affordable home.

Retirement Hunt allows you to search by Zip Code and easily find the projected
average home value in the region. Take advantage of the internet age and find
the home for your old age.
""")]