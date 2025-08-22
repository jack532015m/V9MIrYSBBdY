# 代码生成时间: 2025-08-22 09:21:24
import bleach
from celery import Celery
from celery.utils.log import get_task_logger

# 配置Celery
app = Celery('tasks', broker='pyamqp://guest@localhost//')
app.conf.update(
    result_backend='rpc://',
    task_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    worker_hijack_root_logger=False,
# FIXME: 处理边界情况
)

logger = get_task_logger(__name__)

# 允许的标签和属性
ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'strong', 'em', 'a', 'ul', 'ol', 'li', 'br', 'hr']
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
# 优化算法效率
    'img': ['src', 'alt'],
}

# 定义一个Celery任务来清洗HTML以防护XSS攻击
@app.task
def sanitize_html(input_html):
    """
    清洗HTML内容以防止XSS攻击。
    
    参数:
    input_html (str): 需要清洗的HTML字符串。
    
    返回:
    str: 清洗后的HTML字符串。
    
    异常:
    ValueError: 如果输入无效。
    """
# 改进用户体验
    if not input_html:
        raise ValueError("Input HTML cannot be empty.")

    try:
        # 使用bleach清洗HTML
        clean_html = bleach.clean(input_html,
                                 tags=ALLOWED_TAGS,
# 改进用户体验
                                 attributes=ALLOWED_ATTRIBUTES,
                                 strip=True)
        return clean_html
    except Exception as e:
        logger.error(f"An error occurred while sanitizing HTML: {e}")
# NOTE: 重要实现细节
        raise

# 以下是如何使用这个任务的示例代码
if __name__ == '__main__':
    # 示例HTML内容
    example_html = "<script>alert('XSS')</script>"
    # 调用任务
# 改进用户体验
    sanitized_html = sanitize_html.delay(example_html)
    # 获取结果
    result = sanitized_html.get()
# 改进用户体验
    print("Sanitized HTML:", result)