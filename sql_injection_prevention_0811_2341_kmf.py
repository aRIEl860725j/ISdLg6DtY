# 代码生成时间: 2025-08-11 23:41:40
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import sqlite3
from contextlib import contextmanager

# 使用上下文管理器来管理数据库连接
@contextmanager
def get_db_connection():
    db = sqlite3.connect('database.db')  # 假设数据库文件名为 database.db
    try:
        yield db
    finally:
        db.close()

# 预防SQL注入的函数
def safe_query(db, query, params):  # 使用参数化查询来防止SQL注入
    cursor = db.cursor()
    cursor.execute(query, params)
    return cursor

# Dash应用程序的主体部分
app = dash.Dash(__name__)

# 定义应用界面
app.layout = html.Div(children=[
    html.H1('防止SQL注入的Dash应用'),
    dcc.Input(id='input-box', type='text', placeholder='输入查询条件'),
    html.Button('查询', id='query-button', n_clicks=0),
    html.Div(id='output-container')
])

# 事件回调：查询按钮点击后执行
@app.callback(
    Output('output-container', 'children'),
    [Input('query-button', 'n_clicks')],
    [State('input-box', 'value')]
)
def update_output(n_clicks, input_value):  # 使用输入值作为参数
    if n_clicks == 0:  # 如果按钮没有被点击，则不执行查询
        return '请先点击查询按钮'
    try:
        with get_db_connection() as db:  # 使用上下文管理器获取数据库连接
            query = 'SELECT * FROM users WHERE name = ?'  # 假设要查询的表名为users，字段名为name
            # 使用safe_query函数执行参数化查询
            cursor = safe_query(db, query, (input_value,))
            results = cursor.fetchall()  # 获取查询结果
            return html.Ul([html.Li(f"Name: {row[0]}, Age: {row[1]}") for row in results])
    except Exception as e:  # 错误处理
        return f'查询出错：{str(e)}'

if __name__ == '__main__':
    app.run_server(debug=True)