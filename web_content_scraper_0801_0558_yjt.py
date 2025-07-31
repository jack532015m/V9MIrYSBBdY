# 代码生成时间: 2025-08-01 05:58:07
import requests
from bs4 import BeautifulSoup
from celery import Celery
import os

# Celery configuration
os.environ.setdefault('CELERY_BROKER_URL', 'amqp://guest:guest@localhost//')
app = Celery('web_content_scraper', broker=os.environ['CELERY_BROKER_URL'])


@app.task(
    name='web_content_scraper.grab_content',
    autoretry_for=(requests.exceptions.RequestException,),
    retry_kwargs={'max_retries': 5},
    time_limit=60
)
def grab_content(url):
    """
    This function grabs the content of a webpage.
    It uses the requests library to fetch the webpage and BeautifulSoup to parse the HTML content.

    :param url: The URL of the webpage to scrape.
    :return: The text content of the webpage.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code.
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text content from the webpage
        content = soup.get_text()
        return content
    except requests.exceptions.RequestException as e:
        # Log the error and return a message indicating the failure
        app.send_task('web_content_scraper.log_error', args=[str(e)])
        return 'Failed to fetch content'
    except Exception as e:
        # Log any other exceptions and return a message indicating the failure
        app.send_task('web_content_scraper.log_error', args=[str(e)])
        return 'An error occurred while fetching content'


def log_error(error_message):
    """
    Logs an error message to the console or a file.
    This function can be enhanced to log errors to a more robust logging system.

    :param error_message: The error message to be logged.
    """
    print(f'Error: {error_message}')


# Example usage:
# result = grab_content.delay('https://www.example.com')
# print(result.get(timeout=60))
