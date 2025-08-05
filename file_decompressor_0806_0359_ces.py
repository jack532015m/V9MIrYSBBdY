# 代码生成时间: 2025-08-06 03:59:36
import os
import zipfile
from celery import Celery
from celery.utils.log import get_task_logger

# 配置Celery
app = Celery('file_decompressor', broker='pyamqp://guest@localhost//')
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# 获取Celery任务的日志记录器
logger = get_task_logger(__name__)


@app.task(name='decompress_file', bind=True)
def decompress_file(self, file_path, output_dir):
    '''
    异步任务：解压文件到指定目录
    :param self: Celery任务实例
    :param file_path: 要解压的文件路径
    :param output_dir: 解压后文件存放的目录
    :return: 解压结果
    '''
    try:
        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 解压文件
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
            result = {'status': 'success', 'message': 'File decompressed successfully'}
        return result
    except Exception as e:
        logger.error(f'Error decompressing file: {e}')
        result = {'status': 'error', 'message': f'Failed to decompress file: {str(e)}'}
        return result

# 以下是使用示例，实际部署时不需要
if __name__ == '__main__':
    # 使用Celery配置的broker启动任务
    file_path = '/path/to/your/compressed/file.zip'
    output_dir = '/path/to/output/directory'
    result = decompress_file.delay(file_path, output_dir)
    print(result.get())  # 打印任务结果