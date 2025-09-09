# 代码生成时间: 2025-09-09 13:36:16
import os
import logging
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化Dash应用
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定义安全审计日志应用布局
app.layout = html.Div(children=[
    html.H1('Security Audit Log'),
    dcc.Tabs(id="tabs",
            value='tab-1',
            children=[
                dcc.Tab(label='Log Viewer', value='tab-1'),
                dcc.Tab(label='Log Settings', value='tab-2')
            ],
            ),
    html.Div(id='tabs-content'),
])

# 设置Tab内容的回调函数
@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    # 根据Tab选择显示不同的内容
    if tab == 'tab-1':
        return html.Div(children=[
            html.H2('Log Viewer'),
            dcc.Textarea(id='log-viewer', style={'height': 400, 'width': '100%'}, readOnly=True),
        ])
    elif tab == 'tab-2':
        return html.Div(children=[
            html.H2('Log Settings'),
            # 这里可以添加更多设置选项
            dbc.FormText('Set log level:'),
            dcc.Dropdown(
                id='log-level-dropdown',
                options=[{'label': 'DEBUG', 'value': 'debug'},
                         {'label': 'INFO', 'value': 'info'},
                         {'label': 'WARNING', 'value': 'warning'},
                         {'label': 'ERROR', 'value': 'error'},
                         {'label': 'CRITICAL', 'value': 'critical'}],
                value='info'
            ),
        ])
    else:
        return None

# 读取日志并显示的回调函数
@app.callback(Output('log-viewer', 'value'), [Input('log-level-dropdown', 'value')])
def update_log_viewer(log_level):
    # 更新日志级别
    logging.getLogger().setLevel(getattr(logging, log_level.upper()))
    logger.info('Log level updated to {}'.format(log_level.upper()))
    
    # 读取日志文件内容
    try:
        log_file_path = os.path.join(os.getcwd(), 'logs', 'audit.log')
        with open(log_file_path, 'r') as file:
            logs = file.read()
        return logs
    except FileNotFoundError:
        logger.error('Log file not found.')
        return 'Log file not found.'
    except Exception as e:
        logger.error('An error occurred: {}'.format(str(e)))
        return 'An error occurred: {}'.format(str(e))

if __name__ == '__main__':
    # 运行Dash应用
    app.run_server(debug=True)