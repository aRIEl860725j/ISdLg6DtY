# 代码生成时间: 2025-08-02 21:28:08
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import random

# 定义应用程序
app = dash.Dash(__name__)

# 定义应用程序布局
app.layout = html.Div([
    # 标题
    html.H1('Random Number Generator'),
    # 输入框，用于指定随机数的范围
    dcc.Input(id='min-number', type='number', placeholder='Min', value=0),
    dcc.Input(id='max-number', type='number', placeholder='Max', value=100),
    # 按钮，用于生成随机数
    html.Button('Generate', id='generate-button', n_clicks=0),
    # 输出框，用于显示生成的随机数
    html.Div(id='output-container')
])

# 定义回调函数，用于生成随机数
@app.callback(
    Output('output-container', 'children'),
    [Input('generate-button', 'n_clicks')],
    [State('min-number', 'value'), State('max-number', 'value')]
)
def generate_random_number(n_clicks, min_value, max_value):
    # 检查输入是否有效
    if min_value is None or max_value is None or min_value >= max_value:
        return 'Invalid input. Please enter a valid range.'
    
    # 生成随机数并返回
    random_number = random.randint(int(min_value), int(max_value))
    return f'Generated random number: {random_number}'

# 运行应用程序
if __name__ == '__main__':
    app.run_server(debug=True)