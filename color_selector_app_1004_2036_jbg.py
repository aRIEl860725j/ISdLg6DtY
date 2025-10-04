# 代码生成时间: 2025-10-04 20:36:33
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Define the layout of the app
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Store(id='color-store'),  # Store to hold the selected color
    html.H1("Color Selector"),
    html.P("Select a color from the dropdown below: "),
    dcc.Dropdown(
        id='color-dropdown',
        options=[{'label': color, 'value': color} for color in ['red', 'green', 'blue', 'yellow']],
        value='red'  # Default value
    ),
    html.P(id='color-output'),
    dcc.Graph(id='color-graph')
])

# Callback to update the color display and the graph
@app.callback(
    [Output('color-output', 'children'),
     Output('color-graph', 'figure')],
    [Input('color-dropdown', 'value')],
    [State('color-store', 'data')]
)
def update_output(selected_color):
    # If no color is selected, use the stored color or the default
    color = selected_color if selected_color else 'red'
    # Store the selected color
    app.callback_map.id_registry.callbacks['color-store']['callbacks'][0].set_state(color)
    # Create a simple bar chart
    df = px.DataFrame(px.data.iris(), 
                      x='sepal_width', 
                      y='sepal_length', 
                      color=color)
    fig = df.figure
    fig.update_layout(title_text=f'Graph with {color} color')
    return f'You have selected {color}', fig

if __name__ == '__main__':
    app.run_server(debug=True)