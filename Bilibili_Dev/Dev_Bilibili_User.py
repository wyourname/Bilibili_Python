"""
cron: 2 1 * * *
new Env("哔哩哔哩-【基础检查】")
"""

import json
import random
import time

from urllib3.exceptions import ConnectTimeoutError

from Dev_Bilibili_Config import Config
import requests


class Basic(Config):
    def __init__(self):
        super().__init__()
        self.cookies = self.fetch_cookies()
        self.csrfs = self.fetch_csrf(self.cookies)
        self.coin = self.fetch_drop_coin()

    def get_requests(self, url, proxy=None):
        try:
            time.sleep(1)
            self.headers['user-agent'] = random.choice(self.ua_list)
            with requests.session() as s:
                # 代理
                s.keep_alive = False
                s.adapters.DEFAULT_RETRIES = 2
                if proxy is None:
                    # proxies = {'http': f'http://{proxy}'}
                    r = s.get(url, headers=self.headers)
                else:
                    proxies = {'http': f'http://{proxy}'}
                    r = s.get(url, headers=self.headers, proxies=proxies)
                if r.status_code == 200:
                    data = json.loads(r.text)
                    return data
                else:
                    data_error = json.loads(r.text)
                    return data_error
        except Exception as e:
            self.logger.error('请求失败，错误信息：{}'.format(e))

    def post_requests(self, url, data, proxy=None):
        try:
            self.headers['method'] = 'POST'
            self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
            time.sleep(1)
            with requests.session() as s:
                s.keep_alive = False
                if proxy is None:
                    r = s.post(url, headers=self.headers, data=data)
                else:
                    proxies = {'http': f'http://{proxy}'}
                    r = s.post(url, headers=self.headers, data=data, proxies=proxies)
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

    def unfollow_author(self, csrf):
        data = {'fid': 289549318, 'act': 2, 're_src': 11, 'csrf': csrf}
        follow = self.post_requests(self.url1, data)
        if follow['code'] == 0:
            self.logger.info("取关作者成功")
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
                self.logger.info(
                    '当前硬币数：' + str(data['data']['money']) + "，下一等级升级天数约" + str(int(level_day)))
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
                self.unfollow_author(csrf)

    def check_proxy(self):
        proxys = self.fetch_proxy()
        if not proxys:
            self.logger.info("不使用代理")
        else:
            for i in proxys:
                if self.result_proxy(i):
                    self.logger.info(f"{i}该代理是ok的，保留下来")
                else:
                    # self.remove_proxy(i)  暂时不动这里
                    pass

    def result_proxy(self, ip):
        try:
            requests.adapters.DEFAULT_RETRIES = 3
            this_proxy = "http://" + ip
            res = requests.get(url="http://icanhazip.com/", timeout=8, proxies={"http": this_proxy})
            if res.status_code == 200:
                return True
        except Exception:
            self.logger.error(f"该项检测的代理{ip}无效，响应时间过长")
            return False

    def proxy_num(self):
        proxy_a = self.fetch_proxy()
        if proxy_a is not None:
            return proxy_a
        else:
            return None

    def user_info(self):
        self.logger.info("更新：将已关注我的取关硬币将够，加入代理感觉鸡肋")
        self.check_proxy()
        p_list = self.proxy_num()
        for i in range(len(self.cookies)):
            self.headers['Cookie'] = self.cookies[i]
            if not p_list:
                user = self.get_requests(self.url)
                self.cope_info(user)
                self.mao_san(self.csrfs[i])
            else:
                # p = random.choice(p_list)
                p = random.choice(p_list)
                user = self.get_requests(self.url, p)
                self.cope_info(user)
                self.mao_san(self.csrfs[i])


if __name__ == '__main__':
    cope = Basic()
    cope.user_info()
    # cope.check_proxy()
