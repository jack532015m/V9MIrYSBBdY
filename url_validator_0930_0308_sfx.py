# 代码生成时间: 2025-09-30 03:08:19
import requests
from celery import Celery
from urllib.parse import urlparse
from celery.utils.log import get_task_logger

# Configure Celery
app = Celery('url_validator', broker='pyamqp://guest@localhost//')
logger = get_task_logger(__name__)

@app.task
def validate_url(url):
    '''
    Validate the given URL by checking its status code.
    If the URL is valid, return True; otherwise, return False.
    
    :param url: The URL to be validated.
    :return: A boolean indicating the validity of the URL.
    '''
    try:
        # Use urlparse to validate the URL structure
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            logger.error('Invalid URL structure: %s', url)
            return False
        
        # Send a HEAD request to check the URL without downloading the content
        response = requests.head(url, allow_redirects=True)
        
        # Check if the response status code is 200-299 (HTTP OK)
        if 200 <= response.status_code < 300:
            logger.info('URL is valid: %s', url)
            return True
        else:
            logger.error('URL is invalid or unreachable: %s, status code: %d', url, response.status_code)
            return False
    except requests.RequestException as e:
        logger.error('Request error: %s', e)
        return False
    except Exception as e:
        logger.error('Unexpected error: %s', e)
        return False

# Example usage
# if __name__ == '__main__':
#     validate_url.delay('http://example.com')