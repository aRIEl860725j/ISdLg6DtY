# 代码生成时间: 2025-09-01 10:23:16
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from dash.exceptions import PreventUpdate

# 定义一个函数来生成图表
def generate_chart(selected_df):
    # 检查输入的DataFrame是否为空
    if selected_df.empty:
        raise PreventUpdate

    # 根据选择的列生成图表
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=selected_df['x'], y=selected_df['y']))
    fig.update_layout(title='Interactive Chart', xaxis_title='X Axis', yaxis_title='Y Axis')
    return fig

# 创建Dash应用
app = dash.Dash(__name__)

# 定义应用布局
app.layout = html.Div([
    # 上方的下拉菜单，用于选择数据
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['Data 1', 'Data 2', 'Data 3']],
        value='Data 1'
    ),

    # 用于显示图表的容器
    dcc.Graph(id='live-update-graph'),

    # 用于存储DataFrame的隐藏状态
    dcc.Store(id='df-store', data={'Data 1': pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})}),

    # 用于存储选择的DataFrame索引的隐藏状态
    dcc.Store(id='selected-df-index', data='Data 1')
])

# 回调函数，用于更新图表
@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('dropdown', 'value'), Input('df-store', 'data')],
    [State('df-store', 'data'), State('selected-df-index', 'data')])
def update_graph(selected_df_index, df_store, current_df, selected_df_index_state):
    # 如果下拉菜单的选择未改变，则不更新图表
    if selected_df_index == selected_df_index_state:
        raise PreventUpdate

    # 更新选中的DataFrame索引
    app.callback_context.set_state('selected-df-index', selected_df_index)

    # 从存储中获取选中的DataFrame
    selected_df = df_store.get(selected_df_index)

    # 生成图表并返回
    return generate_chart(selected_df)

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)