"""
cron: 1 1 1 1 *
new Env('天选时刻-进程版')
帐号少的不推荐使用该版本
"""
import logging
import os
import signal
import random
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait, ALL_COMPLETED
from Bilibili_User import *

logging.basicConfig(level=logging.INFO, format='%(message)s')


class Bilibili_CTime(Basic):
    def __init__(self):
        super().__init__()
        self.max_page = self.fetch_page()
        self.max_thread = self.fetch_thread()
        self.black_list = self.fetch_black_list()
        self.cpu_count = os.cpu_count()
        self.pid = os.getpid()

    def check_group(self, csrf):
        try:
            group = self.get_requests(self.url9)
            tag_id = self.cope_group(group)
            if tag_id is not None:
                self.logger.info(f'{"**" * 5}存在天选时刻分组{"**" * 5}')
                time.sleep(15)
                self.Scan_all_live(tag_id, csrf)
            else:
                self.logger.info('不存在分组,开始创建')
                tag_id = self.create_group(csrf)
                self.Scan_all_live(tag_id, csrf)
        except Exception as e:
            self.logger.info(e)
            os.kill(os.getpid(), signal.SIGKILL)

    @staticmethod
    def cope_group(group):
        for i in group['data']:
            if i['name'] == '天选时刻':
                return i['tagid']
            else:
                pass

    def create_group(self, csrf):
        data = {'tag': '天选时刻', 'csrf': csrf}
        group = self.post_requests(self.create_url, data)
        if group['code'] == 0:
            self.logger.info('创建成功')
            return group['data']['tagid']
        else:
            self.logger.info('创建失败,后续关注的up在默认分组')
            return 0

    def Scan_all_live(self, tag_id, csrf):
        all_live = self.get_requests(self.url7)
        if all_live['code'] == 0:
            self.cope_all_live(all_live, tag_id, csrf)
        else:
            self.logger.info('扫描全部分区失败')
            sys.exit(0)

    def cope_all_live(self, all_live, tag_id, csrf):
        for i in all_live['data']:
            min_id = [i['id'] for i in i['list']]
            # min_name = [i['name'] for i in i['list']]
            self.logger.info(f'扫描【{i["name"]}】分区')
            self.cycle_live(i['id'], min_id, tag_id, csrf)

    def cycle_live(self, parent_id, min_live_id, tag_id, csrf):
        with ThreadPoolExecutor(max_workers=self.max_thread) as executor:
            task_list = []
            for i in min_live_id:
                task_list.append(executor.submit(self.cycle_page, parent_id, i, tag_id, csrf))

    def cycle_page(self, parent_id, child_id, tag_id, csrf):
        # try:
        #     os.kill(self.pid, 0)
        # except Exception:
        #     self.logger.info('The main process does not exist and will wait for the remaining processes to complete the task and kill')
        #     os.kill(os.getpid(), signal.SIGKILL)
        for i in range(1, self.max_page + 1):
            try:
                os.kill(self.pid, 0)
            except Exception:
                self.logger.info('The main process does not exist and will wait for the remaining processes to complete the task and kill')
                os.kill(os.getpid(), signal.SIGKILL)
            live_page = self.url_all % (parent_id, child_id, i)
            page_info = self.get_requests(live_page)
            if page_info['code'] == 0:
                if page_info['data']['list']:
                    self.scan_live_page(page_info, tag_id, csrf)
                else:
                    break
            if page_info['code'] == -412:
                self.logger.info("检测到被拦截,结束程序，一小时后再试")
                os.kill(os.getpid(), signal.SIGKILL)
                # os._exit(0)

    def scan_live_page(self, page_info, tag_id, csrf):
        for i in page_info['data']['list']:
            room_info = self.screen_ct_room(i)
            if room_info:
                self.check_room(room_info[0], room_info[1], tag_id, csrf)
            else:
                continue

    @staticmethod
    def screen_ct_room(i):
        if '2' in i['pendant_info']:
            if i['pendant_info']['2']['content'] == '天选时刻':
                return i['roomid'], i['uname']
            else:
                pass

    def check_room(self, room_id, uname, tag_id, csrf):
        url = self.url_check % room_id
        tx_info = self.get_requests(url)
        if tx_info['code'] == 0:
            award = self.screen_condition(tx_info['data']['award_name'])
            require = self.screen_condition(tx_info['data']['require_text'])
            if award or require:
                pass
            else:
                if tx_info['data']['gift_id'] == 0:
                    self.logger.info(
                        f"【{uname}】--【{tx_info['data']['award_name']}】--【{tx_info['data']['require_text']}】")
                    self.tx_join(tx_info['data']['ruid'], tx_info['data']['id'], uname, room_id, tag_id, csrf)
                else:
                    pass

    @staticmethod
    def screen_condition(condition):
        pattern = re.compile(r'大航海|舰长|.?车车?|手照|代金券|优惠券|勋章|提督|男')
        if pattern.findall(condition):
            return True
        else:
            return False

    def tx_join(self, uid, tid, uname, room_id, tag_id, csrf):
        if self.black_list_check(uid):
            self.logger.info(f"【{uname}】已在黑名单中")
        else:
            # self.logger.info(csrf)
            data = {'id': tid, 'platfrom': 'pc', 'roomid': room_id, 'csrf': csrf}
            join_info = self.post_requests(self.url_tx, data)
            if join_info['code'] == 0:
                self.logger.info(f'-------【成功参加"{uname}"的天选】')
                self.send_danmu(room_id, csrf)
                self.relationship_check(uid, uname, tag_id, csrf)
            else:
                self.logger.info(join_info['message'])

    def black_list_check(self, uid):
        if self.black_list:
            for i in self.black_list:
                if i == uid:
                    return True
                else:
                    return False
        else:
            return False

    def relationship_check(self, uid, uname, tag_id, csrf):
        url = self.url_re % uid
        relationship = self.get_requests(url)
        if relationship['code'] == 0:
            if relationship['data']['attribute'] == 1 or relationship['data']['attribute'] == 2:
                if relationship['data']['tag'] is None:
                    self.Move_User(tag_id, uid, uname, csrf)
                else:
                    pass
            else:
                pass

    def Move_User(self, gid, uid, uname, csrf):
        data = {'beforeTagids': 0, 'afterTagids': gid, 'fids': uid, 'csrf': csrf}
        Move_info = self.post_requests(self.url_relationship, data)
        if Move_info['code'] == 0:
            self.logger.info(f'------->【{uname}】--->改变分组成功')
        else:
            self.logger.info(Move_info['message'])

    def send_danmu(self, room_id, csrf):
        time.sleep(1)
        emotion_list = ['official_147', 'official_109', 'official_113', 'official_120', 'official_150', 'official_103', 'official_128', 'official_133', 'official_149', 'official_124', 'official_146', 'official_148', 'official_102', 'official_121', 'official_137', 'official_118', 'official_129', 'official_108', 'official_104', 'official_105', 'official_106', 'official_114', 'official_107', 'official_110', 'official_111', 'official_136', 'official_115', 'official_116', 'official_117', 'official_119', 'official_122', 'official_123', 'official_125', 'official_126', 'official_127', 'official_134', 'official_135', 'official_138']
        rnd = int(time.time())
        emotion = random.choice(emotion_list)
        data = {'bubble': 0, 'msg': emotion, 'color': 16777215, 'fontsize': 25, 'mode': 1, 'rnd': rnd, 'dm_type': 1,
                'roomid': room_id, 'csrf': csrf}
        danmu_info = self.post_requests(self.send, data)
        if danmu_info['code'] == 0:
            self.logger.info(f'------->发送弹幕成功')
        else:
            self.logger.info(danmu_info['message'])

    def config_pre(self):
        self.logger.info(f"总共{len(self.cookies)}个帐号")
        if self.cpu_count <= 2:
            self.logger.info("CPU核数小于2，用该版本意义不大,换用ctime吧")
            os.kill(self.pid, signal.SIGKILL)
        if 5 > self.cpu_count > 2:
            if len(self.cookies) > self.cpu_count:
                self.max_thread = self.max_thread // self.cpu_count
                return self.cpu_count
            else:
                self.max_thread = self.max_thread // len(self.cookies)
                return self.cpu_count
        else:
            if len(self.cookies) <= 4:
                self.max_thread = self.max_thread // len(self.cookies)
                return len(self.cookies)
            else:
                self.max_thread = self.max_thread // 4
                return 4

    def decorate(self):
        self.logger.info("脚本由GitHub@王权富贵233提供")
        self.logger.info("该脚本仅供学习交流，仅供学习参考，仅供学习参考!!!")
        self.logger.info("帐号并发一次最多四，请勿使用我的脚本呆瓜，不喜欢的话请自行删除")

    def run(self):
        self.decorate()
        process = self.config_pre()
        self.logger.info(f'单帐号线程数为{self.max_thread}')
        with ProcessPoolExecutor(max_workers=process) as executor:
            task_p = []
            for i in range(len(self.cookies)):
                self.headers['Cookie'] = self.cookies[i]
                self.headers['user-agent'] = random.choice(self.ua_list)
                self.headers['referer'] = "https://live.bilibili.com/"
                user_info = self.get_requests(self.url)
                self.cope_info(user_info)
                task_p.append(executor.submit(self.check_group, self.csrfs[i]))
                time.sleep(2)
            wait(task_p, return_when=ALL_COMPLETED)
        self.logger.info(f"{'='*5}所有帐号全部完成{'='*5}")


if __name__ == '__main__':
    ctime = Bilibili_CTime()
    ctime.run()
