# 代码生成时间: 2025-09-11 11:31:45
import os
from celery import Celery

# 配置Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
app = Celery('user_permission_management')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model

# User model
UserModel = get_user_model()


# Define tasks
@app.task
def add_user(username, email, password):
    """Add a new user to the system.
    
    Parameters:
    username (str): The username of the user.
    email (str): The email address of the user.
    password (str): The password of the user.
    """
    try:
        user = UserModel.objects.create_user(username=username, email=email, password=password)
        return {'status': 'success', 'message': 'User created successfully.', 'data': {'username': user.username}}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@app.task
def assign_user_to_group(user_id, group_name):
    """Assign a user to a group.
    
    Parameters:
    user_id (int): The id of the user.
    group_name (str): The name of the group.
    """
    try:
        user = UserModel.objects.get(pk=user_id)
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        return {'status': 'success', 'message': 'User assigned to group successfully.', 'data': {'user_id': user_id, 'group_name': group_name}}
    except ObjectDoesNotExist as e:
        return {'status': 'error', 'message': str(e)}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@app.task
def remove_user_from_group(user_id, group_name):
    """Remove a user from a group.
    
    Parameters:
    user_id (int): The id of the user.
    group_name (str): The name of the group.
    """
    try:
        user = UserModel.objects.get(pk=user_id)
        group = Group.objects.get(name=group_name)
        user.groups.remove(group)
        return {'status': 'success', 'message': 'User removed from group successfully.', 'data': {'user_id': user_id, 'group_name': group_name}}
    except ObjectDoesNotExist as e:
        return {'status': 'error', 'message': str(e)}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@app.task
def get_user_groups(user_id):
    """Get all groups a user belongs to.
    
    Parameters:
    user_id (int): The id of the user.
    """
    try:
        user = UserModel.objects.get(pk=user_id)
        groups = [group.name for group in user.groups.all()]
        return {'status': 'success', 'message': 'Groups retrieved successfully.', 'data': {'user_id': user_id, 'groups': groups}}
    except ObjectDoesNotExist as e:
        return {'status': 'error', 'message': str(e)}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


if __name__ == '__main__':
    # Start the Celery worker
    app.start()
