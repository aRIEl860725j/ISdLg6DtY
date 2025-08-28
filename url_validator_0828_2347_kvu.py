# 代码生成时间: 2025-08-28 23:47:32
import dash
from dash import html
import dash_bootstrap_components as dbc
from urllib.parse import urlparse
import requests

# 函数：验证URL是否有效
def validate_url(url):
    """
    验证给定的URL是否有效。
    
    参数:
        url (str): 要验证的URL。
    
    返回:
        bool: URL是否有效。
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

# Dash应用初始化
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 设置应用页面布局
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("URL Validator"), width=6),
    ]),
    dbc.Row([
        dbc.Col(dbc.Input(id="url-input", placeholder="Enter URL", type="text"), width=12),
    ]),
    dbc.Row([
        dbc.Col(html.Button("Validate", id="validate-button", n_clicks=0), width=6),
    ]),
    dbc.Row([
        dbc.Col(html.Div(id="output-container"), width=12),
    ]),
])

# 回调函数：当用户点击“Validate”按钮时触发
@app.callback(
    dash.dependencies.Output("output-container", "children"),
    [dash.dependencies.Input("validate-button", "n_clicks")],
    [dash.dependencies.State("url-input", "value")]
)
def validate_url_callback(n_clicks, url_value):
    """
    回调函数：当用户点击“Validate”按钮时触发。
    
    参数:
        n_clicks (int): 按钮点击次数。
        url_value (str): 用户输入的URL。
    
    返回:
        str: 验证结果。
    """
    if n_clicks > 0:
        output = "Invalid URL" if not validate_url(url_value) else "Valid URL"
    else:
        output = ""
    return output

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)