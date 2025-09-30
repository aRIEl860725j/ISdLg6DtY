# 代码生成时间: 2025-10-01 02:14:30
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 机器学习模型训练器应用
class MachineLearningTrainer:

    def __init__(self):
        # 初始化Dash应用
        self.app = dash.Dash(__name__)
        self.app.layout = html.Div([
            html.H1('机器学习模型训练器'),
            dcc.Upload(
                id='upload-data',
                children=html.Div(['Drag and Drop or ',
                                 html.A('Select a file')]),
                style={'width': '50%', 'height': '60px', 'lineHeight': '60px',
                        'borderWidth': '1px', 'borderStyle': 'dashed',
                        'borderRadius': '5px', 'textAlign': 'center',
                        'margin': '10px'},
                # 允许上传的文件类型
                accept='.csv'
            ),
            html.Div(id='output-data-upload'),
            html.Div(id='output-model'),
        ])

    # 上传文件并显示数据
    @staticmethod
    def load_and_display_data(uploaded_file):
        if uploaded_file is None:
            return None

        # 读取并转换文件内容为DataFrame
        df = pd.read_csv(uploaded_file)

        # 显示数据前几行
        return df.head().to_dict('records')

    # 训练模型并显示结果
    @staticmethod
    def train_and_display_model(df):
        if df is None:
            return None

        # 假设目标变量列名为'y'，特征变量列名为'x'
        X = df[['x']]  # 特征变量
        y = df['y']    # 目标变量

        # 划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 创建线性回归模型
        model = LinearRegression()

        # 训练模型
        model.fit(X_train, y_train)

        # 预测测试集
        y_pred = model.predict(X_test)

        # 计算模型评估指标
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # 返回模型评估结果
        return {'mse': mse, 'r2': r2}

    # 回调函数来处理文件上传并显示数据
    @staticmethod
    @app.callback(
        Output('output-data-upload', 'children'),
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename')]
    )
def display_data_on_upload(
        input_contents, input_filename):
        # 读取文件内容并显示数据
        if input_contents is not None:
            return MachineLearningTrainer.load_and_display_data(input_contents)
        return None

    # 回调函数来训练模型并显示结果
    @staticmethod
    @app.callback(
        Output('output-model', 'children'),
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename')]
    )
def display_model_on_upload(
        input_contents, input_filename):
        # 读取文件内容并训练模型
        if input_contents is not None:
            df = pd.read_csv(input_contents)
            return MachineLearningTrainer.train_and_display_model(df)
        return None

# 运行Dash应用
def run_app():
    app = MachineLearningTrainer()
    app.app.run_server(debug=True)

# 程序入口点
def main():
    run_app()

if __name__ == '__main__':
    main()