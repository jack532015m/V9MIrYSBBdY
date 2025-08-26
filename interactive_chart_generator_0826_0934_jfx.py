# 代码生成时间: 2025-08-26 09:34:20
# 导入必要的库
import os
from celery import Celery
from flask import Flask, request, jsonify
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.layouts import column
from bokeh.io import curdoc

# 初始化Flask应用
app = Flask(__name__)

# 初始化Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# 定义一个生成交互式图表的任务
@celery.task
def generate_chart(data, title, x_axis_label, y_axis_label):
    # 创建一个图表对象
    p = figure(title=title, x_axis_label=x_axis_label, y_axis_label=y_axis_label)
    
    # 将数据添加到图表中
    source = ColumnDataSource(data)
    p.circle(x='x', y='y', source=source)
    
    # 输出图表到HTML文件
    output_file(title + ".html")
    show(p)
    
    # 返回图表的HTML和JavaScript代码
    return components(p)

# 定义一个Flask路由，用于接收图表生成请求
@app.route('/generate_chart', methods=['POST'])
def chart_generator():
    # 获取请求数据
    data = request.get_json()
    
    # 检查请求数据是否完整
    if not all(key in data for key in ['data', 'title', 'x_axis_label', 'y_axis_label']):
        return jsonify({'error': 'Invalid request data'}), 400
    
    # 生成图表
    chart_html, chart_js = generate_chart.delay(data['data'], data['title'], data['x_axis_label'], data['y_axis_label']).get()
    
    # 返回图表的HTML和JavaScript代码
    return jsonify({'chart_html': chart_html, 'chart_js': chart_js})

# 定义一个Flask路由，用于启动Flask应用
@app.route('/')
def index():
    return 'Interactive Chart Generator is running...'

# 运行Flask应用
if __name__ == '__main__':
    app.run(debug=True)
