# 代码生成时间: 2025-08-22 06:46:35
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote

# 定义XSS攻击防护函数
def xss_protection(input_string):
    """
    清理输入字符串以防止XSS攻击。
    
    :param input_string: 输入的字符串
    :return: 清理后的字符串
    """
    try:
        # 解码URL编码字符
        input_string = unquote(input_string)
        # 使用BeautifulSoup解析HTML，并移除潜在的XSS代码
        soup = BeautifulSoup(input_string, features="lxml")
        clean_string = soup.get_text()
        # 移除所有JavaScript代码
        clean_string = re.sub(r"<script>(.*?)</script>", "", clean_string, flags=re.IGNORECASE)
        # 移除所有HTML标签
        clean_string = re.sub(r"<[^>]+>", "", clean_string)
        return clean_string
    except Exception as e:
        # 错误处理
        print(f"Error cleaning input string: {e}")
        return "Error"

# 初始化Dash应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div([
    html.H1("XSS Protection Dashboard"),
    dcc.Textarea(
        id='input-string',
        placeholder='Enter your string here...',
        style={'width': '80%', 'height': '100px', 'margin': '20px'}
    ),
    html.Button("Clean String", id='clean-button', n_clicks=0),
    html.Div(id='output-container')
])

# 定义回调函数，用于清理输入字符串
@app.callback(
    Output('output-container', 'children'),
    [Input('clean-button', 'n_clicks'),
     Input('input-string', 'value')]
)
def clean_string(n_clicks, input_value):
    if n_clicks > 0 and input_value:
        # 清理输入字符串
        clean_string = xss_protection(input_value)
        return html.Div([html.H2("Cleaned String"), html.Pre(clean_string)])
    return ""

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)