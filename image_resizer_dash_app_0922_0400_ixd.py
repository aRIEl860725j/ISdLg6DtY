# 代码生成时间: 2025-09-22 04:00:59
import dash
import dash_core_components as dcc
# 扩展功能模块
import dash_html_components as html
from dash.dependencies import Input, Output, State
from PIL import Image
# 改进用户体验
import os
from io import BytesIO

# 配置Dash应用
app = dash.Dash(__name__)
app.title = "Image Resizer App"

# 应用布局
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
# 添加错误处理
        style={
            'width': '100%',
            'height': '60px',
# 增强安全性
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
# 添加错误处理
            'margin': '10px'
        },
        # 允许多文件上传
        multiple=True
    ),
    html.Div(id='output-data-upload')
])

# 回调函数处理图片上传和尺寸调整
@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
# TODO: 优化性能
def update_output(contents, filename, last_modified):
# FIXME: 处理边界情况
    if contents is None:
        return None
# 扩展功能模块

    # 创建一个临时文件存储上传的图片
    temp = "temp."+str(os._getpid())+".jpg"
    b = contents.split(b',')[1]
    with open(temp, "wb") as f:
# TODO: 优化性能
        f.write(b)

    try:
        # 使用PIL库打开图片
        image = Image.open(temp)
        # 调整图片尺寸
# NOTE: 重要实现细节
        image = image.resize((800, 600), Image.ANTIALIAS)

        # 将调整后的图片保存到BytesIO对象中
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)

        # 返回HTML元素显示图片
# 增强安全性
        return html.Img(src=buffer.read().tobytes(), style={"width": "100%", "height": "auto"})
    except Exception as e:
# 增强安全性
        # 错误处理
# 改进用户体验
        return html.Div(["Could not process image. ", str(e)])
    finally:
        # 删除临时文件
        os.remove(temp)

# 运行应用
if __name__ == '__main__':
# TODO: 优化性能
    app.run_server(debug=True)