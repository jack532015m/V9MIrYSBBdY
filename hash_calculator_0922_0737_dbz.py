# 代码生成时间: 2025-09-22 07:37:08
import hashlib
from celery import Celery

# 配置Celery
app = Celery('hash_calculator', broker='pyamqp://guest@localhost//')


@app.task
def calculate_hash(data, algorithm='sha256'):
    """
    计算给定数据的哈希值
    :param data: 待计算的数据
    :param algorithm: 哈希算法（默认为sha256）
    :return: 哈希值的十六进制字符串
    """
    try:
        hash_func = getattr(hashlib, algorithm)()
        hash_func.update(data.encode('utf-8'))
        return hash_func.hexdigest()
    except AttributeError as e:
        # 如果指定的算法不存在，则抛出异常
        raise ValueError(f"Unsupported algorithm: {algorithm}") from e
    except Exception as e:
        # 其他异常
        raise RuntimeError(f"Failed to calculate hash: {str(e)}") from e


if __name__ == '__main__':
    # 测试代码
    try:
        data = 'Hello, World!'
        algorithm = 'sha256'
        result = calculate_hash.delay(data, algorithm)
        result.get()  # 异步等待结果
        print(f"Hash ({algorithm}): {result.get()}")
    except Exception as e:
        print(f"Error: {str(e)}")