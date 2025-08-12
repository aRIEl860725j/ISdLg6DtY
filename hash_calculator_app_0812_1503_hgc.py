# 代码生成时间: 2025-08-12 15:03:39
import hashlib
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# 定义一个哈希函数
def calculate_hash(text: str, method: str) -> str:
    """
    计算给定文本的哈希值。

    参数:
        text (str): 需要计算哈希的文本。
        method (str): 哈希算法方法。

    返回:
        str: 计算后的哈希值。
    """
    hasher = getattr(hashlib, method)()
    hasher.update(text.encode('utf-8'))
    return hasher.hexdigest()

# 初始化Dash应用
app = dash.Dash(__name__)

# 设置Dash应用的布局
app.layout = html.Div(children=[
    html.H1('哈希值计算工具'),
    dcc.Textarea(
        id='input-text',
        placeholder='请输入文本...',
        debounce=True
    ),
    html.Div(id='output-container'),
    dcc.Dropdown(
        id='hash-method',
        options=[{'label': 'MD5', 'value': 'md5'},
                 {'label': 'SHA1', 'value': 'sha1'},
                 {'label': 'SHA256', 'value': 'sha256'}],
        value='md5',
        multi=False
    )
])

# 定义回调函数
@app.callback(
    Output('output-container', 'children'),
    [Input('input-text', 'value'), Input('hash-method', 'value')]
)
def calculate_hash_value(text: str, method: str) -> str:
    """
    当输入文本或选择不同的哈希方法时，计算哈希值。

    参数:
        text (str): 输入的文本。
        method (str): 选择的哈希方法。

    返回:
        str: 显示的哈希值。
    """
    if not text:
        return '请在上方输入文本。'
    try:
        return calculate_hash(text, method)
    except Exception as e:
        # 出现错误时返回错误信息
        return f'发生错误：{str(e)}'

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)