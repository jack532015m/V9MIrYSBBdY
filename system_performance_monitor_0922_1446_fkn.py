# 代码生成时间: 2025-09-22 14:46:31
import psutil
from celery import Celery
from datetime import datetime

# 配置Celery
app = Celery('system_performance_monitor', broker='pyamqp://guest@localhost//')

# 定义监控任务
@app.task
def monitor_system_performance():
    """监控系统性能，收集CPU和内存使用情况。
    """
    try:
        # 收集CPU使用率
        cpu_usage = psutil.cpu_percent(interval=1)
        # 收集内存使用情况
        memory = psutil.virtual_memory()
        memory_usage = memory.percent

        # 记录监控结果
        performance_data = {
            'timestamp': datetime.now().isoformat(),
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage
        }
        print(f"System Performance Data: {performance_data}")
        # 可以将数据保存到文件或数据库

        # 返回监控结果
        return performance_data
    except Exception as e:
        # 错误处理
        print(f"Error monitoring system performance: {str(e)}")
        raise

# 以下是如何使用这个任务的例子
if __name__ == '__main__':
    # 定期执行性能监控任务
    monitor_system_performance.apply_async()
    # 你可以使用定时器或其他调度工具来定期执行此任务
    # 例如使用APScheduler或Celery的定时任务功能
