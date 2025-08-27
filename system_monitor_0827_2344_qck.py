# 代码生成时间: 2025-08-27 23:44:16
import os
import psutil
from celery import Celery

# 初始化Celery应用
app = Celery('system_monitor', broker='pyamqp://guest@localhost//')

# 定义系统信息监控任务
@app.task
def monitor_system_performance():
    """监控系统性能并返回结果"""
    try:
        # 获取CPU使用率
        cpu_usage = psutil.cpu_percent(interval=1)
        # 获取内存使用情况
        memory = psutil.virtual_memory()
        # 获取磁盘使用情况
        disk_usage = psutil.disk_usage('/')
        # 获取网络信息
        network_io = psutil.net_io_counters()
        
        # 构建系统性能报告
        report = {
            'cpu_usage': cpu_usage,
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'free': memory.free
            },
            'disk_usage': {
                'total': disk_usage.total,
                'used': disk_usage.used,
                'free': disk_usage.free,
                'percent': disk_usage.percent
            },
            'network_io': {
                'bytes_sent': network_io.bytes_sent,
                'bytes_recv': network_io.bytes_recv
            }
        }
        return report
    except Exception as e:
        # 处理异常情况
        return f"Error monitoring system performance: {str(e)}"

# 定义一个简单的调度器，每10秒执行一次监控任务
if __name__ == '__main__':
    while True:
        report = monitor_system_performance.delay()
        # 等待任务完成
        result = report.get()
        print(result)
        # 休眠10秒
        import time
        time.sleep(10)