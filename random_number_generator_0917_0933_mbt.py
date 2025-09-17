# 代码生成时间: 2025-09-17 09:33:58
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import random
import plotly.express as px
from dash.exceptions import PreventUpdate

# 定义Dash应用程序
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# 添加布局
app.layout = html.Div([
    # 标题
    html.H1("Random Number Generator"),
    # 输入框用于用户输入范围
    dcc.Input(id='min-input', type='number', value=1, debounce=True),
    dcc.Input(id='max-input', type='number', value=10, debounce=True),
    # 按钮用于生成随机数
    html.Button("Generate", id="generate-button"),
    # 输出区域显示生成的随机数
    html.Div(id="output-container")
])

# 回调函数用于生成随机数
@app.callback(
    Output("output-container", "children"),
    [Input("generate-button", "n_clicks")],
    [State("min-input", "value"), State("max-input", "value")],
    prevent_initial_call=True
)
def generate_random_number(n_clicks, min_value, max_value):
    # 如果按钮未点击，则不更新输出
    if n_clicks is None:
        raise PreventUpdate()
    
    # 检查输入值是否有效
    if min_value >= max_value:
        return "Minimum value must be less than maximum value."
    
    # 生成并返回随机数
    random_number = random.randint(min_value, max_value)
    return f"Generated Random Number: {random_number}"

# 运行应用程序
if __name__ == '__main__':
    app.run_server(debug=True)