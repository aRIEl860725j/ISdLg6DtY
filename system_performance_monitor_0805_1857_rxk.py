# 代码生成时间: 2025-08-05 18:57:17
import psutil
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate

# 定义 Dash 应用
app = dash.Dash(__name__)

# 布局定义
app.layout = html.Div([
    html.H1('系统性能监控工具', style={'textAlign': 'center'}),
    dcc.Graph(id='cpu-graph'),
    dcc.Graph(id='memory-graph'),
    dcc.Graph(id='disk-graph'),
    dcc.Graph(id='network-graph'),
    html.Div(id='hidden-div', style={'display': 'none'}),
])

# 回调函数：获取CPU使用率
@app.callback(
    Output('cpu-graph', 'figure'),
    [Input('hidden-div', 'children')]
)
def update_cpu_graph(*args):
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_data = [
            go.Scatter(
                x=['CPU'],
                y=[cpu_usage],
                mode='lines+markers',
                name='CPU Usage'
            )
        ]
        cpu_layout = go.Layout(
            title='CPU Usage',
            xaxis=dict(title='Time'),
            yaxis=dict(title='Percent')
        )
        return {'data': cpu_data, 'layout': cpu_layout}
    except Exception as e:
        print(f'Error updating CPU graph: {e}')
        raise PreventUpdate

# 回调函数：获取内存使用情况
@app.callback(
    Output('memory-graph', 'figure'),
    [Input('hidden-div', 'children')]
)
def update_memory_graph(*args):
    try:
        memory = psutil.virtual_memory()
        memory_data = [
            go.Bar(
                x=['Used', 'Available'],
                y=[memory.used / (1024 * 1024 * 1024), memory.available / (1024 * 1024 * 1024)],
                marker_color=['blue', 'green']
            )
        ]
        memory_layout = go.Layout(
            title='Memory Usage',
            xaxis=dict(title='Memory'),
            yaxis=dict(title='GB')
        )
        return {'data': memory_data, 'layout': memory_layout}
    except Exception as e:
        print(f'Error updating memory graph: {e}')
        raise PreventUpdate

# 回调函数：获取磁盘使用情况
@app.callback(
    Output('disk-graph', 'figure'),
    [Input('hidden-div', 'children')]
)
def update_disk_graph(*args):
    try:
        disk_usage = psutil.disk_usage('/')
        disk_data = [
            go.Bar(
                x=['Used', 'Available'],
                y=[disk_usage.used / (1024 * 1024 * 1024), disk_usage.free / (1024 * 1024 * 1024)],
                marker_color=['red', 'green']
            )
        ]
        disk_layout = go.Layout(
            title='Disk Usage',
            xaxis=dict(title='Disk'),
            yaxis=dict(title='GB')
        )
        return {'data': disk_data, 'layout': disk_layout}
    except Exception as e:
        print(f'Error updating disk graph: {e}')
        raise PreventUpdate

# 回调函数：获取网络使用情况
@app.callback(
    Output('network-graph', 'figure'),
    [Input('hidden-div', 'children')]
)
def update_network_graph(*args):
    try:
        network_io = psutil.net_io_counters()
        network_data = [
            go.Bar(
                x=['Sent', 'Received'],
                y=[network_io.bytes_sent / (1024 * 1024), network_io.bytes_recv / (1024 * 1024)],
                marker_color=['blue', 'orange']
            )
        ]
        network_layout = go.Layout(
            title='Network I/O',
            xaxis=dict(title='Network'),
            yaxis=dict(title='MB')
        )
        return {'data': network_data, 'layout': network_layout}
    except Exception as e:
        print(f'Error updating network graph: {e}')
        raise PreventUpdate

# 定时更新图表
@app.callback(
    Output('hidden-div', 'children'),
    [dash.dependencies.Input('cpu-graph', 'id'),
     dash.dependencies.Input('memory-graph', 'id'),
     dash.dependencies.Input('disk-graph', 'id'),
     dash.dependencies.Input('network-graph', 'id')],
    prevent_initial_call=True
)
def update_graphs(*args):
    pass  # 无需返回任何内容

# 运行 Dash 应用
if __name__ == '__main__':
    app.run_server(debug=True)