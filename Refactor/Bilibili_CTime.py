import random
import time
import requests
from Bilibili_User import *


class ChosenTime(UserElement):
    def __init__(self):
        super().__init__()
        self.cookie = self.fetch_cookies()
        self.csrf = self.fetch_csrf()

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
                time.sleep(random.randint(3, 5))

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
        uid = []
        for i in range(len(data2)):
            if not data2[i]["pendant_info"].values():
                continue
            else:
                if list(data2[i]["pendant_info"].keys())[0] == '1':
                    if len(data2[i]['pendant_info'].keys()) > 1:
                        if data2[i]['pendant_info']['2']['content'] == '天选时刻':
                            self.logger.info("发现一个天选时刻")
                            roomId.append(data2[i]['roomid'])
                            uid.append(data2[i]['uid'])
                        else:
                            continue
                    else:
                        continue
                else:
                    if data2[i]['pendant_info']['2']['content'] == '天选时刻':
                        self.logger.info("发现一个天选时刻")
                        roomId.append(data2[i]['roomid'])
                        uid.append(data2[i]['uid'])
                    else:
                        continue
        return roomId, uid

    def cyc_get_roomId(self, pid, aid, csrf):
        page = 0
        while True:
            time.sleep(random.randint(2, 3))
            page += 1
            data2 = self.get_roomId(pid, aid, page)
            if len(data2) == 0:
                self.logger.info("扫描完毕")
                break
            elif page == 51:
                self.logger.info('页面到达51页,扫下去也没有意义，停止')
                break
            else:
                roomid, uid = self.cope_roomId(data2)
                if len(roomid) > 0:
                    rid = self.check_Room(roomid[0])
                    code = self.TianXuan(roomid[0], rid, csrf)
                    gid = self.check_group()
                    if len(gid) > 0:
                        if code == 0:
                            self.logger.info("存在天选时刻分组，将用户%s移动到天选时刻分组" % uid[0])
                            time.sleep(1)
                            self.move_user(gid[0], uid[0], csrf)
                        else:
                            continue
                    else:
                        self.logger.info("不存在天选时刻分组，将创建天选时刻分组")
                        gid = self.make_group(csrf)
                        if len(gid) > 0: self.logger.info("创建天选时刻分组成功")
                        self.move_user(gid[0], uid[0], csrf)
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
                    self.logger.info('success')
                    return data4['code']
                else:
                    self.logger.info(data4['message'])
                    return data4['code']
            else:
                self.logger.error('天选失败，状态码：%s' % response.status_code)
        except Exception as e:
            self.logger.error('天选失败，原因：%s' % e)

    def check_group(self):
        gid = []
        url_group = "http://api.bilibili.com/x/relation/tags"
        try:
            response = requests.get(url_group, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 0:
                    for i in range(len(data['data'])):
                        if data['data'][i]['name'] == '天选时刻':
                            gid.append(data['data'][i]['tagid'])
                            break
                        else:
                            pass
                    return gid
                else:
                    self.logger.info(data)
            else:
                self.logger.error('获取信息失败，状态码：%s' % response.status_code)
        except Exception as e:
            self.logger.error('获取信息失败，原因：%s' % e)

    def make_group(self, csrf):
        g_id = []
        url_make = "http://api.bilibili.com/x/relation/tag/create"
        try:
            data = {'tag': '天选时刻', 'csrf': csrf}
            response = requests.post(url_make, headers=self.headers, data=data)
            if response.status_code == 200:
                data2 = response.json()
                if data2['code'] == 0:
                    self.logger.info("创建分组成功")
                    self.logger.info(data2)
                    g_id.append(data2['data']['tagid'])
                    return g_id
                else:
                    self.logger.info(data2)
            else:
                self.logger.error('创建分组失败，状态码：%s' % response.status_code)
        except Exception as e:
            self.logger.error('创建分组失败，原因：%s' % e)

    def move_user(self, gid, uid, csrf):
        url_relationship = "http://api.bilibili.com/x/relation/tags/moveUsers"
        try:
            data = {'beforeTagids': 0, 'afterTagids': gid, 'fids': uid, 'csrf': csrf}
            response = requests.post(url_relationship, headers=self.headers, data=data)
            if response.status_code == 200:
                data3 = response.json()
                if data3['code'] == 0:
                    self.logger.info("移动成功")
                else:
                    self.logger.info(data3)
            else:
                self.logger.error('移动失败，状态码：%s' % response.status_code)
        except Exception as e:
            self.logger.error('移动失败，原因：%s' % e)

    def run(self):
        for i in range(len(self.cookie)):
            self.headers['cookie'] = self.cookie[i]
            data1 = self.collect_area()
            self.cope_area(data1, self.csrf[i])


if __name__ == '__main__':
    ct = ChosenTime()
    ct.run()
