# 代码生成时间: 2025-08-29 16:39:22
import requests
from celery import Celery
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 配置Celery
app = Celery('web_scraper', broker='amqp://guest@localhost//')
app.conf.update(
    result_backend='rpc://',
)

# 网页内容抓取函数
@app.task
def scrape_web_content(url):
    """
    抓取网页内容的任务函数。
    :param url: 需要抓取的网页URL。
    :return: 网页内容或错误信息。
    """
    try:
        # 发送HTTP请求获取网页内容
        response = requests.get(url)
        response.raise_for_status()  # 检查HTTP响应状态

        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取网页标题
        title = soup.title.string if soup.title else 'No title found'

        # 提取网页链接
        links = [urljoin(url, a.get('href')) for a in soup.find_all('a', href=True)]

        # 返回网页标题和链接列表
        return {'title': title, 'links': links}

    except requests.exceptions.HTTPError as http_err:
        # 处理HTTP错误
        return f'HTTP error occurred: {http_err}'
    except requests.exceptions.RequestException as err:
        # 处理请求错误
        return f'Error occurred: {err}'
    except Exception as err:
        # 处理其他错误
        return f'An unexpected error occurred: {err}'

if __name__ == '__main__':
    # 测试网页内容抓取工具
    url_to_scrape = 'https://example.com'
    result = scrape_web_content.delay(url_to_scrape)
    print(result.get())  # 打印抓取结果