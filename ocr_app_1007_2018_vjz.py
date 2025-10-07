# 代码生成时间: 2025-10-07 20:18:35
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import base64
import io
import cv2
import pytesseract
from PIL import Image

def ocr_image(image_path):
    """执行OCR识别，返回识别结果"""
    # 读取图片文件
    image = Image.open(image_path)
    # 使用pytesseract识别图片中的文字
    text = pytesseract.image_to_string(image)
    return text

# 创建Dash应用
app = dash.Dash(__name__)
app.layout = html.Div([
    # 上传图片组件
    dcc.Upload(
        id='image-upload',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select a file')
        ]),
        style={'width': '100%', 'height': '60px', 'lineHeight': '60px',
               'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
               'textAlign': 'center', 'margin': '10px'},
    ),
    # 文本区域显示识别结果
    html.Div(id='output-data-upload')
])

# 回调函数处理图片上传和OCR识别
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('image-upload', 'contents')],
    [State('image-upload', 'filename')])
def update_output(contents, filename):
    """处理上传的图片并显示OCR识别结果"""
    if contents is None or filename is None:
        raise PreventUpdate()
    """检查文件是否为空"""
    if not contents:
        return 'No file selected or file is empty'
    """将上传的图片文件转换为PIL Image对象"""
    image = Image.open(io.BytesIO(contents.getbuffer()))
    try:
        """执行OCR识别"""
        result = ocr_image(image)
        return html.Div([
            html.H5(filename),
            html.Hr(),
            html.P(result)
        ])
    except Exception as e:
        """错误处理"""
        return f'An error occurred: {str(e)}'

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)