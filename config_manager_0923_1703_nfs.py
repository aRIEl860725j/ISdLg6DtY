# 代码生成时间: 2025-09-23 17:03:12
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import json
import os

# 配置文件管理器
class ConfigManager:
    def __init__(self, config_file):
        """
        初始化配置文件管理器
        :param config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        """
        加载配置文件
        :return: 配置数据
        """
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("配置文件不存在")
            return {}
        except json.JSONDecodeError:
            print("配置文件格式错误")
            return {}

    def save_config(self, new_data):
        """
        保存配置数据
        :param new_data: 新的配置数据
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(new_data, f, indent=4)
        except Exception as e:
            print(f"保存配置文件失败: {e}")

    def update_config(self, key, value):
        """
        更新配置数据
        :param key: 配置项键
        :param value: 配置项值
        """
        if key in self.config_data:
            self.config_data[key] = value
            self.save_config(self.config_data)
        else:
            print(f"配置项 '{key}' 不存在")

    def get_config(self, key):
        """
        获取配置数据
        :param key: 配置项键
        :return: 配置项值
        """
        return self.config_data.get(key)

# 创建DASH应用
app = dash.Dash(__name__)

# 设置DASH应用布局
app.layout = html.Div([
    html.H1("配置文件管理器"),
    dcc.Input(id='config-key', type='text', placeholder='配置项键'),
    dcc.Input(id='config-value', type='text', placeholder='配置项值'),
    html.Button('更新配置', id='update-config-btn', n_clicks=0),
    html.Div(id='result')
])

# 定义回调函数
@app.callback(
    Output('result', 'children'),
    [Input('update-config-btn', 'n_clicks')],
    [State('config-key', 'value'), State('config-value', 'value')]
)
def update_config(n_clicks, key, value):
    if n_clicks > 0:
        manager = ConfigManager('config.json')
        manager.update_config(key, value)
        return f'配置项 {key} 更新为 {value}'
    return ''

# 运行DASH应用
if __name__ == '__main__':
    app.run_server(debug=True)