# 代码生成时间: 2025-09-03 07:47:08
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# 设置日志
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# 创建Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定义定时任务调度器
scheduler = BackgroundScheduler()

# 定义定时任务函数
def timed_task():
    logging.info("定时任务执行...")

# 在调度器中添加任务，参数说明：func: 任务函数，trigger: 触发器类型，interval: 时间间隔（秒）
scheduler.add_job(timed_task, 'interval', seconds=5)

# 启动调度器
scheduler.start()

# Dash应用布局
app.layout = html.Div([
    dbc.Container(
        className="p-4",
        children=[
            dbc.Row(
                className="mb-4",
                children=[
                    dbc.Col(dcc.Markdown("## 定时任务调度器"), md=12)
                ]
            ),
            dbc.Row(
                className="mb-4",
                children=[
                    dbc.Col(dcc.Markdown("这是一个使用Dash和APScheduler实现的定时任务调度器。"), md=12)
                ]
            )
        ]
    )
])

# Dash回调函数，用于更新定时任务状态
@app.callback(
    Output("output-div", "children"),
    [Input("interval-component", "value"), Input("start-button", "n_clicks"), Input("stop-button", "n_clicks")],
    [State("interval-component", "value"), State("output-div", "children")],
    prevent_initial_call=True
)
def update_output_div(value, start_n_clicks, stop_n_clicks, current_value, current_output):
    if start_n_clicks is not None and start_n_clicks > 0:
        scheduler.add_job(timed_task, 'interval', seconds=value)
        scheduler.start()
        raise PreventUpdate
    elif stop_n_clicks is not None and stop_n_clicks > 0:
        scheduler.shutdown()
        raise PreventUpdate
    return current_output

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)
