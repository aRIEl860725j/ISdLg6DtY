# 代码生成时间: 2025-08-10 22:10:22
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import hashlib
import base64

def generate_hash(text: str, algorithm: str) -> str:
    """Generates a hash value for the given text using the specified algorithm."""
    if algorithm.lower() not in hashlib.algorithms_available:
        raise ValueError('Unsupported hash algorithm')
# 优化算法效率
    hash_function = getattr(hashlib, algorithm.lower())
    return hash_function(text.encode()).hexdigest()

def base64_encode(text: str) -> str:
    """Encodes the given text to base64."""
    return base64.b64encode(text.encode()).decode()

def hash_app():
    app = dash.Dash(__name__)
# 优化算法效率
    app.layout = html.Div(children=[
        html.H1('Hash Calculator'),
        dcc.Textarea(
            id='input-text',
            placeholder='Enter text here...',
            value='',
            style={'width': '100%', 'height': '100px'}
        ),
        dcc.Dropdown(
            id='algorithm-selector',
# 优化算法效率
            options=[
                {'label': algo, 'value': algo} for algo in sorted(hashlib.algorithms_available)
            ],
            value='sha256',
            clearable=False
        ),
        html.Button('Compute Hash', id='compute-button', n_clicks=0),
        html.Div(id='output-container')
    ])
    @app.callback(
        Output('output-container', 'children'),
        [Input('compute-button', 'n_clicks'), Input('input-text', 'value'), Input('algorithm-selector', 'value')]
    )
    def update_output(n_clicks, text, algorithm):
# 增强安全性
        if n_clicks == 0 or not text or not algorithm:
            return ''
        try:
            hash_value = generate_hash(text, algorithm)
            base64_encoded = base64_encode(text)
            return html.Div(children=[
                html.H4(f'Hash Value: {hash_value}'),
                html.H4(f'Base64 Encoded: {base64_encoded}')
            ])
        except Exception as e:
            return f'Error: {str(e)}'
    if __name__ == '__main__':
        app.run_server(debug=True)
