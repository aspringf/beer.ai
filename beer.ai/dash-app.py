import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import pandas as pd

layout = dbc.Container(html.H1("Beer is smarter than you"))

app = dash.Dash(__name__)
server = app.server

app.layout = layout

if __name__ == "__main__":
    app.run_server()
