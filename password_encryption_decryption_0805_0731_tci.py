# 代码生成时间: 2025-08-05 07:31:36
import os
from celery import Celery
from cryptography.fernet import Fernet

# 定义 Celery 应用
app = Celery('password_encryption_decryption', broker='pyamqp://guest@localhost//')

# 生成密钥并保存到文件
def generate_key():
    return Fernet.generate_key()

# 加载密钥
def load_key():
    key_path = 'secret.key'
    if os.path.exists(key_path):
        with open(key_path, 'rb') as key_file:
            return key_file.read()
    else:
        return generate_key()

# 保存密钥到文件
def save_key(key):
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)

# 加密密码
@app.task
def encrypt_password(password):
    """
    加密密码
    :param password: 待加密的密码
    :return: 加密后的密码
    """
    try:
        key = load_key()
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(password.encode())
        return encrypted_password.decode()
    except Exception as e:
        raise Exception(f'Failed to encrypt password: {str(e)}')

# 解密密码
@app.task
def decrypt_password(encrypted_password):
    """
    解密密码
    :param encrypted_password: 待解密的密码
    :return: 解密后的密码
    """
    try:
        key = load_key()
        fernet = Fernet(key)
        decrypted_password = fernet.decrypt(encrypted_password.encode())
        return decrypted_password.decode()
    except Exception as e:
        raise Exception(f'Failed to decrypt password: {str(e)}')

if __name__ == '__main__':
    # 生成密钥并保存
    key = generate_key()
    save_key(key)
    print(f'Key generated and saved: {key}')
    
    # 示例：加密和解密密码
    password = 'mysecretpassword'
    encrypted = encrypt_password.delay(password)
    decrypted = decrypt_password.delay(encrypted.get())
    print(f'Encrypted password: {encrypted.get()}')
    print(f'Decrypted password: {decrypted.get()}')
