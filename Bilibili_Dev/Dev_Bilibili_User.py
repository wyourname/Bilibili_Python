import json
import time
import urllib3
from Dev_Bilibili_Config import Config
import requests
import random


class Basic(Config):
    def __init__(self):
        super().__init__()
        self.cookies = self.fetch_cookies()
        self.csrfs = self.fetch_csrf(self.cookies)
        self.coin = self.fetch_drop_coin()

    def get_requests(self, url):
        try:
            urllib3.disable_warnings()
            response = requests.get(url, headers=self.headers, verify=False)
            if response.status_code == 200:
                response.close()
                get_data = json.loads(response.text)
                return get_data
            else:
                self.logger.error('请求失败：{}'.format(response.content))
                return None
        except Exception as e:
            self.logger.error('请求失败，错误信息：{}'.format(e))

    def post_requests(self, url, data):
        try:
            self.headers['method'] = 'POST'
            self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
            urllib3.disable_warnings()
            response = requests.post(url, headers=self.headers, data=data, verify=False)
            if response.status_code == 200:
                response.close()
                post_data = json.loads(response.text)
                return post_data
            else:
                self.logger.error('请求失败：{}'.format(response.content))
                return None
        except Exception as e:
            self.logger.error('请求失败，错误信息：{}'.format(e))

    def cope_info(self, data):
        if data['code'] == 0:
            self.logger.info("**********" + data['data']['uname'] + "**********")
            self.logger.info("当前经验值：" + str(data['data']['level_info']['current_exp']))
            if data['data']['level_info']['current_level'] == 6:
                self.logger.info("你已经是lv6的大佬了")
            else:
                level_day = (data['data']['level_info']['next_exp'] - data['data']['level_info']['current_exp']) / 65
                self.logger.info('当前硬币数：' + str(data['data']['money']) + "，下一等级升级天数约" + str(int(level_day)))
        elif data['code'] == -101:
            self.logger.info(data['message'] + "请检查cookie")
        elif data['code'] == -111:
            self.logger.info(data['message'] + "请检查csrf")
        else:
            self.logger.info(data['message'])

    def user_info(self):
        self.logger.info("**********用户信息**********")
        self.logger.info("该脚本为验证你的cookie是否有效，如果cookie无效，请检查cookie是否过期")
        self.logger.info("脚本包含了日常任务函数，如果你不需要日常任务，请删除该脚本和Bilibili_Daily.py文件")
        for i in range(len(self.cookies)):
            self.headers['Cookie'] = self.cookies[i]
            user = self.get_requests(self.url)
            self.cope_info(user)


if __name__ == '__main__':
    cope = Basic()
    cope.user_info()
