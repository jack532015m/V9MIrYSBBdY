# 代码生成时间: 2025-07-31 19:54:10
# user_login_validation.py

"""
User Login Validation System using Python and Celery framework.
This script handles the user login process and verifies credentials.
"""

import logging
from celery import Celery
from celery.utils.log import get_task_logger

# Set up Celery
app = Celery('user_login_validation', broker='pyamqp://guest@localhost//')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = get_task_logger(__name__)


@app.task
def validate_user_credentials(username, password):
    """
    Validates user credentials against a predefined set of valid users.
    Args:
        username (str): The username of the user attempting to log in.
        password (str): The password of the user attempting to log in.
    Returns:
        dict: A dictionary containing the result of the login attempt.
        The dictionary will have keys 'success', 'message', and 'user_data'.
    """
    # Predefined valid users for demonstration purposes
    valid_users = {
        'admin': 'password123',
        'user1': 'user123',
    }

    # Check if the username exists in the valid users
    if username in valid_users:
        # Check if the password is correct
        if valid_users[username] == password:
            return {
                'success': True,
                'message': 'Login successful.',
                'user_data': {'username': username},
            }
        else:
            logger.error(f"Invalid password for user {username}")
            return {
                'success': False,
                'message': 'Invalid password.',
            }
    else:
        logger.error(f"User {username} does not exist")
        return {
            'success': False,
            'message': 'User does not exist.',
        }


if __name__ == '__main__':
    # This is just for demonstration purposes to run the task directly.
    # In a real-world scenario, this task would be triggered by a web request.
    result = validate_user_credentials('admin', 'password123')
    print(result.get())
