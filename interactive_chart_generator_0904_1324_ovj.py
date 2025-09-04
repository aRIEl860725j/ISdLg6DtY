# 代码生成时间: 2025-09-04 13:24:52
import dash\
import dash_core_components as dcc\
import dash_html_components as html\
from dash.dependencies import Input, Output, State\
import plotly.express as px\
import pandas as pd\

# 定义Dash应用\
app = dash.Dash(__name__)\

# 设置布局，包含下拉框、滑块和图表\
app.layout = html.Div([\
    # 标题\
    html.H1("交互式图表生成器"),\
    # 下拉框，选择图表类型\
    dcc.Dropdown(\
        id='chart-type-dropdown',\
        options=[\
            {'label': '折线图', 'value': 'line'},\
            {'label': '条形图', 'value': 'bar'},\
            {'label': '散点图', 'value': 'scatter'}\
        ],\
        value='line'  # 默认选择折线图\
    ),\
    # 滑块，设置x轴范围\
    dcc.Slider(\
        id='x-range-slider',\
        min=0,\
        max=100,\
        value=[0, 100],\
        marks={i: f'{i}' for i in range(0, 101, 10)},\
        step=1\
    ),\
    # 滑块，设置y轴范围\
    dcc.Slider(\
        id='y-range-slider',\
        min=0,\
        max=100,\
        value=[0, 100],\
        marks={i: f'{i}' for i in range(0, 101, 10)},\
        step=1\
    ),\
    # 图表\
    dcc.Graph(id='interactive-chart')\
])\

# 回调函数，更新图表\
@app.callback(\
    Output('interactive-chart', 'figure'),\
    [Input('chart-type-dropdown', 'value'),\
     Input('x-range-slider', 'value'),\
     Input('y-range-slider', 'value')])\
def update_chart(chart_type, x_range, y_range):
    # 模拟数据
    df = pd.DataFrame({'x': range(101), 'y': range(101)})

    # 根据图表类型和范围更新图表
    if chart_type == 'line':
        fig = px.line(df, x='x', y='y', range_x=x_range, range_y=y_range)
    elif chart_type == 'bar':
        fig = px.bar(df, x='x', y='y', range_x=x_range, range_y=y_range)
    elif chart_type == 'scatter':
        fig = px.scatter(df, x='x', y='y', range_x=x_range, range_y=y_range)
    else:
        raise ValueError(