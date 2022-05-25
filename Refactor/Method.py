import requests
from Refactor_UserElement import *


class User(UserElement):
    def __init__(self):
        super().__init__()
        self.a = self.fetch_cookies()  # 获取cookies 顺序不可以调动
        self.b = self.fetch_csrf()  # 获取csrf 顺序不可以调动

    def get_requests(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 0:
                    return data
            else:
                self.logger.error("请求失败，状态码为：" + str(response.status_code))
        except Exception as e:
            self.logger.error(e)

    def post_requests(self, url, params):
        try:
            response = requests.post(url, headers=self.headers, data=params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                self.logger.error("请求失败，状态码为：" + str(response.status_code))
        except Exception as e:
            self.logger.error(e)

    def drop_coin(self, bvid, csrf):
        data_bv = {
            'bvid': bvid,
            'multiply': 1,
            'csrf': csrf
        }
        try:
            response = requests.post(self.url3, headers=self.headers, data=data_bv)
            if response.status_code == 200:
                data = response.json()
                self.logger.info(data)
            else:
                self.logger.error("请求失败，状态码为：" + str(response.status_code))
        except Exception as e:
            self.logger.error(e)

    def consult_dynamic(self, url):  # 获取个人动态，为投币任务做准备返回个人动态数据
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                dynamic = response.json()
                return dynamic
            else:
                self.logger.error("请求失败，状态码为：" + str(response.status_code))
        except Exception as e:
            self.logger.error(e)


