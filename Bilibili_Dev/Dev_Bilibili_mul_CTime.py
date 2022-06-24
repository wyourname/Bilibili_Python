import re
import sys
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from Dev_Bilibili_User import *


class Refactor_Bilibili_CTime(Basic):
    def __init__(self):
        super().__init__()
        self.max_page = self.fetch_page()
        self.max_thread = self.fetch_thread()
        self.black_list = self.fetch_black_list()
        try:
            self.pool = ThreadPoolExecutor(max_workers=self.max_thread)
        except ValueError as e:
            self.logger.error('初始化线程池失败，原因：%s' % e)
            exit(1)

    def check_group(self, csrf):
        group = self.get_requests(self.url9)
        tag_id = self.cope_group(group)
        if tag_id:
            self.logger.info("+++++++++>开始扫描全部分区<++++++++++")
            self.scan_all_area(tag_id, csrf)
        else:
            self.logger.info("=========>未发现天选时刻分组，开始创建<=========")
            tag_id1 = self.create_group(csrf)
            self.scan_all_area(tag_id1, csrf)
            return

    def create_group(self, csrf):
        data = {'tag': '天选时刻', 'csrf': csrf}
        group = self.post_requests(self.create_url, data)
        if group['code'] == 0:
            self.logger.info("=========>创建天选时刻分组成功<=========")
            return group['data']['tagid']
        else:
            self.logger.error("=========>创建天选时刻分组失败<=========")
            return

    def cope_group(self, group):
        for i in group['data']:
            if i['name'] == '天选时刻':
                self.logger.info("=========>发现有天选时刻分组，继续执行<=========")
                return i['tagid']
            else:
                pass

    def scan_all_area(self, gid, csrf):
        all_area = self.get_requests(self.url7)
        self.cope_all_area(all_area, gid, csrf)

    def cope_all_area(self, all_area, gid, csrf):
        tasklist = []
        for i in all_area['data']:
            self.logger.info('*********>正在扫描《' + i['name'] + "》<*********")
            area_id, area_name = self.cope_min_area(i['list'])
            task = self.pool.submit(self.cycle_min_area, i['id'], area_id, area_name, gid, csrf)
            tasklist.append(task)
        wait(tasklist, return_when=ALL_COMPLETED)
        self.logger.info('*********>全部扫描完成<*********')

    @staticmethod
    def cope_min_area(data1):
        data_id = []
        data_name = []
        for i in data1:
            data_id.append(i['id'])
            data_name.append(i['name'])
        return data_id, data_name

    def cycle_min_area(self, parent_id, area_id, area_name, gid, csrf):
        for i in area_id:
            self.logger.info('      ->正在扫描' + area_name[area_id.index(i)] + "<-")
            self.cycle_page(parent_id, i, gid, csrf)

    def cycle_page(self, parent_id, area_id, gid, csrf):
        page = 0
        while True:
            page += 1
            url_page = self.url_all % (parent_id, area_id, page)
            if page > self.max_page:
                self.logger.info('      ->Scan reached maximum number of pages, stop<-')
                break
            page_info = self.get_requests(url_page)
            if page_info['data']['list']:
                self.scan_room(page_info['data']['list'], gid, csrf)
            else:
                self.logger.info('      ->Scan reached the end of the page, stop<-')
                break

    def scan_room(self, page_info, gid, csrf):
        for i in page_info:
            room_info = self.screen_out_room(i)
            if room_info is not None:
                self.check_Room(room_info[0], room_info[1], gid, csrf)
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

    def check_Room(self, room_id, uid, gid, csrf):
        url = self.url_check % room_id
        tx_info = self.get_requests(url)
        if tx_info['code'] == 0:
            result = self.screen_condition(tx_info['data']['award_name'])
            if result:
                self.logger.info("筛选去掉【奖品】：%s" % tx_info['data']['award_name'])
            else:
                self.logger.info("【奖品】：%s ---【条件】: %s" % (tx_info['data']['award_name'], tx_info['data']['require_text']))
                self.TX_Join(tx_info['data']['id'], room_id, gid, uid, csrf)

    @staticmethod
    def screen_condition(condition):
        pattern = re.compile(r'大航海|舰长|.?车车?|手照|代金券|优惠券')
        if pattern.findall(condition):
            return True
        else:
            return False

    def black_screen(self, uid):
        if self.black_list:
            for i in self.black_list:
                if i == uid:
                    return True
            else:
                return False
        else:
            return False

    def TX_Join(self, rid, room_id, gid, uid, csrf):
        if self.black_screen(uid):
            self.logger.info("【UID】跳过：%s ---【原因】: 在设置的黑名单中" % uid)
        else:
            data = {'id': rid, 'platfrom': 'pc', 'roomid': room_id, 'csrf': csrf}
            Join_info = self.post_requests(self.url_tx, data)
            self.cope_Join(Join_info, gid, uid, csrf)

    def cope_Join(self, join_info, gid, uid, csrf):
        if join_info['code'] == 0:
            self.logger.info("【参加天选抽奖成功】,等待2秒改变用户组")
            time.sleep(2)
            self.Move_User(gid, uid, csrf)
        else:
            self.logger.info(join_info['message'])

    def Move_User(self, gid, uid, csrf):
        data = {'beforeTagids': 0, 'afterTagids': gid, 'fids': uid, 'csrf': csrf}
        Move_info = self.post_requests(self.url_relationship, data)
        if Move_info['code'] == 0:
            self.logger.info("【更改分组成功】")
        else:
            self.logger.info(Move_info['message'])

    def decorate(self):
        self.logger.info("脚本由GitHub@王权富贵233提供")
        self.logger.info("该脚本仅供学习交流，仅供学习参考，仅供学习参考")
        self.logger.info("脚本不保证稳定性，请自行测试")

    def run(self):
        self.decorate()
        for i in range(len(self.cookies)):
            self.headers['Cookie'] = self.cookies[i]
            user_info = self.get_requests(self.url)
            self.cope_info(user_info)
            self.check_group(self.csrfs[i])
            self.logger.info("##########>第%s个帐号结束<##########" % (i + 1))
        self.pool.shutdown()
        sys.exit(0)


if __name__ == '__main__':
    bilibili = Refactor_Bilibili_CTime()
    bilibili.run()
