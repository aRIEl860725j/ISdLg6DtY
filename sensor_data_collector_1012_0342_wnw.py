# 代码生成时间: 2025-10-12 03:42:21
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from flask import Flask
import random
import datetime as dt

# 模拟传感器数据生成函数
def generate_sensor_data():
    """生成模拟传感器数据"""
    return {
        "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sensor_value": random.uniform(0, 100)
    }

# 创建Dash应用
def create_dash_app():
    app = dash.Dash(__name__)
    
    # 应用布局
    app.layout = html.Div([
        html.H1("传感器数据采集"),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000,  # 每1秒刷新
            n_intervals=0
        )
    ])
    
    # 回调函数，用于实时更新图表
def update_graph_live(app):
    @app.callback(Output('live-update-graph', 'figure'), [Input('interval-component', 'n_intervals')])
    def update_graph_live(n):
        data = generate_sensor_data()
        df = pd.DataFrame([data])
        fig = px.line(df, x='timestamp', y='sensor_value', title='实时传感器数据')
        return fig
    
    # 注册回调函数
    app.callback(Output('live-update-graph', 'figure'), [Input('interval-component', 'n_intervals')])(update_graph_live)
    
    return app

# 运行应用
def run_app():
    app = create_dash_app()
    app.run_server(debug=True)

if __name__ == '__main__':
    run_app()
