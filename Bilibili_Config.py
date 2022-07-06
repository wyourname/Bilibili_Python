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
            "Connection": "close"
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
        self.url11 = "https://api.bilibili.com/x/space/arc/search?mid=%s"
        self.url_all = "https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web" \
                       "&parent_area_id=%s&area_id=%s&page=%s "
        self.url_check = "https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/Check?roomid=%s"
        self.url_tx = "https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/Join"
        self.url_relationship = "https://api.bilibili.com/x/relation/tags/moveUsers"
        self.url_group = "https://api.bilibili.com/x/relation/tags"
        self.create_url = "https://api.bilibili.com/x/relation/tag/create"
        self.prize = "https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/AwardRecord"
        self.ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47 ",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 "
            "Safari/537.36 Edg/103.0.1264.37",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 "
            "Safari/537.36 "
        ]
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger(__name__)

    def check_json(self):
        config = os.getcwd() + '/Bilibili_config.json'
        if os.path.exists(config):
            self.logger.info("配置文件存在")
            return True
        else:
            self.logger.info("配置文件不存在")
            return False

    def create_file(self):
        with open('./Bilibili_config.json', 'w', encoding='utf-8') as f:
            json.dump({"Users": [{"Cookie": ""}], "Drop_coin": [{"coin": 1}], "max_page": 50, "max_thread": 7,
                       "black_list": [], "white_list": [], "favorite": []}, f, ensure_ascii=False, indent=4)
        self.logger.info("Bilibili_config.json文件已经生成，请在文件中添加Cookie 如：")
        self.logger.info('"Users": [{"Cookie": "这里是你的cookie"}]')
        self.logger.info('默认生成单帐号，投币数量为1，天选页数为50，投币线程数为7，黑名单为空，白名单为空，指定的投币up主为空')
        self.logger.info('如需多账号，则如 "Users": [{"Cookie": "这里是你的cookie"}, {"Cookie": "这里是你的cookie"},{}...]')

    def update_config(self):
        coin = {'coin': 1}
        with open("./Bilibili_config.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i in data['Drop_coin']:
                if i.keys() != coin.keys():
                    self.logger.info("检查到你的投币配置有误，自动为你更新")
                    data['Drop_coin'].remove(i)
                    data['Drop_coin'].append(coin)
                    self.update_json(data)
            if "black_list" in data:
                self.logger.info("黑名单文件已存在")
            else:
                self.logger.info("黑名单不存在，创建")
                data.update({"black_list": []})
                self.update_json(data)
            if "white_list" in data:
                self.logger.info("白名单文件已存在")
            else:
                self.logger.info("白名单不存在，创建")
                data.update({"white_list": []})
                self.update_json(data)
            if "Unfollows" in data:
                del data['Unfollows']
                self.update_json(data)
            if "favorite" in data:
                self.logger.info("给指定up主名单配置存在")
            else:
                self.logger.info("给指定up主名单配置不存在，创建")
                data.update({"favorite": []})
                self.update_json(data)

    def insert_data(self, num):
        for i in range(num - 1):
            with open("./Bilibili_config.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                data['Drop_coin'].append({'coin': 1})
            self.update_json(data)

    def update_json(self, data):
        with open("./Bilibili_config.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.logger.info("更新配置文件完成")

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
            self.logger.error("请检查config文件路径是否存在或者文件是否正确，文件应该与当前文件在同一目录下:" + str(e))
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

    def fetch_favorite(self):
        try:
            with open('./Bilibili_config.json', 'r', encoding='utf-8') as f:
                white_list = json.load(f)
                return white_list['favorite']
        except Exception as e:
            self.logger.info(e)
            return None

    def check_config(self):
        cookies = self.fetch_cookies()
        csrfs = self.fetch_csrf(cookies)
        coins = self.fetch_drop_coin()
        if cookies:
            if len(cookies) == len(coins) == len(csrfs):
                self.logger.info("配置文件正确")
                self.update_config()
            else:
                self.logger.info("配置文件有误,尝试修正")
                self.insert_data(len(cookies))
                self.update_config()
        else:
            self.logger.info("检查一下cookie吧")

    def basic_info(self):
        self.logger.info("脚本作者：github@wangquanfugui233")
        self.logger.info("Bilibili_config.json文件路径为：" + str(os.getcwd()) + "/Bilibili_config.json")
        self.logger.info("cookie不能有大括号！！！！！！")
        if self.check_json():
            self.logger.info("开始检查配置文件")
            self.check_config()
        else:
            self.logger.info("开始创建配置文件")
            self.create_file()
        self.logger.info("每次填完配置文件后，请跑一次本脚本检查是否正确")


if __name__ == '__main__':
    a = Config()
    a.basic_info()
