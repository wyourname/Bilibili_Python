import logging
import asyncio
import os
import sys

import aiofiles
import yaml


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
        self.url_re = "https://api.bilibili.com/x/relation?fid=%s"
        self.url9 = "https://api.bilibili.com/x/relation/tags"
        self.url10 = "https://api.bilibili.com/x/relation/tag"
        self.url11 = "https://api.bilibili.com/x/space/arc/search?mid="
        self.url_all = "https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web" \
                       "&parent_area_id=%s&area_id=%s&page=%s "
        self.url_check = "https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/Check?roomid=%s"
        self.url_tx = "https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/Join"
        self.url_relationship = "https://api.bilibili.com/x/relation/tags/moveUsers"
        self.url_group = "https://api.bilibili.com/x/relation/tags"
        self.create_url = "https://api.bilibili.com/x/relation/tag/create"
        self.prize = "https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/AwardRecord"
        self.send = "https://api.live.bilibili.com/msg/send"
        self.clockin_url = "https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn"
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

    async def create_config(self):
        data = {
            'user1': {
                'cookie': 'xxxx',
                'coin': 0,
                'spider_page': 50,
                'spider_thread': 7,  # 线程数不可超出7
                'blacklist': [],  # 此处填写uid,格式为uid1,uid2,uid3,uid4,uid5,uid6,uid
                'whitelist': [],  # 白名单处填写uid,格式为uid1,uid2,uid，中奖天选后防止取关会自动添加上
                'DesignateUp': [],  # 设定要投币的uid,格式为uid1,uid2,
                'proxylist': []  # 代理列表格式字符串，格式为"ip:port" 不写就默认不代理
            }
        }

        comments = {
            'user1': {
                'cookie': '用户登录B站时使用的cookie',
                'coin': '是否开启B站自动投币功能，0表示关闭，1表示开启，如果你要投币两个我还没适配哦',
                'spider_page': 'B站天选时爬取的页数',
                'spider_thread': '线程数不可超出7',
                'blacklist': '此处填写uid,格式为uid1,uid2,uid3,uid4,uid5,uid6,uid7',
                'whitelist': '白名单处填写uid,格式为uid1,uid2,uid，中奖天选后防止取关会自动添加上',
                'DesignateUp': '设定要投币的uid可以是你喜欢的up,格式为uid1,uid2,',
                'proxylist': '代理列表格式字符串，格式为"ip:port" 不写就默认不代理'
            }
        }
        async with aiofiles.open('../Basic/config.yaml', mode='w', encoding='utf-8') as f:
            for key, value in data.items():
                await f.write(key + ':\n')
                for k, v in value.items():
                    await f.write('  ' + k + ': ' + str(v) + '  # ' + comments[key][k] + '\n')
            self.logger.info('config.yaml is created,please go to Modify Configuration File')

    async def check_config(self):
        datalist = ['cookie', 'coin', 'spider_page', 'spider_thread', 'blacklist', 'whitelist', 'DesignateUp',
                    'proxylist']
        with open('../Basic/config.yaml', 'r', encoding='utf-8') as f:
            # 检查配置文件是否正确
            data = yaml.safe_load(f)
            if data is not None:
                for key, value in data.items():
                    # 处理配置数据
                    # print(k, v)
                    not_found = set(datalist) - set(data[key].keys())
                    if not_found:
                        self.logger.info(f'{key}以下键未在 config.yaml 中找到：{not_found},自动添加默认值')
                        for k1 in not_found:
                            if k1 == 'cookie':
                                data[key][k1] = 'xxxx'
                            elif k1 == 'drop':
                                data[key][k1] = 0
                            elif k1 == 'spider_page':
                                data[key][k1] = 50
                            elif k1 == 'spider_thread':
                                data[key][k1] = 7
                            else:
                                data[key][k1] = []
                            # 在config.yaml中添加键值对
                        await self.correct_config(data)
                return data
            else:
                self.logger.info('config.yaml 不正确。请检查文件是否正确。')
                return None

    async def correct_config(self, data):
        with open('../Basic/config.yaml', 'w', encoding='utf-8') as f:
            f.write(yaml.dump(data, default_flow_style=False))
        self.logger.info('config.yaml,修改完成')

    async def start(self):
        # 检查配置文件是否存在
        if not os.path.exists('../Basic/config.yaml'):
            self.logger.info('config.yaml 不存在，开始创建')
            await self.create_config()
            sys.exit(1)
        else:
            data = await self.check_config()
            if data is not None:
                return data


# bilibili daily

if __name__ == '__main__':
    con = Config()
    asyncio.run(con.start())
