# 代码生成时间: 2025-08-18 16:58:13
# -*- coding: utf-8 -*-

"""
密码加密解密工具

本模块使用CELERY框架来实现密码的加密和解密功能。
"""

import os
from celery import Celery
from cryptography.fernet import Fernet

# 配置CELERY
celery_app = Celery('password_encryption_utility', broker=os.environ.get('CELERY_BROKER_URL'))

# 定义密码加密解密函数
class PasswordUtility:
    """密码加密解密工具类"""
    def __init__(self):
        # 生成密钥并保存
        self.key = Fernet.generate_key()

    def encrypt_password(self, password):
        """
        加密密码

        参数:
        password (str): 待加密的密码

        返回:
        str: 加密后的密码
        """
        try:
            fernet = Fernet(self.key)
            encrypted_password = fernet.encrypt(password.encode())
            return encrypted_password.decode()
        except Exception as e:
            # 错误处理
            print(f"加密密码时发生错误: {e}")
            return None

    def decrypt_password(self, encrypted_password):
        """
        解密密码

        参数:
        encrypted_password (str): 待解密的加密密码

        返回:
        str: 解密后的密码
        """
        try:
            fernet = Fernet(self.key)
            decrypted_password = fernet.decrypt(encrypted_password.encode())
            return decrypted_password.decode()
        except Exception as e:
            # 错误处理
            print(f"解密密码时发生错误: {e}")
            return None

# CELERY任务
@celery_app.task
def encrypt_task(password):
    """
    CELERY任务：加密密码

    参数:
    password (str): 待加密的密码

    返回:
    str: 加密后的密码
    """
    password_utility = PasswordUtility()
    return password_utility.encrypt_password(password)

@celery_app.task
def decrypt_task(encrypted_password):
    """
    CELERY任务：解密密码

    参数:
    encrypted_password (str): 待解密的加密密码

    返回:
    str: 解密后的密码
    """
    password_utility = PasswordUtility()
    return password_utility.decrypt_password(encrypted_password)