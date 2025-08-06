# 代码生成时间: 2025-08-06 19:20:51
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

def create_app():
    # 创建一个Dash应用实例
    app = dash.Dash(__name__)

    # 定义应用的布局，包括输入组件和输出组件
    app.layout = html.Div([
        dcc.Graph(id='interactive-chart'),
        dcc.Dropdown(
            id='xaxis-column',
            options=[{'label': i, 'value': i} for i in ['Cylinders', ' displ', ' horsepower']],
            value='Cylinders',
        ),
        dcc.Dropdown(
            id='yaxis-column',
            options=[{'label': i, 'value': i} for i in ['Cylinders', ' displ', ' horsepower']],
            value='displ',
        ),
        dcc.RadioItems(
            id='chart-type',
            options=[{'label': i, 'value': i} for i in ['scatter', 'line', 'bar']],
            value='scatter',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'}
        ),
    ])

    @app.callback(
        Output('interactive-chart', 'figure'),
        [Input('xaxis-column', 'value'),
         Input('yaxis-column', 'value'),
         Input('chart-type', 'value')]
    )
    def update_graph(xaxis_column_name, yaxis_column_name, chart_type):
        # 过滤数据，确保x轴和y轴数据一致
        dff = pd.DataFrame({
            'Cylinders': np.random.randint(4, 10, 100),
            'displ': np.random.uniform(1, 7, 100),
            'horsepower': np.random.uniform(50, 300, 100)
        })
        # 根据用户选择的图表类型生成图表
        if chart_type == 'scatter':
            dff = px.scatter(dff, x=xaxis_column_name, y=yaxis_column_name, title=f'{chart_type.capitalize()} Chart')
        elif chart_type == 'line':
            dff = px.line(dff, x=xaxis_column_name, y=yaxis_column_name, title=f'{chart_type.capitalize()} Chart')
        elif chart_type == 'bar':
            dff = px.bar(dff, x=xaxis_column_name, y=yaxis_column_name, title=f'{chart_type.capitalize()} Chart')
        else:
            # 如果图表类型不是预期的，返回一个错误提示的图表
            dff = px.line(dff, x=xaxis_column_name, y=yaxis_column_name, title='Please select a valid chart type')
        return dff.figure

    return app

if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=True)