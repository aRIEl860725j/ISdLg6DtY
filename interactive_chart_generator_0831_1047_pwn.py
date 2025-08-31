# 代码生成时间: 2025-08-31 10:47:00
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# 定义Dash应用
app = dash.Dash(__name__)

# 设置应用的布局
app.layout = html.Div([
    html.H1("交互式图表生成器"),
    dcc.Dropdown(
        id="data-source",
        options=[
            {'label': '数据集1', 'value': 'data1'},
            {'label': '数据集2', 'value': 'data2'}
        ],
        value='data1'  # 默认值
    ),
    dcc.Graph(id="interactive-chart"),
    dcc.Slider(
        id='year-slider',
        min=1980,
        max=2020,
        value=1980,
        marks={str(year): str(year) for year in range(1980, 2021)},
        step=None
    )
])

# 回调函数，根据选择的数据集和年份生成图表
@app.callback(
    Output("interactive-chart", "figure"),
    [Input("data-source", "value"), Input("year-slider", "value")]
)
def update_graph(selected_data, year):
    # 加载数据集
    if selected_data == 'data1':
        df = pd.read_csv('data1.csv')
    elif selected_data == 'data2':
        df = pd.read_csv('data2.csv')
    else:
        # 处理错误数据集选择
        raise ValueError("无效的数据集选择")

    # 根据年份筛选数据
    df = df[df['Year'] == year]

    # 使用Plotly Express生成图表
    fig = px.bar(df, x='Category', y='Value', title=f'{year}年数据')
    return fig

# 运行Dash服务器
if __name__ == '__main__':
    app.run_server(debug=True)