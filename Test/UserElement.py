import json
import logging
import time

import requests


class UserElement:
    def __init__(self):
        self.User_Cookie = []
        self.headers = {
            "authority": "api.bilibili.com",
            "method": "GET",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.6",
            "cookie": "",
            "dnt": "1",
            "origin": "https://www.bilibili.com",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Microsoft Edge";v="101"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47 "

        }
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger(__name__)

    # 此处是读取cookie的函数并把cookie赋值给self.Cookie
    def fetch_cookie(self):
        with open('./config.json', 'r', encoding='utf-8') as f:
            ck = json.load(f)
            for i in range(len(ck['Users'])):
                self.User_Cookie.append(ck['Users'][i]['Cookie'])
        return self.User_Cookie

    # 此处是请求用户信息的函数
    def Get_UserInfo(self):
        url1 = "https://api.bilibili.com/x/web-interface/nav"
        for i in range(len(self.User_Cookie)):
            self.headers['cookie'] = self.User_Cookie[i]
            # print(self.headers['cookie'])
            response = requests.get(url1, headers=self.headers)
            print(response.text)
            time.sleep(3)


if __name__ == '__main__':
    a = UserElement()
    a.fetch_cookie()
    # print(a.cookie_index)
    a.Get_UserInfo()
    # print(a.headers)
