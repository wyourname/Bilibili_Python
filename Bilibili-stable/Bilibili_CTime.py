import logging
import os
import random
import signal
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from Bilibili_User import *

logging.basicConfig(level=logging.INFO, format='%(message)s')


# logger = logging.getLogger()


class Bilibili_CTime(Basic):
    def __init__(self):
        super().__init__()
        self.max_page = self.fetch_page()
        self.max_thread = self.fetch_thread()
        self.black_list = self.fetch_black_list()

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
            # os._exit(0)

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
            os.kill(os.getpid(), signal.SIGKILL)
            sys.exit(0)

    def cope_all_live(self, all_live, tag_id, csrf):
        for i in all_live['data']:
            min_id = [i['id'] for i in i['list']]
            min_name = [i['name'] for i in i['list']]
            self.logger.info(f'扫描【{i["name"]}】分区')
            self.cycle_live(i['id'], min_id, tag_id, csrf)

    def cycle_live(self, parent_id, min_live_id, tag_id, csrf):
        # self.logger.info(os.getpid())
        with ThreadPoolExecutor(max_workers=self.max_thread) as executor:
            task_list = []
            for i in min_live_id:
                try:
                    task_list.append(executor.submit(self.cycle_page, parent_id, i, tag_id, csrf))
                except Exception as e:
                    self.logger.info(e)
                    # os.kill(os.getpid(), signal.SIGKILL)
                    # os._exit(0)
            # wait(task_list, return_when=ALL_COMPLETED)

    def cycle_page(self, parent_id, child_id, tag_id, csrf):
        for i in range(1, self.max_page + 1):
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
            data = {'id': tid, 'platfrom': 'pc', 'roomid': room_id, 'csrf': csrf}
            join_info = self.post_requests(self.url_tx, data)
            if join_info['code'] == 0:
                self.logger.info(f'【成功参加"{uname}"的天选】')
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
            self.logger.info(f'{uname}->【改变分组成功】')
        else:
            self.logger.info(Move_info['message'])

    def decorate(self):
        self.logger.info("脚本由GitHub@王权富贵233提供")
        self.logger.info("该脚本仅供学习交流，仅供学习参考，仅供学习参考")
        self.logger.info("脚本现已支持黑名单，前往Bilibili_config.json添加黑名单")
        self.logger.info("格式：black_list = [uid1,uid2,uid3,...,...] uid为数字，逗号为英文逗号")

    def run(self):
        self.decorate()
        for i in range(len(self.cookies)):
            self.headers['Cookie'] = self.cookies[i]
            self.headers['user-agent'] = random.choice(self.ua_list)
            self.headers['referer'] = "https://live.bilibili.com/"
            self.cope_info(self.get_requests(self.url))
            self.check_group(self.csrfs[i])
            self.logger.info(f"{'*'*5}第{i+1}帐号结束{'*'*5}")


if __name__ == '__main__':
    ctime = Bilibili_CTime()
    ctime.run()
