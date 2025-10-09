# 代码生成时间: 2025-10-10 03:43:25
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import os
from PIL import Image

# Define the directory for media assets
MEDIA_DIRECTORY = 'media_assets'

# Check if the media directory exists, if not, create it
if not os.path.exists(MEDIA_DIRECTORY):
    os.makedirs(MEDIA_DIRECTORY)

# Initialize the Dash application
app = dash.Dash(__name__)

# Define the layout of the Dash application
app.layout = html.Div([
    html.H1("Media Asset Management"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True  # Allow multiple file uploads
    ),
    html.Div(id='output-data-upload')
])

# Callback to update the output when new files are uploaded
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')]
)
def update_output(contents):
    if contents is not None:
        # Create an empty list to store the file names
        file_names = []
        
        # Loop through the uploaded files
        for i, content in enumerate(contents):
            filename = content.filename
            
            # Check if the file is an image
            if filename.split('.')[-1].lower() in ['jpg', 'jpeg', 'png']:
                # Save the image file to the media directory
                with open(os.path.join(MEDIA_DIRECTORY, filename), 'wb') as f:
                    f.write(content)
                    
                # Append the file name to the list
                file_names.append(filename)
            else:
                # If the file is not an image, print an error message
                print(f"Unsupported file format: {filename}")
        
        # Return a list of uploaded file names
        return [html.Li(filename) for filename in file_names]
    else:
        # If no files are uploaded, return an empty list
        return html.P("No files uploaded")

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)