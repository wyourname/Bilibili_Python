from Bilibili_User import UserElement
import requests
import random


class DailyMethod(UserElement):
    def __init__(self):
        super().__init__()
        self.cookie = self.fetch_cookies()
        self.csrf = self.fetch_csrf()

    def get_requests(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            if response.status_code == 200:
                get_data = response.json()
                return get_data
            else:
                self.logger.error('请求失败，状态码：{}'.format(response.status_code))
                return None
        except Exception as e:
            self.logger.error('请求失败，错误信息：{}'.format(e))

    def post_requests(self, url, **kwargs):
        try:
            response = requests.post(url, headers=self.headers, data=kwargs, timeout=5)
            if response.status_code == 200:
                post_data = response.json()
                return post_data
            else:
                self.logger.error('请求失败，状态码：{}'.format(response.status_code))
                return None
        except Exception as e:
            self.logger.error('请求失败，错误信息：{}'.format(e))
