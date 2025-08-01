# 代码生成时间: 2025-08-02 00:46:15
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
# 改进用户体验

# 定义排序算法的函数
def sort_algorithm(data):
    # 检查数据是否为空
    if not data:
        raise ValueError("数据不能为空")
    # 这里以冒泡排序算法为例，其他排序算法可以在此扩展
    for i in range(len(data) - 1):
        for j in range(len(data) - 1 - i):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data

# 创建Dash应用
def create_dash_app():
    app = dash.Dash(__name__)
    app.layout = html.Div(children=[
        html.H1(children='排序算法可视化'),
        dcc.Input(id='input-data', placeholder='输入数字，用逗号分隔', type='text'),
# 改进用户体验
        html.Button(id='sort-button', n_clicks=0, children='排序'),
        dcc.Graph(id='sorted-graph')
    ])

    @app.callback(
        Output('sorted-graph', 'figure'),
        [Input('sort-button', 'n_clicks')],
        [State('input-data', 'value')]
    )
def update_graph(n_clicks, data_input):
        ctx = dash.callback_context
        if not ctx.triggered or n_clicks == 0:
            return px.line()

        data_list = [int(x) for x in data_input.split(',') if x.strip().isdigit()]
        try:
            sorted_data = sort_algorithm(data_list)
        except ValueError as e:
            return px.line(title=f'错误：{e}')

        df = pd.DataFrame({'Original': data_list, 'Sorted': sorted_data})
        return px.line(df)

    return app

# 运行Dash应用
def run_app():
# FIXME: 处理边界情况
    app = create_dash_app()
    app.run_server(debug=True)

if __name__ == '__main__':
    run_app()