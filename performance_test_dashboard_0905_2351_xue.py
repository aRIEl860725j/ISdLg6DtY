# 代码生成时间: 2025-09-05 23:51:21
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
from urllib.error import URLError
import requests
import time
import random

# Define the layout of the dashboard
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Performance Test Dashboard'),
    dcc.Dropdown(
        id='endpoint-dropdown',
        options=[{'label': i, 'value': i} for i in ['Endpoint 1', 'Endpoint 2']],
        value='Endpoint 1'
    ),
    dcc.Graph(id='response-time-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    ),
    html.Div(id='output-container')
])

# Function to fetch response time from endpoint
def fetch_response_time(endpoint):
    try:
        start_time = time.time()
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise an exception for HTTP errors
        end_time = time.time()
        return end_time - start_time
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data from {endpoint}: {e}')
        return None

# Callback to update the graph
@app.callback(
    Output('response-time-graph', 'figure'),
    Input('interval-component', 'n_intervals'),
    Input('endpoint-dropdown', 'value'))
def update_graph(n, endpoint):
    if endpoint is None:
        raise PreventUpdate
    response_time = fetch_response_time(f'http://{endpoint}')
    if response_time is None:
        response_time = 0
    data = [go.Scatter(
        x=['Response Time'],
        y=[response_time],
        mode='lines+markers',
        name='Endpoint: ' + endpoint
    )]
    layout = go.Layout(
        title='Response Time Over Time',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Response Time (s)')
    )
    return go.Figure(data=data, layout=layout)

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)