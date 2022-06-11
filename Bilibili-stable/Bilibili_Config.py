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
        self.url_group = "http://api.bilibili.com/x/relation/tags"
        self.create_url = "http://api.bilibili.com/x/relation/tag/create"
        self.cookies = []
        self.csrfs = []
        self.Num = []
        self.coin = []
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger(__name__)

    def create_file(self):
        config = os.getcwd() + '/Bilibili_config.json'
        if os.path.exists(config):
            self.logger.info("----------文件已存在---------")
            return True
        else:
            with open('./Bilibili_config.json', 'w', encoding='utf-8') as f:
                json.dump({"Users": [{"Cookie": ""}], "Unfollows": [{"number": 50}], "Drop_coin": [{"User": 1}],
                           "max_page": 100, "max_thread": 7}, f, ensure_ascii=False)
                self.logger.info("文件创建格式生成success,请前往我的仓库添加cookie")
                self.logger.info("请在文件中添加Cookie 如：")
                self.logger.info('{"Users": [{"Cookie": "这里是你的cookie"}], "Unfollows": [{"number": 50}], "Drop_coin": '
                                 '[{"User": 1}], "max_page": 100, "max_thread": 7}')
                return True

    def fetch_cookies(self):
        try:
            with open('./Bilibili_config.json', 'r', encoding='utf-8') as f:
                ck = json.load(f)
                for i in range(len(ck['Users'])):
                    self.cookies.append(ck['Users'][i]['Cookie'])
        except Exception as e:
            self.logger.info("请检查config文件路径是否存在或者文件是否正确，文件应该与当前文件在同一目录下")
            self.logger.error(e)
        return self.cookies

    def fetch_csrf(self):
        element = []
        try:
            for i in range(len(self.cookies)):
                str1 = self.cookies[i].split('; ')
                for j in range(len(str1)):
                    str2 = str1[j].split('=')
                    element.append(str2)
                csrf_dict = dict(element)
                self.csrfs.append(csrf_dict['bili_jct'])
        except Exception as e:
            self.logger.info("请检查你的cookie是否正确 " + str(e))
        return self.csrfs

    def fetch_num(self):
        try:
            with open('Bilibili_config.json', 'r', encoding='utf-8') as f:
                Num = json.load(f)
                for i in range(len(Num['Unfollows'])):
                    self.Num.append(Num['Unfollows'][i]['number'])
        except Exception as e:
            self.logger.info("请检查文件路径是否存在或者文件是否正确，文件应该与当前文件在同一目录下")
            self.logger.error(e)
        return self.Num

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
        try:
            with open('./Bilibili_config.json', 'r', encoding='utf-8') as f:
                drop_coin = json.load(f)
                for i in range(len(drop_coin['Drop_coin'])):
                    self.coin.append(drop_coin['Drop_coin'][i]['User'])
                return self.coin
        except Exception as e:
            self.logger.info(e)
            return 0

    def basic_info(self):
        if self.create_file():
            self.logger.info("-----------------该脚本为生成Bilibili_config.json-----------------")
            self.logger.info("正确的cookie格式如下，顺序可变动：")
            self.logger.info("buvid3=xxxx; sid=xxxx; buvid_fp_plain=xxxxxx; rpdid=xxxx; blackside_state=0; "
                             "buvid_fp=xxxxxx; _uuid=xxxxx; buvid4=xxxxx; i-wanna-go-back=-1; LIVE_BUVID=xxx; "
                             "CURRENT_BLACKGAP=x; nostalgia_conf=-1; hit-dyn-v2=1; DedeUserID=xxxxx; "
                             "DedeUserID__ckMd5=xxxxxx; SESSDATA=xxxxx; bili_jct=xxxx; b_ut=xx; CURRENT_QUALITY=xx; "
                             "fingerprint3=xxx; fingerprint=xxx; CURRENT_FNVAL=80; bp_video_offset_289549318=xxxxx; "
                             "innersign=0; b_lsid=xxxx; b_timer=xxxx; PVID=xxx")
            self.logger.info("********************************************************")
            self.cookies = self.fetch_cookies()
            self.csrfs = self.fetch_csrf()
            self.coin = self.fetch_drop_coin()
            self.Num = self.fetch_num()
            for i in range(len(self.cookies)):
                self.logger.info("你的第" + str(i + 1) + "个cookie的值为：" + self.cookies[i])
                self.logger.info("你第" + str(i + 1) + "个csrf的值为：" + self.csrfs[i])
                self.logger.info("第%s个帐号每个视频投币数为：%s,投币数应为1-2个合理" % (i + 1, self.coin[i]))
                self.logger.info("第%s个帐号最大取关数为：%s,数应为50个合理" % (i + 1, self.Num[i]))
            self.logger.info("你的最大爬取页数为：%s,爬取最大页数50左右为宜你也可以选择1000" % self.fetch_page())
            self.logger.info("你的最大爬取线程数为：%s,爬取最大线程数为2-3左右为宜你也可以选择10" % self.fetch_thread())
        else:
            self.logger.info("未知错误")


if __name__ == '__main__':
    a = Config()
    a.basic_info()
