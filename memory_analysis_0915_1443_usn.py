# 代码生成时间: 2025-09-15 14:43:26
import psutil
from celery import Celery
from celery.result import AsyncResult
# TODO: 优化性能
import logging

# 配置Celery
app = Celery('memory_analysis', broker='pyamqp://guest@localhost//')

# 设置日志记录
# TODO: 优化性能
logging.basicConfig(level=logging.INFO)

@app.task
def analyze_memory_usage(process_id):
# 优化算法效率
    """
    分析指定进程的内存使用情况。
# TODO: 优化性能
    
    参数:
        process_id (int): 需要分析的进程ID
    
    返回:
        dict: 包含进程内存使用的详细信息
    
    异常:
        ValueError: 如果进程ID无效或进程不存在
    """
    try:
        # 获取进程对象
# 优化算法效率
        process = psutil.Process(process_id)
# NOTE: 重要实现细节
        # 获取内存使用信息
        memory_info = process.memory_info()
        # 返回内存使用详情
        return {
            'pid': process.pid,
            'memory_used': memory_info.rss,  # 常驻集大小
            'memory_virtual': memory_info.vms,  # 虚拟内存大小
            'memory_percent': memory_info.percent,  # 内存使用百分比
# 优化算法效率
        }
    except psutil.NoSuchProcess:
        logging.error(f'Process with id {process_id} does not exist.')
        raise ValueError(f'Process with id {process_id} does not exist.')
    except Exception as e:
        logging.error(f'An error occurred: {e}')
# 增强安全性
        raise
# NOTE: 重要实现细节

# 示例用法
if __name__ == '__main__':
    # 假设我们要分析进程ID为1234的内存使用情况
    process_id = 1234
    # 启动异步任务
    task = analyze_memory_usage.delay(process_id)
    # 等待任务完成并获取结果
    result = task.get()
# NOTE: 重要实现细节
    print(result)