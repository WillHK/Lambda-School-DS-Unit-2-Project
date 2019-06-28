from app import app
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

layout = html.Div(
    html.H2("Examples"),
    html.H6("San Francisco, California"),
    html.Div("The city of San Francisco is a poster child for rising property values, the 94920 zip code exemplifies this with median values of $2.66 million in May 2019."),
    dcc.Graph(),
    html.Div("Within 5 years our model suggests median prices of $3.52 million, possibly not the right place to plan on retiring."),
    html.H6("Baltimore County, Maryland"),
    html.Div("On the other side of the country we have 21236 just outside Baltimore with median prices of $238,000 in May 2019."),
    dcc.Graph(),
    html.Div("In 5 years prices are projected to rise to $267,804, a much more reasonable increase."),
    html.Div("As you can see by picking the right location your money will go much further and allow a higher quality of living during retirement.")
) 