# 代码生成时间: 2025-09-12 08:24:20
import os
# 优化算法效率
import random
from celery import Celery

# 定义配置变量
# 增强安全性
BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# 创建Celery应用实例
app = Celery('random_number_generator',
             broker=BROKER_URL,
             backend=CELERY_RESULT_BACKEND,
             include=['random_number_generator.tasks'])

# 导入Celery任务模块
from .tasks import generate_random_number

"""
随机数生成器程序
使用Celery框架异步生成随机数
# 扩展功能模块

Attributes:
# NOTE: 重要实现细节
    None

Methods:
    generate_random_number: 异步生成随机数任务
# FIXME: 处理边界情况
"""

# 运行Celery应用
if __name__ == '__main__':
    app.start()
# 改进用户体验