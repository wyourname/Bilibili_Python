import random
import time

import requests

from Refactor_UserElement import *


class ChosenTime(UserElement):
    def __init__(self):
        super().__init__()
        self.cookie = self.fetch_cookies()
        self.csrf = self.fetch_csrf()
        self.roomId = []

    def collect_area(self):
        try:
            response = requests.get(self.url7, headers=self.headers)
            if response.status_code == 200:
                data1 = response.json()['data']
                return data1
            else:
                self.logger.error('获取全部直播分区失败，状态码：%s' % response.status_code)
        except Exception as e:
            self.logger.error('获取全部直播分区失败，原因：%s' % e)

    def cope_area(self, data1, csrf):
        for i in range(len(data1)):
            self.logger.info('--------->正在扫描' + data1[i]['name'] + "<---------")
            for j in range(len(data1[i]["list"])):
                self.logger.info("扫描^^^----->:" + data1[i]["list"][j]["name"])
                self.cyc_get_roomId(data1[i]["id"], data1[i]["list"][j]["id"], csrf)
                time.sleep(random.randint(5, 7))

    def get_roomId(self, pid, aid, page):
        url_ct = "https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=%s" \
                 "&area_id=%s&page=%s" % (pid, aid, page)
        try:
            response = requests.get(url_ct, headers=self.headers)
            if response.status_code == 200:
                data2 = response.json()['data']['list']
                return data2
            else:
                self.logger.error('获取全部直播分区失败，状态码：%s' % response.status_code)
        except Exception as e:
            self.logger.error('获取全部直播分区失败，原因：%s' % e)

    def cope_roomId(self, data2):
        roomId = []
        for i in range(len(data2)):
            if not data2[i]["pendant_info"].values():
                continue
            else:
                if list(data2[i]["pendant_info"].keys())[0] == '1':
                    if len(data2[i]['pendant_info'].keys()) > 1:
                        if data2[i]['pendant_info']['2']['content'] == '天选时刻':
                            self.logger.info("发现一个天选时刻")
                            roomId.append(data2[i]['roomid'])
                            self.logger.info("房间号：%s" % data2[i]['roomid'])
                        else:
                            continue
                    else:
                        continue
                else:
                    if data2[i]['pendant_info']['2']['content'] == '天选时刻':
                        self.logger.info("发现一个天选时刻")
                        self.logger.info("房间号：%s" % data2[i]['roomid'])
                        roomId.append(data2[i]['roomid'])
                    else:
                        continue
        return roomId

    def cyc_get_roomId(self, pid, aid, csrf):
        page = 1
        while True:
            time.sleep(random.randint(3, 5))
            page += 1
            self.logger.info("正在扫描第%s页" % page)
            data2 = self.get_roomId(pid, aid, page)
            if len(data2) == 0:
                self.logger.info("扫描完毕")
                break
            else:
                roomid = self.cope_roomId(data2)
                if len(roomid) > 0:
                    id = self.check_Room(roomid[0])
                    self.logger.info(id)
                    self.TianXuan(roomid[0], id, csrf)
                else:
                    continue

    def check_Room(self, roomid):
        url_check = "https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/Check?roomid=%s" % roomid
        try:
            response = requests.get(url_check, headers=self.headers)
            if response.status_code == 200:
                data3 = response.json()
                if data3['code'] == 0:
                    self.logger.info("奖品：%s,数量：%s,需要条件：%s" % (
                        data3['data']['award_name'], data3['data']['award_num'], data3['data']['require_text']))
                    return data3['data']['id']
                else:
                    self.logger.info(data3)
            else:
                self.logger.error('获取房间信息失败，状态码：%s' % response.status_code)
        except Exception as e:
            self.logger.error('获取房间信息失败，原因：%s' % e)

    def TianXuan(self, roomid, id, csrf):
        url_tianxuan = "https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/Join"
        try:
            data = {'id': id, 'platfrom': 'pc', 'roomid': roomid, 'csrf': csrf}
            response = requests.post(url_tianxuan, headers=self.headers, data=data)
            if response.status_code == 200:
                data4 = response.json()
                if data4['code'] == 0:
                    self.logger.info("天选成功")
                else:
                    self.logger.info(data4)
            else:
                self.logger.error('天选失败，状态码：%s' % response.status_code)
        except Exception as e:
            self.logger.error('天选失败，原因：%s' % e)

    def run(self):
        for i in range(len(self.cookie)):
            self.headers['cookie'] = self.cookie[i]
            data1 = self.collect_area()
            self.cope_area(data1, self.csrf[i])


if __name__ == '__main__':
    ct = ChosenTime()
    ct.run()

    # a = ct.get_roomId()
    # ct.cope_roomId(a)
    # ct.cope_roomId(a)
    # print(ct.roomId)
