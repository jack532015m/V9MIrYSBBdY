# 代码生成时间: 2025-10-06 03:21:22
import os
import base64
from cryptography.fernet import Fernet
from celery import Celery

# 定义一个 Celery 应用
app = Celery('file_encryption_utility', broker='pyamqp://guest@localhost//')

# 生成密钥，保存到环境变量中，或者直接在这里指定
fernet_key = os.environ.get('FERNET_KEY')
if not fernet_key:
    fernet_key = Fernet.generate_key()
    os.environ['FERNET_KEY'] = fernet_key

# 初始化 Fernet 对象
cipher_suite = Fernet(fernet_key)

# Celery 任务：加密文件
@app.task
def encrypt_file(file_path):
    """加密给定的文件。"""
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
            encrypted_data = cipher_suite.encrypt(file_data)
            with open(file_path + 'encrypted', 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)
            return {'status': 'success', 'message': 'File encrypted successfully'}
    except FileNotFoundError:
        return {'status': 'error', 'message': 'File not found'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# Celery 任务：解密文件
@app.task
def decrypt_file(file_path):
    """解密给定的文件。"""
    try:
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            with open(file_path.replace('encrypted', 'decrypted'), 'wb') as decrypted_file:
                decrypted_file.write(decrypted_data)
            return {'status': 'success', 'message': 'File decrypted successfully'}
    except FileNotFoundError:
        return {'status': 'error', 'message': 'File not found'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# 启动 Celery worker
if __name__ == '__main__':
    app.start()
