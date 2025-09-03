# 代码生成时间: 2025-09-03 17:20:05
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
from threading import Thread
import time
import logging as log

# 定义日志配置
log.basicConfig(level=log.INFO)

# 假设的数据生成器函数
def generate_data(duration, interval):
    """
    这个函数模拟数据生成，持续时间为duration秒，每个interval间隔生成一次数据。
    """
    t0 = time.time()
    while time.time() - t0 < duration:
        time.sleep(interval)
        # 模拟生成数据
        data = {
            'time': pd.to_datetime('now', unit='s'),
            'value': np.random.randint(1, 100)
        }
        yield data

# 性能测试页面布局
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Performance Test Dashboard'),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
    ),
    html.Div(id='live-update-text')
])

# 回调函数，用于实时更新图表
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')],
              [State('live-update-graph', 'figure')])
def update_graph_live(n, figure):  # n为时间戳
    if n is None:  # 如果是第一次，则不更新
        raise PreventUpdate
    
    # 模拟数据生成
    df = pd.DataFrame(list(generate_data(10, 1)))
    
    if not df.empty:  # 如果有新数据，则更新图表
        df['time'] = pd.to_datetime(df['time'])
        fig = px.line(df, x='time', y='value')
        fig.update_layout(title='Real-time Value')
        fig.update_yaxes(rangemode='tozero')
        return fig
    else:  # 如果没有新数据，则不更新
        raise PreventUpdate

# 启动服务器
if __name__ == '__main__':
    app.run_server(debug=True)