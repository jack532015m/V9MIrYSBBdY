# 代码生成时间: 2025-08-16 16:10:14
import bleach
from celery import Celery
from celery.utils.log import get_task_logger
from celery.signals import task_failure

# 设置Celery
app = Celery('xss_protection',
             broker='pyamqp://guest@localhost//')
app.conf.update(
    result_expires=3600,  # 任务结果过期时间（秒）
    task_serializer='json',
    accept_content=['json'],  # 接受的任务内容类型
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    broker_transport_options={'max_retries': 3},
    worker_redirect_stdouts=True,
)

logger = get_task_logger(__name__)

# 定义任务失败信号处理器
@task_failure.connect
def task_failure_handler(sender=None, task_id=None, task=None, **kwargs):
    logger.error(f'Task {task_id} failed with {task.exception}.')

# 定义XSS防护函数
def xss_protection(content):
    """
    该函数通过bleach库来清理输入内容，移除潜在的XSS攻击代码。
    
    参数:
    content (str): 要清理的字符串内容。
    
    返回:
    str: 清理后的安全内容。
    """
    try:
        # bleach.clean()方法会移除或转义潜在的XSS代码
        safe_content = bleach.clean(content)
        return safe_content
    except Exception as e:
        logger.error(f'Failed to clean content: {e}')
        raise

# 将XSS防护函数封装为Celery任务
@app.task
def clean_content_task(content):
    """
    Celery任务，用于异步处理XSS防护。
    
    参数:
    content (str): 要清理的字符串内容。
    
    返回:
    str: 清理后的安全内容。
    """
    logger.info('Starting to clean content...')
    safe_content = xss_protection(content)
    logger.info('Content cleaned successfully.')
    return safe_content

# 启动Celery worker
if __name__ == '__main__':
    app.start()