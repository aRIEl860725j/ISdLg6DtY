# 代码生成时间: 2025-09-24 15:45:02
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# 定义表单数据验证函数
def validate_form(input_dict):
    """
    验证表单数据的有效性。
    Args:
        input_dict (dict): 表单输入数据字典。
    Raises:
        PreventUpdate: 如果表单数据无效，则阻止更新。
    """
    errors = []
    if 'name' not in input_dict or not input_dict['name'].strip():
        errors.append('Name is required')
    if 'email' not in input_dict or '@' not in input_dict['email']:
        errors.append('Valid email is required')
    if 'age' in input_dict and not input_dict['age'].isdigit():
        errors.append('Age must be a number')
    
    if errors:
        raise PreventUpdate(f'Validation errors: {errors}')
    
# 创建Dash应用
app = dash.Dash(__name__)

app.layout = html.Div([
    # 表单输入组件
    dcc.Input(id='name', type='text', placeholder='Enter name'),
    dcc.Input(id='email', type='email', placeholder='Enter email'),
    dcc.Input(id='age', type='text', placeholder='Enter age'),
    html.Button('Submit', id='submit-button', n_clicks=0),

    # 用于显示验证结果的组件
    html.Div(id='output-container')
])

# 定义回调函数，处理表单提交事件
@app.callback(
    Output('output-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('name', 'value'), State('email', 'value'), State('age', 'value')],
)
def submit_form(n_clicks, name, email, age):
    """
    处理表单提交事件。
    Args:
        n_clicks (int): 提交按钮点击次数。
        name (str): 用户姓名。
        email (str): 用户邮箱。
        age (str): 用户年龄。
    Returns:
        str: 验证结果或表单数据。
    """
    if n_clicks == 0:
        raise PreventUpdate
    
    input_dict = {'name': name, 'email': email, 'age': age}
    try:
        validate_form(input_dict)
        return f'Form submitted successfully: {input_dict}'
    except PreventUpdate as e:
        return str(e)

if __name__ == '__main__':
    app.run_server(debug=True)