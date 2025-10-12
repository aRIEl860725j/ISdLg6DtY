# 代码生成时间: 2025-10-13 00:00:27
import os
import subprocess
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# 定义软件包管理器类
class PackageManager:
    def __init__(self):
        # 初始化Dash应用
        self.app = Dash(__name__)
        self.app.layout = html.Div([
            html.H1("软件包管理器"),
            dcc.Input(id='package-name', type='text', placeholder='输入软件包名称'),
            html.Button('安装', id='install-button', n_clicks=0),
            html.Button('卸载', id='uninstall-button', n_clicks=0),
            html.Div(id='output')
        ])

    # 定义回调函数安装软件包
    @app.callback(
        Output('output', 'children'),
        [Input('install-button', 'n_clicks'),
         Input('package-name', 'value')
        ]
    )
    def install_package(n_clicks, package_name):
        if n_clicks and package_name:
            try:
                # 使用pip命令安装软件包
                subprocess.run(["pip", "install", package_name], check=True)
                return f'{package_name} 安装成功！'
            except subprocess.CalledProcessError as e:
                return f'安装失败：{e}'
        return ''

    # 定义回调函数卸载软件包
    @app.callback(
        Output('output', 'children'),
        [Input('uninstall-button', 'n_clicks'),
         Input('package-name', 'value')
        ]
    )
    def uninstall_package(n_clicks, package_name):
        if n_clicks and package_name:
            try:
                # 使用pip命令卸载软件包
                subprocess.run(["pip", "uninstall", package_name, "-y"], check=True)
                return f'{package_name} 卸载成功！'
            except subprocess.CalledProcessError as e:
                return f'卸载失败：{e}'
        return ''

    # 运行Dash应用
    def run(self):
        self.app.run_server(debug=True)

# 创建软件包管理器实例并运行
if __name__ == '__main__':
    package_manager = PackageManager()
    package_manager.run()