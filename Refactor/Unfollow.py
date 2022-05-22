import time
import requests

from Refactor_UserElement import *


class Follow(UserElement):
    def __init__(self):
        super().__init__()
        self.a = self.fetch_cookies()  # 获取cookies 顺序不可以调动
        self.b = self.fetch_csrf()  # 获取csrf 顺序不可以调动

    def user_info(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                self.logger.info('登录成功')
                self.logger.info(data['data']['uname']+" 当前等级为："+str(data['data']['level_info']['current_level']))
            else:
                self.logger.error("请求失败，状态码为："+str(response.status_code))
        except Exception as e:
            self.logger.error(e)

    def follow_user(self):
        for i in range(len(self.a)):
            self.headers['Cookie'] = self.a[i]
            self.user_info()
            time.sleep(5)


if __name__ == '__main__':
    follow = Follow()
    follow.follow_user()
