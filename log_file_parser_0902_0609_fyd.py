# 代码生成时间: 2025-09-02 06:09:40
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os

# 定义全局变量来存储日志文件路径和解析结果
LOG_FILE_PATH = ''
PARSING_RESULTS = None

# 定义一个函数来解析日志文件
def parse_log_file(log_file_path):
    try:
        # 尝试读取日志文件
        with open(log_file_path, 'r') as file:
            log_data = file.readlines()

        # 将日志数据存储为一个Pandas DataFrame
        global PARSING_RESULTS
        PARSING_RESULTS = pd.DataFrame(log_data, columns=['Log Entry'])
        return PARSING_RESULTS
    except Exception as e:
        # 处理文件读取或解析过程中的任何异常
        print(f'Error parsing log file: {e}')
        return None

# 定义一个函数来创建Dash应用
def create_dash_app(log_file_path):
    # 创建Dash应用
    app = dash.Dash(__name__)

    # 应用布局
    app.layout = html.Div([
        html.H1('Log File Parser Tool'),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select File')
            ]),
            style={'width': '100%', 'height': '60px', 'lineHeight': '60px',
                   'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                    'textAlign': 'center', 'margin': '10px'},
            # 允许上传文件
            multiple=False
        ),
        html.Div(id='output-data-upload'),
        dcc.Graph(id='log-file-graph')
    ])

    # 定义回调函数来处理文件上传
    @app.callback(
        Output('output-data-upload', 'children'),
        Input('upload-data', 'contents'),
        Input('upload-data', 'filename')
    )
    def update_output(list_of_contents, list_of_names):
        if list_of_contents is not None:
            # 解析上传的日志文件
            global LOG_FILE_PATH
            LOG_FILE_PATH = list_of_names[0]
            global PARSING_RESULTS
            PARSING_RESULTS = parse_log_file(LOG_FILE_PATH)
            return [html.Div([
                'File uploaded: ', html.B(list_of_names[0])
            ])]
        else:
            return [html.Div([
                'No file uploaded yet.'
            ])]

    # 定义回调函数来显示解析结果
    @app.callback(
        Output('log-file-graph', 'figure'),
        Input('upload-data', 'contents'),
        Input('upload-data', 'filename')
    )
    def update_graph(list_of_contents, list_of_names):
        if list_of_contents is not None:
            global PARSING_RESULTS
            if PARSING_RESULTS is not None:
                # 创建一个简单的图形来显示日志文件的前几行
                fig = px.bar(PARSING_RESULTS.head(), x=PARSING_RESULTS.index, y='Log Entry')
                return fig
            else:
                return {'data': [{'x': [], 'y': []}]}
        else:
            return {'data': [{'x': [], 'y': []}]}

    return app

# 运行Dash应用
if __name__ == '__main__':
    log_file_path = ''  # 指定日志文件路径
    app = create_dash_app(log_file_path)
    app.run_server(debug=True)