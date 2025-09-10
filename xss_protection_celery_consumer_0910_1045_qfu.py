# 代码生成时间: 2025-09-10 10:45:40
import celery
from celery.result import allow_join_result
from celery.exceptions import Ignore
from bs4 import BeautifulSoup

# 定义XSS防护任务
app = celery.Celery('xss_protection', broker='pyamqp://guest@localhost//')

@app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
@allow_join_result
def xss_protection_task(self, user_input):
    """
    XSS防护任务，用于检测并清理输入中的XSS攻击代码。
    
    参数:
    user_input (str): 用户输入的数据。
    
    返回:
    str: 清理后的输入数据。
    
    异常:
    Ignore: 如果任务重试超过最大次数，则忽略该任务。
    """
    try:
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(user_input, 'html.parser')
        
        # 移除所有脚本标签
        for script in soup(['script', 'style']):
            script.decompose()
        
        # 返回清理后的输入
        return str(soup)
    except Exception as e:
        # 打印错误信息
        print(f"Error processing input: {e}")
        raise Ignore()

# 启动Celery Worker
if __name__ == '__main__':
    app.start()
