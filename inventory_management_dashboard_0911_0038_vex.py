# 代码生成时间: 2025-09-11 00:38:14
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
from sqlalchemy import create_engine
import base64
import io
import plotly.express as px

# 定义全局变量，用于存储库存数据
INVENTORY_DATA = {}
DATABASE_URI = 'sqlite:///inventory.db'  # 示范用的SQLite数据库

# 创建数据库引擎
engine = create_engine(DATABASE_URI)

# 定义Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定义应用布局
app.layout = html.Div([
    html.H1('库存管理系统'),
    dcc.Upload(
        id='upload-data',
        children=html.Button('上传库存数据'),
        multiple=False,
        style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'},
    ),
    html.Div(id='output-data-upload'),
    dcc.Dropdown(
        id='inventory-dropdown',
        options=[{'label': item, 'value': item} for item in INVENTORY_DATA.keys()],
        value=list(INVENTORY_DATA.keys())[0] if INVENTORY_DATA else None,
        multi=False,
    ),
    dcc.Graph(id='inventory-graph'),
])

# 处理上传文件并更新库存数据
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')],
)
def update_output(contents, filename, last_modified):
    if contents is None:
        raise PreventUpdate
    # 解码文件内容并读取为Pandas DataFrame
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return dbc.Alert('文件格式不支持', color='danger')
        # 验证并更新库存数据
        INVENTORY_DATA.update(df.to_dict(orient='list'))
        return dbc.Alert('库存数据更新成功', color='success')
    except Exception as e:
        return dbc.Alert(f'文件读取失败：{str(e)}', color='danger')

# 更新下拉菜单和图表
@app.callback(
    Output('inventory-dropdown', 'options'),
    Output('inventory-graph', 'figure'),
    [Input('upload-data', 'contents')],
)
def update_graph(contents):
    if contents is None:
        raise PreventUpdate
    # 更新下拉菜单选项
    options = [{'label': item, 'value': item} for item in INVENTORY_DATA.keys()]
    # 选择第一个项目作为默认值
    default_value = list(INVENTORY_DATA.keys())[0]
    # 更新图表
    df = pd.DataFrame(INVENTORY_DATA[default_value])
    fig = px.bar(df, x=df.columns, y=df.values[0])
    fig.update_layout(title='库存概览', xaxis_title='类别', yaxis_title='数量')
    return options, fig

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)