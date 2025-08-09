# 代码生成时间: 2025-08-10 04:33:14
import os
import sqlite3
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdateError
from dash_extensions.snippet import send_code
import pandas as pd

# Define the application's layout
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1('Database Migration Tool'), className='text-center'),
        ]),
        dbc.Row([
            dbc.Col(html.P('Select source and destination databases.'), className='text-center'),
        ]),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.Button('Choose Source Database', color='primary', id='choose-source-db'),
                dbc.Button('Choose Destination Database', color='primary', id='choose-destination-db'),
                html.Div(id='source-db-path'),
                html.Div(id='destination-db-path'),
            ]), className='mt-3'),
        ]),
        dbc.Row([
            dbc.Col(dbc.Button('Migrate Database', color='primary', id='migrate-db'), className='text-center mt-3'),
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='output'), className='text-center'),
        ]),
    ]),
])

# Callback for choosing source database
@app.callback(
    Output('source-db-path', 'children'),
    [Input('choose-source-db', 'n_clicks')],
    [State('source-db-path', 'children')]
)
def choose_source_db(n_clicks, current_path):
    if n_clicks and not current_path:
        path = filedialog.askopenfilename()
        return html.P(f'Selected source database: {path}')
    raise PreventUpdateError

# Callback for choosing destination database
@app.callback(
    Output('destination-db-path', 'children'),
    [Input('choose-destination-db', 'n_clicks')],
    [State('destination-db-path', 'children')]
)
def choose_destination_db(n_clicks, current_path):
    if n_clicks and not current_path:
        path = filedialog.asksaveasfilename()
        return html.P(f'Selected destination database: {path}')
    raise PreventUpdateError

# Callback for migrating database
@app.callback(
    Output('output', 'children'),
    Input('migrate-db', 'n_clicks'),
    State('source-db-path', 'children'),
    State('destination-db-path', 'children')
)
def migrate_db(n_clicks, source_path, destination_path):
    try:
        # Connect to source database
        with sqlite3.connect(source_path) as conn:
            # Read data from source database
            query = "SELECT * FROM your_table"
            df = pd.read_sql_query(query, conn)
            # Connect to destination database
            with sqlite3.connect(destination_path) as conn:
                # Write data to destination database
                df.to_sql('your_table', conn, if_exists='replace', index=False)
        return html.P('Migration successful!')
    except Exception as e:
        return html.P(f'Error: {str(e)}')

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
