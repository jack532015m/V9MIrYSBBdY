# 代码生成时间: 2025-07-31 11:08:39
import os
from celery import Celery
from celery.utils.log import get_task_logger
import shutil

# 配置Celery
app = Celery('batch_file_renamer', broker='pyamqp://guest@localhost//')
app.conf.update(
    result_backend='rpc://',
)
logger = get_task_logger(__name__)


# 定义任务：批量重命名文件
@app.task(name='batch_file_renamer.rename_files', bind=True)
def rename_files(self, directory, prefix, suffix, ext):
    """
    批量重命名指定目录下的文件
    :param directory: 文件夹路径
    :param prefix: 新文件名前缀
    :param suffix: 新文件名后缀
    :param ext: 文件扩展名
    :return: None
    """
    try:
        # 检查目录是否存在
        if not os.path.isdir(directory):
            logger.error('Directory does not exist: {}'.format(directory))
            raise FileNotFoundError('Directory does not exist')

        # 准备文件名模板
        file_name_template = '{}{:04d}.{}'.format(prefix, '{{:04d}}', ext)

        # 重命名文件
        for i, filename in enumerate(sorted(os.listdir(directory)), 1):
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, file_name_template.format(i))
            if os.path.isfile(old_file_path):
                shutil.move(old_file_path, new_file_path)
                logger.info('Renamed file {} to {}'.format(old_file_path, new_file_path))
            else:
                logger.debug('Skipping non-file: {}'.format(old_file_path))

    except FileNotFoundError as e:
        logger.error(e)
        self.retry(exc=e)
    except Exception as e:
        logger.error('An error occurred: {}'.format(e))
        self.retry(exc=e)


# 示例用法
# 这里仅作为文档说明，不作为实际代码执行部分
# directory = '/path/to/your/directory'
# rename_files.apply_async(args=[directory, 'newfile_', 'txt', 'txt'], countdown=10)  # 10秒后执行