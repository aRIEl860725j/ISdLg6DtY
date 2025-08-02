# 代码生成时间: 2025-08-03 03:55:38
import dash
import dash_core_components as dcc
import dash_html_components as html
import json
from dash.dependencies import Input, Output

# 定义全局变量，用于存储原始的JSON数据
original_json_data = ''

# 定义JSON数据格式化函数
def format_json(json_string):
    """
    将输入的JSON字符串格式化为更易读的格式。
    
    参数:
    json_string (str): 要格式化的JSON字符串。
    
    返回:
    str: 格式化后的JSON字符串，如果输入无效则返回错误信息。
    """
    try:
        # 将JSON字符串转换为Python字典
        json_data = json.loads(json_string)
        # 将字典格式化为字符串
        formatted_json = json.dumps(json_data, indent=4)
        return formatted_json
    except json.JSONDecodeError as e:
        # 如果JSON解析失败，返回错误信息
        return f'Invalid JSON: {str(e)}'

# 创建Dash应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div([
    # 提供一个文本输入框，用于输入原始的JSON字符串
    dcc.Textarea(
        id='json-input',
        placeholder='Enter your JSON here...',
        style={'width': '100%', 'height': '300px'},
        value=original_json_data
    ),
    # 提供一个按钮，用于触发JSON格式化操作
    html.Button('Format JSON', id='format-button', n_clicks=0),
    # 提供一个文本区域，用于显示格式化后的JSON数据
    dcc.Textarea(
        id='formatted-json-output',
        placeholder='Formatted JSON will appear here...',
        style={'width': '100%', 'height': '300px'},
        value='',
        readOnly=True
    )
])

# 定义回调函数，用于处理JSON格式化操作
@app.callback(
    Output('formatted-json-output', 'value'),
    [Input('format-button', 'n_clicks')],
    [State('json-input', 'value')]
)
def format_json_callback(n_clicks, json_input):
    "