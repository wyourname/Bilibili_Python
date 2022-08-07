"""
cron : 2 1 * * *
new Env("哔哩哔哩-【basic】")
"""

import json
import random
import time
from Bilibili_Config import Config
import requests


class Basic(Config):
    def __init__(self):
        super().__init__()
        self.cookies = self.fetch_cookies()
        self.csrfs = self.fetch_csrf(self.cookies)
        self.coin = self.fetch_drop_coin()

    def get_requests(self, url):
        try:
            time.sleep(1)
            self.headers['user-agent'] = random.choice(self.ua_list)
            with requests.session() as s:
                # 代理
                proxies = {'http': 'http://202.55.5.209:8090'}
                s.keep_alive = False
                s.adapters.DEFAULT_RETRIES = 2
                r = s.get(url, headers=self.headers, proxies=proxies)
                if r.status_code == 200:
                    data = json.loads(r.text)
                    return data
                else:
                    data_error = json.loads(r.text)
                    return data_error
        except Exception as e:
            self.logger.error('请求失败，错误信息：{}'.format(e))

    def post_requests(self, url, data):
        try:
            self.headers['method'] = 'POST'
            self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
            time.sleep(1)
            with requests.session() as s:
                s.keep_alive = False
                r = s.post(url, headers=self.headers, data=data)
                if r.status_code == 200:
                    post_data = json.loads(r.text)
                    return post_data
                else:
                    data_error = json.loads(r.text)
                    return data_error
        except Exception as e:
            self.logger.error('请求失败，错误信息：{}'.format(e))

    def check_author(self):
        url = self.url_re % 289549318
        author = self.get_requests(url)
        if author['code'] == 0:
            if author['data']['attribute'] != 0:
                return True
            else:
                return False
        else:
            return False

    def follow_author(self, csrf):
        data = {'fid': 289549318, 'act': 1, 're_src': 11, 'csrf': csrf}
        follow = self.post_requests(self.url1, data)
        if follow['code'] == 0:
            self.logger.info("关注作者成功")
        else:
            self.logger.info(follow['message'])

    def cope_info(self, data):
        if data['code'] == 0:
            self.logger.info("**********" + data['data']['uname'] + "**********")
            self.logger.info("当前经验值：" + str(data['data']['level_info']['current_exp']))
            if data['data']['level_info']['current_level'] == 6:
                self.logger.info("你已经是lv6的大佬了")
            else:
                level_day = (data['data']['level_info']['next_exp'] - data['data']['level_info']['current_exp']) / 65
                self.logger.info('当前硬币数：' + str(data['data']['money']) + "，下一等级升级天数约" + str(int(level_day)))
            return True
        elif data['code'] == -101:
            self.logger.info(data['message'] + "请检查cookie")
            return False
        elif data['code'] == -111:
            self.logger.info(data['message'] + "请检查csrf")
        else:
            self.logger.info(data['message'])

    def mao_san(self, csrf):
        if self.fetch_follow():
            if self.check_author():
                pass
            else:
                self.follow_author(csrf)
        else:
            pass

    def manual(self):
        self.logger.info("author: github@wangquanfugui233")
        self.logger.info("本次更新加入关注作者B站号，将随机为作者提供0.1个硬币")
        self.logger.info("这让你感到不适，请删除脚本或者配置文件将follow_author设置为小写false")

    def user_info(self):
        self.manual()
        for i in range(len(self.cookies)):
            self.headers['Cookie'] = self.cookies[i]
            user = self.get_requests(self.url)
            self.cope_info(user)


if __name__ == '__main__':
    cope = Basic()
    cope.user_info()
