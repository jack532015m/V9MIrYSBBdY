# 代码生成时间: 2025-09-13 04:21:19
import json
from celery import Celery
from flask import Flask, jsonify, request

# 创建Celery实例
app = Celery('api_response_formatter', broker='pyamqp://guest@localhost//')
app.conf.update(
    result_backend='rpc://',
    task_serializer='json',  # 指定任务序列化方式
    accept_content=['json'],  # 接受的内容类型
    timezone='UTC',  # 设置时区
    enable_utc=True,  # 启用UTC时区
)

# 创建Flask应用实例
flask_app = Flask(__name__)

# 定义API响应格式化任务
@app.task
def format_api_response(api_response, status_code=200):
    """
    格式化API响应
    
    参数:
    api_response - 原始API响应数据
    status_code - HTTP状态码，默认为200
    """
    try:
        # 尝试将API响应数据转换为JSON格式
        formatted_response = json.dumps(api_response, ensure_ascii=False)
        # 返回格式化后的响应
        return {'status_code': status_code, 'data': formatted_response}
    except json.JSONDecodeError as e:
        # 处理JSON解码错误
        return {'status_code': 400, 'error': 'Invalid JSON data', 'message': str(e)}

# 创建Flask路由处理函数
@flask_app.route('/api/format', methods=['POST'])
def format_response():
    """
    API路由处理函数，处理POST请求并将API响应数据发送到Celery任务进行格式化
    """
    try:
        # 获取请求数据
        api_response = request.json
        # 调用Celery任务
        result = format_api_response.delay(api_response)
        # 返回任务结果
        return jsonify(result.get(timeout=10)), 200
    except Exception as e:
        # 处理其他异常
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

# 运行Flask应用
if __name__ == '__main__':
    flask_app.run(debug=True)