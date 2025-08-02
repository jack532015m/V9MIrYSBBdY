# 代码生成时间: 2025-08-02 13:45:53
import os
import celery
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
from celery.signals import task_failure
from kombu import Queue

# 配置Celery
os.environ.setdefault('CELERY_BROKER_URL', 'amqp://guest:guest@localhost//')
app = Celery('message_notification_system',
             broker='amqp://guest:guest@localhost//',
             backend='rpc://')

# 设置任务默认配置
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    result_expires=3600,
    broker_url='amqp://guest:guest@localhost//',
)

# 定义错误处理信号
@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, **kwargs):
    """处理任务失败的情况"""
    print(f'Task {task_id} failed with exception: {exception}')

# 发送消息的任务
@app.task(bind=True, soft_time_limit=60)
def send_message(self, message, recipient):
    """发送消息给指定接收者
    
    参数:
        message (str): 要发送的消息内容
        recipient (str): 接收者邮箱地址
    
    返回:
        bool: 消息发送成功返回True，失败返回False
    """
    try:
        # 这里模拟发送消息的过程
        print(f'Sending message to {recipient}: {message}')
        return True
    except Exception as e:
        # 记录错误信息
        print(f'Error sending message to {recipient}: {e}')
        return False

# 启动Celery Worker
if __name__ == '__main__':
    app.start()
