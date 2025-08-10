# 代码生成时间: 2025-08-10 23:28:20
import os
import re
from celery import Celery
from celery.utils.log import get_task_logger

# 配置Celery
app = Celery('batch_file_renamer')
app.config_from_object('celeryconfig')

# 获取任务日志记录器
logger = get_task_logger(__name__)

# 定义文件重命名任务
@app.task
def rename_files(file_directory, pattern, replacement):
    '''
    批量重命名文件任务
    :param file_directory: 文件目录
    :param pattern: 正则表达式匹配模式
    :param replacement: 替换模式
    '''
    try:
        # 遍历指定目录下的所有文件
        for filename in os.listdir(file_directory):
            # 检查文件是否符合正则表达式模式
            if re.search(pattern, filename):
                # 构建新文件名
                new_filename = re.sub(pattern, replacement, filename)
                # 构建旧文件和新文件的完整路径
                old_file_path = os.path.join(file_directory, filename)
                new_file_path = os.path.join(file_directory, new_filename)
                # 重命名文件
                os.rename(old_file_path, new_file_path)
                logger.info(f'Renamed {filename} to {new_filename}')
        logger.info('File renaming completed successfully.')
    except FileNotFoundError:
        logger.error(f'Directory {file_directory} not found.')
        raise
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        raise

# 用法示例
if __name__ == '__main__':
    # 配置Celery
    app.conf.broker_url = 'amqp://guest@localhost//'
    app.conf.result_backend = 'rpc://'
    
    # 调用重命名任务
    # 假设我们要将'/path/to/files'目录下所有以'old_name'开头的文件
    # 重命名为以'new_name'开头
    rename_files.delay('/path/to/files', r'^old_name', 'new_name')
