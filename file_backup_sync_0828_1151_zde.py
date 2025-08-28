# 代码生成时间: 2025-08-28 11:51:48
import os
import shutil
from celery import Celery
from celery.utils.log import get_task_logger

# 配置Celery
app = Celery('file_backup_sync', broker='pyamqp://guest@localhost//')

# 获取日志记录器
logger = get_task_logger(__name__)

def backup_file(source, destination):
    """备份文件函数，将源文件复制到目标路径"""
    try:
        shutil.copy2(source, destination)
        return f"File {source} backed up successfully to {destination}"
    except IOError as e:
        logger.error(f"An error occurred while backing up file {source}: {e}")
        raise Exception(f"Failed to back up file {source}")

@app.task
def sync_directory(source_dir, destination_dir):
    """同步目录函数，将源目录的文件同步到目标目录"""
    try:
        # 确保目标目录存在
        os.makedirs(destination_dir, exist_ok=True)
        # 遍历源目录中的文件
        for filename in os.listdir(source_dir):
            source_file = os.path.join(source_dir, filename)
            destination_file = os.path.join(destination_dir, filename)
            # 同步单个文件
            backup_file(source_file, destination_file)
        return f"All files in {source_dir} synced to {destination_dir}"
    except Exception as e:
        logger.error(f"An error occurred while syncing directory {source_dir}: {e}")
        raise Exception(f"Failed to sync directory {source_dir}")

# 设置Celery配置
app.conf.update(
    result_expires=3600,  # 任务结果过期时间，单位为秒
    task_serializer='json',  # 任务序列化方式
    accept_content=['json'],  # 接受的任务内容类型
    timezone='UTC',  # 时区设置
    enable_utc=True
)

if __name__ == '__main__':
    # 启动Celery worker
    app.start()
