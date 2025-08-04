# 代码生成时间: 2025-08-04 15:28:27
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API响应格式化工具
"""

import json
from celery import Celery

# 定义Celery实例
app = Celery('api_response_formatter',
              broker='pyamqp://guest@localhost//',
              backend='rpc://')


@app.task
def format_response(data):
    """
    格式化API响应数据
    
    参数:
    data (dict): 需要格式化的API响应数据
    
    返回:
    str: 格式化后的JSON字符串
    
    异常:
    ValueError: 当输入的数据不是字典时抛出异常
    """
    if not isinstance(data, dict):
        raise ValueError("输入的数据必须是字典")
    
    # 添加额外的响应字段
    formatted_data = {
        "status": "success",
        "message": "请求成功",
        "data": data
    }
    
    # 将字典转换为JSON字符串
    return json.dumps(formatted_data, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    """
    测试代码
    """
    # 模拟API响应数据
    sample_data = {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    }
    
    # 调用format_response函数并打印结果
    try:
        result = format_response(sample_data)
        print("格式化后的响应：", result)
    except ValueError as e:
        print("错误：", e)