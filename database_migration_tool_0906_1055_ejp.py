# 代码生成时间: 2025-09-06 10:55:55
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

# 数据库配置
DATABASE_URI = 'sqlite:///migration.db'  # 示例数据库URI，实际使用时需要替换为正确的数据库URI

# 创建Dash应用
app = dash.Dash(__name__)

# 定义应用布局
app.layout = html.Div([
    html.H1('数据库迁移工具'),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['拖拽文件到此区域或 ',
                            html.A('选择文件')])
    ),
    html.Div(id='output-data-upload'),
    html.Hr(),
    dcc.Graph(id='migration-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # 每秒刷新
        n_intervals=0
    ),
    html.Button('开始迁移', id='start-migration', n_clicks=0),
    html.Div(id='migration-status')
])

# 回调函数：处理文件上传
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
     State('upload-data', 'last_modified')]
)
def update_output(listed_input, listed_filename, listed_datetime):
    if listed_input is not None:
        return f'文件 {listed_filename} 已上传'
    return '尚未上传文件'

# 回调函数：读取上传的文件并展示数据
@app.callback(
    Output('migration-graph', 'figure'),
    [Input('upload-data', 'contents')]
)
def update_graph(uploaded_content):
    if uploaded_content is not None:
        # 将上传的CSV文件转换为DataFrame
        df = pd.read_csv(uploaded_content)
        # 使用Plotly Express创建图表
        fig = px.histogram(df, x=df.columns[0], nbins=30)
        return fig
    return {'data': [], 'layout': {'xaxis': {'title': 'X Axis'}, 'yaxis': {'title': 'Y Axis'}}}

# 回调函数：开始数据库迁移
@app.callback(
    Output('migration-status', 'children'),
    [Input('start-migration', 'n_clicks')],
    [State('upload-data', 'contents')]
)
def start_migration(n_clicks, contents):
    if n_clicks > 0 and contents is not None:
        try:
            # 创建数据库连接
            engine = sqlalchemy.create_engine(DATABASE_URI)
            connection = engine.connect()
            # 将上传的文件中的数据迁移到数据库
            df = pd.read_csv(contents)
            df.to_sql('migration_table', con=engine, if_exists='replace', index=False)
            return '数据库迁移成功'
        except SQLAlchemyError as e:
            return f'数据库迁移失败：{e}'
    return '请上传文件并点击开始迁移按钮'

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)