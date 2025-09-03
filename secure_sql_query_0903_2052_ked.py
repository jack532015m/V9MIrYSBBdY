# 代码生成时间: 2025-09-03 20:52:32
import mysql.connector
from celery import Celery
from celery.utils.log import get_task_logger

# 初始化Celery任务
app = Celery('secure_sql_query', broker='pyamqp://guest@localhost//')
logger = get_task_logger(__name__)


# 数据库配置信息
DB_CONFIG = {
    "host": "localhost",
    "database": "mydatabase",
    "user": "myuser",
    "password": "mypassword"
}


@app.task
def execute_secure_query(query_template, params):
    """
    Executes an SQL query in a secure manner to prevent SQL injection.
    
    :param query_template: A string template with placeholders for parameters.
    :param params: A tuple or list of parameters to safely substitute into the query.
    :return: The result of the query execution.
    """
    try:
        # Establish a connection to the database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Prepare the query with parameters to prevent SQL injection
        query = query_template.format(*params)

        # Execute the query
        cursor.execute(query)

        # Fetch and return the results
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    except Exception as e:
        logger.error(f'Error executing query: {e}')
        raise


# Example usage of the secure SQL query function
if __name__ == '__main__':
    query_template = "SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    params = ("example_user", "example_pass")
    try:
        result = execute_secure_query(query_template, params)
        print(result)
    except Exception as e:
        print(f'An error occurred: {e}')