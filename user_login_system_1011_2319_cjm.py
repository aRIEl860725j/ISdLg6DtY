# 代码生成时间: 2025-10-11 23:19:41
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from flask import session
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash

# 假设有一个用户数据文件，包含用户名和密码
users_df = pd.read_csv('users.csv')

# Dash应用程序
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('用户登录验证系统'),
    html.Div(
        children=[
            dcc.Input(id='username', type='text', placeholder='请输入用户名'),
            dcc.Input(id='password', type='password', placeholder='请输入密码'),
            html.Button('登录', id='login-button', n_clicks=0)
        ],
        style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}
    ),
    html.Div(id='login-message')
])

# 回调函数：用户登录验证
@app.callback(
    Output('login-message', 'children'),
    [Input('login-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value')]
)
def login(n_clicks, username, password):
    # 检查是否有点击事件
    if n_clicks == 0:
        return ''
    
    # 在users_df中查找用户名
    user = users_df[users_df['username'] == username]
    
    # 如果没有找到用户，返回错误信息
    if user.empty:
        return '用户名不存在'
    
    # 检查密码是否正确
    if check_password_hash(user.iloc[0]['password'], password):
        # 设置session信息
        session['username'] = username
        session['logged_in'] = True
        return '登录成功'
    else:
        return '密码错误'

# 运行应用程序
if __name__ == '__main__':
    app.run_server(debug=True)