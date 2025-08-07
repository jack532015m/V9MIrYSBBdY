# 代码生成时间: 2025-08-07 23:31:23
import os
import zipfile
from celery import Celery

# 配置Celery
app = Celery('unzip_tool', broker='pyamqp://guest@localhost//')

# 异步任务：解压文件
@app.task
def unzip_file(zip_path, extract_to):
    """
    异步解压文件到指定目录。
    :param zip_path: 压缩文件的路径。
    :param extract_to: 要解压到的目录。
    :returns: 解压结果，成功或失败。
    :raises: IOError 如果解压过程中发生IO错误。
    """
    try:
        # 确保目标目录存在
        if not os.path.exists(extract_to):
            os.makedirs(extract_to)

        # 打开压缩文件并解压
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        return True  # 解压成功
    except zipfile.BadZipFile:
        # 压缩文件损坏
        print(f"Error: The file {zip_path} is not a zip file or it is corrupt.")
        return False
    except FileNotFoundError:
        # 文件未找到
        print(f"Error: The file {zip_path} does not exist.")
        return False
    except Exception as e:
        # 其他错误
        print(f"An error occurred: {e}")
        return False

# 以下代码用于本地测试，实际部署时不需要
if __name__ == '__main__':
    # 测试解压文件
    test_zip_path = 'path_to_your_zip_file.zip'
    test_extract_to = 'path_to_extract_directory'
    result = unzip_file.delay(test_zip_path, test_extract_to)
    if result.get():
        print("Unzip successful.")
    else:
        print("Unzip failed.")