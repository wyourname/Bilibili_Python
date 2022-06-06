import random
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from Bilibili_User import *


class ChosenTime(UserElement):
    def __init__(self):
        super().__init__()
        self.cookie = self.fetch_cookies()
        self.csrf = self.fetch_csrf()
        self.max_page = self.fetch_page()
        self.max_thread = self.fetch_thread()
        try:
            self.pool = ThreadPoolExecutor(max_workers=self.max_thread)
        except ValueError as e:
            self.logger.error('初始化线程池失败，原因：%s' % e)
            exit(1)

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

    def cope_area(self, data1, csrf):  # 这里是核心分区的扫描
        for i in data1:
            self.logger.info('--------->正在扫描《' + i['name'] + "》<---------")
            data_id, data_name = self.cope_min_area(i['list'])
            self.pool.submit(self.cycle, i['id'], data_id, data_name, csrf)
        self.pool.shutdown(wait=True)
        self.logger.info('--------->程序结束<---------')

    @staticmethod
    def cope_min_area(data1):
        data_id = []
        data_name = []
        for i in data1:
            data_id.append(i['id'])
            data_name.append(i['name'])
        return data_id, data_name

    def cycle(self, parents_id, child_id, child_title, csrf):
        for i in child_id:
            self.logger.info('      ->正在扫描' + child_title[child_id.index(i)] + "<-")
            self.cycle_page(parents_id, i, csrf)

    def cycle_page(self, parents_id, child_id, csrf):
        page = 0
        while True:
            page += 1
            if page > self.max_page:
                self.logger.info("页面到达设置的最大页数，结束扫描")
                break
            self.logger.info('      ->正在扫描第%s页' % page)
            data3 = self.scanner_page(parents_id, child_id, page)
            if data3:
                self.scan_page_room(data3, csrf)
            else:
                break
            time.sleep(1)

    def scanner_page(self, parents_id, child_id, page):  # 搜寻子分区的直播间
        try:
            url_ct = "https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id" \
                     "=%s&area_id=%s&page=%s" % (parents_id, child_id, page)
            response = requests.get(url_ct, headers=self.headers)
            if response.status_code == 200:
                data3 = response.json()['data']['list']
                return data3
            else:
                self.logger.error('获取第%s的%s页直播间信息失败，状态码：%s' % (child_id, page, response.status_code))
        except Exception as e:
            self.logger.error('获取第%s的%s页直播间信息失败，原因：%s' % (child_id, page, e))

    def scan_page_room(self, data3, csrf):
        for i in data3:
            room_info = self.screen_out_room(i)
            if room_info is not None:
                self.check_Room(room_info[0], room_info[1], csrf)
            else:
                continue

    def screen_out_room(self, data):
        if "2" in data['pendant_info']:
            if data['pendant_info']['2']['content'] == '天选时刻':
                self.logger.info("直播间：%s --发现了天选时刻" % data['uname'])
                return data['roomid'], data['uid']
            else:
                pass
        else:
            pass

    def check_Room(self, roomid, uid, csrf):
        url_check = "https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/Check?roomid=%s" % roomid
        try:
            response = requests.get(url_check, headers=self.headers)
            if response.status_code == 200:
                data3 = response.json()
                if data3['code'] == 0:
                    self.logger.info("奖品是：%s,数量为：%s,需要条件：%s" % (
                        data3['data']['award_name'], data3['data']['award_num'], data3['data']['require_text']))
                    self.TX(data3['data']['id'], roomid, uid, csrf)
                else:
                    self.logger.info(data3)
            else:
                self.logger.error('检查房间信息失败，状态码：%s' % response.status_code)
        except Exception as e:
            self.logger.error('检查房间信息失败，原因：%s' % e)

    def TX(self, rid, roomid, uid, csrf):
        url_tx = "https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/Join"
        try:
            data = {'id': rid, 'platfrom': 'pc', 'roomid': roomid, 'csrf': csrf}
            response = requests.post(url_tx, headers=self.headers, data=data)
            if response.status_code == 200:
                data4 = response.json()
                if data4['code'] == 0:
                    if data4['message'] == '':
                        self.logger.info("参与天选成功")
                        time.sleep(1)
                        self.control_user(uid, csrf)
                    else:
                        self.logger.info(data4['message'])
                else:
                    self.logger.info(data4['message'])
                    return data4['code']
            else:
                self.logger.error('天选失败，状态码：%s' % response.status_code)
        except Exception as e:
            self.logger.error('天选失败，原因：%s' % e)

    def control_user(self, uid, csrf):
        gid = self.check_group()
        if gid is not None:
            self.logger.info("存在天选时刻分组，执行移动用户操作")
            self.move_user(gid, uid, csrf)
        else:
            self.logger.info("不存在天选时刻分组，执行创建分组操作")
            gid = self.create_group(csrf)
            if gid is not None:
                self.move_user(gid, uid, csrf)
            else:
                self.logger.info("未知错误")

    def check_group(self):
        url_group = "http://api.bilibili.com/x/relation/tags"
        try:
            response = requests.get(url_group, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 0:
                    for i in range(len(data['data'])):
                        if data['data'][i]['name'] == '天选时刻':
                            return data['data'][i]['tagid']
                        else:
                            pass
                else:
                    self.logger.error(data)
            else:
                self.logger.error('获取信息失败，状态码：%s' % response.status_code)
        except Exception as e:
            self.logger.error('获取信息失败，原因：%s' % e)

    def create_group(self, csrf):
        url_make = "http://api.bilibili.com/x/relation/tag/create"
        try:
            data = {'tag': '天选时刻', 'csrf': csrf}
            response = requests.post(url_make, headers=self.headers, data=data)
            if response.status_code == 200:
                data2 = response.json()
                if data2['code'] == 0:
                    self.logger.info("创建分组成功")
                    return data2['data']['tagid']
                else:
                    self.logger.error(data2)
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
                    self.logger.error(data3)
            else:
                self.logger.error('移动失败，状态码：%s' % response.status_code)
        except Exception as e:
            self.logger.error('移动失败，原因：%s' % e)

    def run(self):
        self.logger.info('-------开始执行--------')
        for i in range(len(self.csrf)):
            self.logger.info('------》开始执行帐号%s' % (i + 1))
            self.headers['Cookie'] = self.cookie[i]
            data = self.collect_area()
            self.cope_area(data, self.csrf[i])


if __name__ == '__main__':
    ct = ChosenTime()
    ct.run()

