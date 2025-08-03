# 代码生成时间: 2025-08-03 18:43:41
import dash\
import dash_core_components as dcc\
import dash_html_components as html\
from dash.dependencies import Input, Output\
import plotly.express as px\
from dash.exceptions import PreventUpdate\

# 定义排序算法函数\
def bubble_sort(data):
    """实现冒泡排序算法"""
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data
\

def quick_sort(data):
    """实现快速排序算法"""
    if len(data) <= 1:
        return data
    else:
        pivot = data[0]
        less = [x for x in data[1:] if x <= pivot]
        greater = [x for x in data[1:] if x > pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)

# 定义Dash应用
def create_sorting_app():
    app = dash.Dash(__name__)
    app.layout = html.Div([
        html.H1("Sorting Algorithm App"),
        dcc.Textarea(id="input-data",\         placeholder="Enter numbers separated by commas"),
        html.Button("Sort", id="sort-button", n_clicks=0),
        html.Div(id="output-data")
    ])
    
    @app.callback(
        Output("output-data", "children"),
        [Input("sort-button", "n_clicks")],
        [State("input-data", "value"), State("sort-button", "n_clicks")])
    def sort_data(n_clicks, input_data, n_clicks2):
        """处理排序操作"""
        if n_clicks is None or n_clicks2 is None:
            raise PreventUpdate
        
        try:
            # 将输入数据转换为整数列表
            data = [int(x.strip()) for x in input_data.split(",")]
        except ValueError:
            return "Invalid input. Please enter numbers separated by commas."
        
        # 选择排序算法
        if input_data.startswith("bubble"):
            sorted_data = bubble_sort(data)
        elif input_data.startswith("quick"):
            sorted_data = quick_sort(data)
        else:
            raise ValueError("Invalid sort algorithm. Please specify 'bubble' or 'quick'.")
        
        return "Sorted data: " + ", ".join(map(str, sorted_data))
    
    return app

# 运行Dash应用
def main():
    app = create_sorting_app()
    app.run_server(debug=True)

if __name__ == "__main__":
    main()