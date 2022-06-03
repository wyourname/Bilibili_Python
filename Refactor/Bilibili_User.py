import json
import logging


# 这里是把模块里面的一些变量提取出来，方便后面的使用
# 可以把这些变量提取出来，放到一个文件里面，这样就不会污染模块里面的变量
# 这里负责读取数据处理数据把数据包装传递到method里面
# sessdata  bili_jct  DedeUserID  DedeUserID_ckmd5  sid Build
#
#


class UserElement:
    def __init__(self):
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
                          "Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47 ",
            "connection": "close"
        }

        self.url = "https://api.bilibili.com/x/web-interface/nav"
        self.url1 = "http://api.bilibili.com/x/relation/modify"
        self.url2 = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all"
        self.url3 = "http://api.bilibili.com/x/web-interface/coin/add"
        self.url4 = "http://api.bilibili.com/x/web-interface/share/add"
        self.url5 = "http://api.bilibili.com/x/web-interface/archive/related"
        self.url6 = "http://api.bilibili.com/x/click-interface/web/heartbeat"
        self.url7 = "http://api.live.bilibili.com/room/v1/Area/getList"
        self.url8 = "https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign"
        self.User_Cookie = []
        self.csrf = []
        self.sessdata = []
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger(__name__)

    def fetch_cookies(self):
        try:
            with open('Bilibili_config.json', 'r', encoding='utf-8') as f:
                ck = json.load(f)
                for i in range(len(ck['Users'])):
                    self.User_Cookie.append(ck['Users'][i]['Cookie'])
        except Exception as e:
            self.logger.info("请检查文件路径是否存在或者文件是否正确，文件应该与当前文件在同一目录下")
            self.logger.error(e)
        return self.User_Cookie

    def fetch_csrf(self):
        element = []
        try:
            for i in range(len(self.User_Cookie)):
                str1 = self.User_Cookie[i].split('; ')
                for j in range(len(str1)):
                    str2 = str1[j].split('=')
                    element.append(str2)
                csrf_dict = dict(element)
                self.csrf.append(csrf_dict['bili_jct'])
                self.sessdata.append(csrf_dict['SESSDATA'])
        except Exception as e:
            self.logger.info("请检查你的cookie是否正确 " + str(e))
        return self.csrf, self.sessdata
