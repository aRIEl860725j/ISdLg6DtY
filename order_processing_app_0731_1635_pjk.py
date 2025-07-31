# 代码生成时间: 2025-07-31 16:35:39
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from dash.exceptions import PreventUpdate
from dash import no_update

# 定义一个简单的订单处理应用
app = dash.Dash(__name__)

# 假设有一个订单数据框，这里我们使用一个示例数据框
df = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5],
    "customer_name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "order_status": ["pending", "shipped", "delivered", "cancelled", "pending"],
    "order_date": pd.date_range(start="2023-01-01", periods=5)
})

# 应用布局
app.layout = html.Div([
    html.H1("Order Processing Application"),
    dcc.Table(
        id='order-table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action='native',
        sort_action='native',
        sort_mode='multi',
        column_selectable='multi',
        row_selectable='single',
        row_deletable=True,
        ),
    html.Div(id='output-container'),
])

# 回调，当订单状态更改时更新表格
@app.callback(
    Output('order-table', 'data'),
    Input('order-table', 'active_cell'),
    Input('order-table', 'columns'),
    Input('order-table', 'selected_rows'),
    prevent_initial_call=True,
)
def update_order_status(active_cell, columns, selected_rows):
    # 如果没有选中的行，不执行任何操作
    if not selected_rows:
        raise PreventUpdate

    # 获取选中行的索引和列
    row_index = selected_rows[0]
    column_name = columns[active_cell['column']].id

    # 获取当前的订单状态并更改它
    current_status = df.loc[row_index, 'order_status']
    if current_status == 'pending':
        new_status = 'shipped'
    elif current_status == 'shipped':
        new_status = 'delivered'
    elif current_status == 'delivered':
        new_status = 'completed'
    else:
        new_status = 'pending'

    # 更新数据框中的状态
    df.loc[row_index, 'order_status'] = new_status

    # 返回更新后的数据框记录
    return df.to_dict('records')

# 启动服务器
if __name__ == '__main__':
    app.run_server(debug=True)