# 代码生成时间: 2025-09-07 02:38:00
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime as dt

# 定义定时任务调度器类
class DashboardScheduler:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        # 定义Dash界面布局
        self.app.layout = html.Div([
            html.H1("定时任务调度器"),
            html.Div([
                html.P("任务名称"),
                dcc.Input(id='task-name', type='text', placeholder='请输入任务名称')
            ]),
            html.Div([
                html.P("执行时间"),
                dcc.Input(id='exec-time', type='text', placeholder='请输入执行时间，例如：2023-12-25 14:00:00')
            ]),
            html.Button('添加任务', id='add-task-button', n_clicks=0),
            dcc.Interval(
                id='interval-component',
                interval=1*1000,  # in milliseconds
                disabled=False
            )
        ])

    def add_task(self, task_name, exec_time):
        # 添加任务到调度器
        try:
            self.scheduler.add_job(self.execute_task, 'date', run_date=exec_time, args=[task_name])
        except Exception as e:
            print(f"添加任务失败：{e}")
            raise

    def execute_task(self, task_name):
        # 定义任务执行逻辑
        print(f"任务 {task_name} 正在执行...")

    def setup_callbacks(self):
        # 定义Dash回调函数
        @self.app.callback(
            Output('interval-component', 'disabled'),
            [Input('interval-component', 'n_intervals')]
        )
        def update_output(n):
            return True

        @self.app.callback(
            Output('task-name', 'value'),
            [Input('add-task-button', 'n_clicks')],
            [State('task-name', 'value'), State('exec-time', 'value')]
        )
        def add_task_callback(n_clicks, task_name, exec_time):
            if n_clicks > 0:
                self.add_task(task_name, exec_time)
                raise PreventUpdate
            return task_name

    def run(self):
        # 启动Dash应用和调度器
        self.app.run_server(debug=True)
        self.scheduler.start()

# 创建调度器对象
scheduler = BlockingScheduler()

# 创建并启动DashboardScheduler应用
if __name__ == '__main__':
    scheduler_app = DashboardScheduler(scheduler)
    scheduler_app.run()