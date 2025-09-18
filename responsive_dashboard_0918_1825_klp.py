# 代码生成时间: 2025-09-18 18:25:04
import dash
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dependencies import MATCH, ALL, ALLSMALLER
import plotly.express as px
import pandas as pd

# 定义一个响应式布局的Dash应用
app = dash.Dash(__name__)

# 应用的布局定义
app.layout = html.Div(
    [
        # 定义一个下拉菜单，用于选择数据集
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': i, 'value': i} for i in ['MT Car Simulation', 'Fruit Retail Demo', 'Candlestick Chart']],
            value='MT Car Simulation',
            clearable=False,
            searchable=False
        ),
        # 定义一个图表容器，用于显示图表
        dcc.Graph(id='example-graph', style={'height': '70vh'}),
        # 定义一个表格容器，用于显示表格数据
        dcc.Table(id='example-table', style={'height': '30vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}
)

# 回调函数，用于更新图表和表格数据
@app.callback(
    Output('example-graph', 'figure'),
    Output('example-table', 'children'),
    Input('dropdown', 'value'))
def update_graph_and_table(value):
    # 根据下拉菜单的值选择对应的数据集
    if value == 'MT Car Simulation':
        df = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [2, 1, 3, 5, 4]})
    elif value == 'Fruit Retail Demo':
        df = pd.DataFrame({'fruit': ['Apples', 'Oranges', 'Bananas', 'Berries', 'Grapes'], 'sales': [10, 20, 30, 40, 50]})
    elif value == 'Candlestick Chart':
        df = pd.DataFrame({'Date': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05']})
    else:
        raise PreventUpdate  # 如果下拉菜单的值无效，则阻止更新

    # 根据选择的数据集生成图表
    if value == 'MT Car Simulation':
        fig = px.scatter(df, x='x', y='y', title='MT Car Simulation Data')
    elif value == 'Fruit Retail Demo':
        fig = px.bar(df, x='fruit', y='sales', title='Fruit Retail Data')
    elif value == 'Candlestick Chart':
        fig = px.line(df, x='Date', y='sales', title='Candlestick Chart Data')
    else:
        raise PreventUpdate  # 如果下拉菜单的值无效，则阻止更新

    # 根据选择的数据集生成表格
    table_children = html.Table(
        [
            html.Tr([html.Th(col) for col in df.columns]),
            *[
                html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(len(df))
            ]
        ]
    )

    return fig, table_children

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)