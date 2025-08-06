# 代码生成时间: 2025-08-06 09:21:15
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
import pandas as pd

# 定义JSON数据格式转换器Dash应用
class JsonConverterDashApp:
    def __init__(self):
        # 初始化Dash应用
        self.app = dash.Dash(__name__)
        self.layout()

    def layout(self):
        # 定义应用布局
        self.app.layout = html.Div([
            # 上传文件的输入框
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={'width': '100%', 'height': '60px', 'lineHeight': '60px',
                        'borderWidth': '1px', 'borderStyle': 'dashed',
                        'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'}
            ),
            # 显示上传文件的名称
            html.Div(id='output-data-upload'),
            # JSON到Pandas DataFrame转换按钮
            html.Button('Convert JSON to DataFrame', id='convert-button'),
            # 显示转换结果的Dataframe表格
            dcc.Graph(id='output-graph')
        ])

    @staticmethod
def parse_contents(contents, filename):
        # 解析上传文件的内容
        contents = contents.encode('utf-8')
        return json.loads(contents)

    def callback(self):
        # 定义回调函数
        @self.app.callback(
            Output('output-data-upload', 'children'),
            Input('upload-data', 'contents')
        )
def update_output(*args, **kwargs):
            # 更新上传文件名称的显示
            contents = args[0]
            if contents is not None:
                return html.Div([
                    html.H5(filename),
                ])
            else:
                return html.Div([
                    'No file uploaded yet'
                ])

        @self.app.callback(
            Output('output-graph', 'figure'),
            Input('convert-button', 'n_clicks'),
            [State('upload-data', 'contents')]
        )
def update_graph(*args, **kwargs):
            # 更新转换结果的显示
            contents = args[1]
            if contents is not None:
                df = pd.DataFrame(self.parse_contents(contents, ""))
                return {
                    'data': [
                        {'x': df.columns.to_list(), 'y': df.sum().values.tolist(), 'type': 'bar', 'name': 'Sum'}
                    ],
                    'layout': {
                        'title': 'JSON to DataFrame Conversion Result'
                    }
                }
            else:
                return {}

    def run(self):
        # 运行Dash应用
        self.app.run_server(debug=True)

if __name__ == '__main__':
    app = JsonConverterDashApp()
    app.callback()
    app.run()