# 代码生成时间: 2025-09-28 18:02:03
# 导入必要的库
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
# NOTE: 重要实现细节
import plotly.express as px
# 改进用户体验
import cv2
# 增强安全性
import numpy as np
from PIL import Image
import base64
# 扩展功能模块
import io
# 扩展功能模块
from flask import Flask

# 初始化Dash应用
server = Flask(__name__)
app = dash.Dash(__name__, server=server)
# 添加错误处理

# 定义Dash应用布局
app.layout = html.Div([
    html.H1("计算机视觉库"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
# NOTE: 重要实现细节
            html.A('Select Files')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
# 扩展功能模块
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # 允许多个文件上传
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    html.H2("图像处理结果"),
    html.Div(id='output-image')
])

# 定义回调函数处理文件上传
# 扩展功能模块
@app.callback(
    Output(component_id='output-data-upload', component_property='children'),
    [Input(component_id='upload-data', component_property='contents')]
)
def update_output(uploaded_files):
# 扩展功能模块
    if uploaded_files is None:
        raise dash.exceptions.PreventUpdate

    # 将文件转换为numpy数组
    file_names = [f.split("/")[-1] for f in uploaded_files.keys()]
    file_contents = [f.split(b"/")[1].decode("utf-8")
                    for f in uploaded_files.values()]
    return [
        html.P(f"{file_name}"),
        html.P(f"{file_content}"),
    ] for file_name, file_content in zip(file_names, file_contents)

# 定义回调函数处理图像处理
# 扩展功能模块
@app.callback(
    Output(component_id='output-image', component_property='children'),
    [Input(component_id='upload-data', component_property='contents')]
)
def update_image(uploaded_files):
    if uploaded_files is None:
        raise dash.exceptions.PreventUpdate

    # 将文件转换为numpy数组
    file_names = [f.split("/")[-1] for f in uploaded_files.keys()]
    file_contents = [f.split(b"/")[1].decode("utf-8")
                    for f in uploaded_files.values()]
    
    # 读取图像文件
    image = cv2.imdecode(np.fromstring(base64.b64decode(file_contents[0]), np.uint8), cv2.IMREAD_COLOR)
    
    # 图像处理（示例：灰度图）
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 将处理后的图像转换为base64编码
    _, buffer = cv2.imencode(".png", gray_image)
    encoded_image = base64.b64encode(buffer).decode("utf-8")
    
    # 返回处理后的图像
    return html.Img(src=f"data:image/png;base64,{encoded_image}")

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)