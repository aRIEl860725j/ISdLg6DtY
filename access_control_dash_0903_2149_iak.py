# 代码生成时间: 2025-09-03 21:49:47
import dash
import dash_auth
from dash import html, dcc
from dash.dependencies import Input, Output
from flask import session

# 设置配置参数
config = {
    "routes_pathname_prefix": "/app/"
}

# 定义Dash应用
app = dash.Dash(__name__, **config)

# 使用dash_auth进行访问控制
auth = dash_auth.BasicAuth(
    app,
    "访问控制示例",
    # 定义用户认证信息
    {
        "admin": "admin",
        "user": "user"
    }
)

# 定义布局
app.layout = html.Div(children=[
    html.H1("访问权限控制示例"),
    html.P("这是一个受保护的页面."),
    dcc.Link("返回首页", href="/")
])

# 定义回调函数，用于刷新会话信息
@app.callback(
    Output("output-container", "children"),
    [Input("interval-component", "n_intervals")]
)
def update_metrics(n):
    # 这里可以添加一些业务逻辑，例如根据会话信息显示不同内容
    if 'user_name' in session:
        user_name = session['user_name']
        return f"Hello, {user_name}!"
    else:
        return "请登录"

# 定义回调函数，用于登录
@app.callback(
    Output("login-output", "children"),
    [Input("login-button", "n_clicks")],
    [State("username-input", "value"), State("password-input", "value")]
)
def login(n_clicks, username, password):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    if username == "admin" and password == "admin":
        session['user_name'] = "admin"
        return "管理员登录成功"
    elif username == "user" and password == "user":
        session['user_name'] = "user"
        return "用户登录成功"
    else:
        return "用户名或密码错误"

# 启动服务器
if __name__ == '__main__':
    app.run_server(debug=True)