# 代码生成时间: 2025-08-07 07:16:23
import os
import celery
from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from datetime import datetime, timedelta

# 配置Celery
os.environ.setdefault('CELERY_BROKER_URL', 'redis://localhost:6379/0')
os.environ.setdefault('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

app = Celery('tasks', broker=os.environ['CELERY_BROKER_URL'],
             backend=os.environ['CELERY_RESULT_BACKEND'])
app.conf.beat_schedule = {
    # 定时任务配置
    'run_every_10_seconds': {
        'task': 'tasks.my_periodic_task',
        'schedule': 10.0,  # 每10秒执行一次任务
    },
}

# 定义周期性任务
@periodic_task(run_every=(10.0), name='my_periodic_task')
def my_periodic_task():
    """
    定义一个周期性执行的任务。
    此函数将被定时任务调用。
    """
    try:
        # 这里可以放入需要定时执行的代码
        print(f"Periodic task executed at {datetime.now()}")
    except Exception as e:
        # 处理任务执行过程中可能出现的任何异常
        print(f"Error executing periodic task: {e}")

if __name__ == '__main__':
    # 启动Celery beat调度器
    app.start()
