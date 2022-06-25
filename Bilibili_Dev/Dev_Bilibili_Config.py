import json
import logging
import os


# 这里是把模块里面的一些变量提取出来，方便后面的使用
# 可以把这些变量提取出来，放到一个文件里面，这样就不会污染模块里面的变量
# 这里负责读取数据处理数据把数据包装传递到method里面
# sessdata  bili_jct  DedeUserID  DedeUserID_ckmd5  sid Build
#
#


class Config:
    def __init__(self):
        self.headers = {
            "authority": "api.bilibili.com",
            "method": "GET",
            "scheme": "https",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.6",
            "cookie": "",
            "dnt": "1",
            "origin": "https://www.bilibili.com",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Microsoft Edge";v="101"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47 ",
            "connection": "close"
        }

        self.url = "https://api.bilibili.com/x/web-interface/nav"
        self.url1 = "https://api.bilibili.com/x/relation/modify"
        self.url2 = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all"
        self.url3 = "https://api.bilibili.com/x/web-interface/coin/add"
        self.url4 = "https://api.bilibili.com/x/web-interface/share/add"
        self.url5 = "https://api.bilibili.com/x/web-interface/archive/related"
        self.url6 = "https://api.bilibili.com/x/click-interface/web/heartbeat"
        self.url7 = "https://api.live.bilibili.com/room/v1/Area/getList"
        self.url8 = "https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign"
        self.url9 = "https://api.bilibili.com/x/relation/tags"
        self.url10 = "https://api.bilibili.com/x/relation/tag"
        self.url_all = "https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web" \
                       "&parent_area_id=%s&area_id=%s&page=%s "
        self.url_check = "https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/Check?roomid=%s"
        self.url_tx = "https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/Join"
        self.url_relationship = "http://api.bilibili.com/x/relation/tags/moveUsers"
        self.url_group = "https://api.bilibili.com/x/relation/tags"
        self.create_url = "https://api.bilibili.com/x/relation/tag/create"
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger(__name__)

    def create_file(self):
        config = os.getcwd() + '/Bilibili_config.json'
        if os.path.exists(config):
            self.logger.info("----------配置文件已存在---------")
            return False
        else:
            with open('./Bilibili_config.json', 'w', encoding='utf-8') as f:
                json.dump({"Users": [{"Cookie": ""}], "Drop_coin": [{"coin": 1}], "max_page": 100, "max_thread": 7,
                           "black_list": [], "white_list": []}, f, ensure_ascii=False, indent=4)
                self.logger.info("请在文件中添加Cookie 如：")
                self.logger.info(
                    '{"Users": [{"Cookie": "这里是你的cookie"}], "Drop_coin": [{"coin": 1}], "max_page": 100, '
                    '"max_thread": 7}')
                return True

    def update_config(self):
        coin = {'coin': 1}
        with open("./Bilibili_config.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i in data['Drop_coin']:
                if i.keys() != coin.keys():
                    data['Drop_coin'].remove(i)
                    data['Drop_coin'].append(coin)
            if "black_list" in data:
                self.logger.info("黑名单文件已存在")
            else:
                self.logger.info("黑名单不存在，创建")
                data.update({"black_list": []})
            if "white_list" in data:
                self.logger.info("白名单文件已存在")
            else:
                self.logger.info("白名单不存在，创建")
                data.update({"white_list": []})
            if "Unfollows" in data:
                del data['Unfollows']
        with open("./Bilibili_config.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.logger.info("更新配置文件完成")

    def insert_data(self, num):
        for i in range(num - 1):
            with open("./Bilibili_config.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                data['Drop_coin'].append({'coin': 1})
            with open("./Bilibili_config.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        self.logger.info("更新ok")

    def fetch_cookies(self):
        cookies = []
        try:
            with open('./Bilibili_config.json', 'r', encoding='utf-8') as f:
                ck = json.load(f)
                for i in ck['Users']:
                    if i['Cookie'] != "":
                        cookies.append(i['Cookie'])
                    else:
                        self.logger.info("Cookie为空")
                return cookies
        except Exception as e:
            self.logger.error("请检查config文件路径是否存在或者文件是否正确，文件应该与当前文件在同一目录下:"+str(e))
            return None

    def fetch_csrf(self, cookies):
        element = []
        csrfs = []
        try:
            for i in cookies:
                str1 = i.split('; ')
                for j in str1:
                    str2 = j.split('=')
                    element.append(str2)
                csrf_dict = dict(element)
                csrfs.append(csrf_dict['bili_jct'])
                element.clear()
            return csrfs
        except Exception as e:
            self.logger.info("请检查你的cookie是否正确 " + str(e))
            return None

    def fetch_page(self):
        try:
            with open('./Bilibili_config.json', 'r', encoding='utf-8') as f:
                page = json.load(f)
                return page['max_page']
        except Exception as e:
            self.logger.info(e)
            return 0

    def fetch_thread(self):
        try:
            with open('./Bilibili_config.json', 'r', encoding='utf-8') as f:
                thread = json.load(f)
                return thread['max_thread']
        except Exception as e:
            self.logger.info(e)
            return 0

    def fetch_drop_coin(self):
        coin = []
        try:
            with open('./Bilibili_config.json', 'r', encoding='utf-8') as f:
                drop_coin = json.load(f)
                for i in drop_coin['Drop_coin']:
                    coin.append(i['coin'])
                return coin
        except Exception as e:
            self.logger.info(e)
            return 0

    def fetch_black_list(self):
        try:
            with open('./Bilibili_config.json', 'r', encoding='utf-8') as f:
                black_list = json.load(f)
                return black_list['black_list']
        except Exception as e:
            self.logger.info(e)
            return 0

    def fetch_white_list(self):
        try:
            with open('./Bilibili_config.json', 'r', encoding='utf-8') as f:
                white_list = json.load(f)
                return white_list['white_list']
        except Exception as e:
            self.logger.info(e)
            return 0

    def basic_info(self):
        self.logger.info("------》开始检查你的配置文件")
        self.logger.info('简化多用户步骤，只需要在config文件中添加--> ,{"Cookie": "这里是你的cookie"}  《再》运行一次本文件即可')
        self.logger.info("新增黑白名单功能，在black_list和white_list中添加用户ID即可")
        self.logger.info("黑名单是指你不想关注的用户，白名单是指你想保留关注的用户")
        # if self.create_file():
        #     self.logger.info("配置文件创建成功,请前往添加Cookie")
        # else:
        #     self.update_config()
        #     cookies = self.fetch_cookies()
        #     if len(cookies) > 0:
        #         self.logger.info("cookie检查成功")
        #         if len(self.fetch_cookies()) == len(self.fetch_csrf(cookies)) == len(self.fetch_drop_coin()):
        #             self.logger.info("配置文件正确")
        #         else:
        #             self.insert_data(len(self.fetch_cookies()))
        #     else:
        #         self.logger.info("cookie检查失败")


if __name__ == '__main__':
    a = Config()
    a.basic_info()
