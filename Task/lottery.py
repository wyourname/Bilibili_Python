import asyncio
import os
import random
import signal
import time
import re
import sys
import os
pythonpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(pythonpath)
from Basic.depend import necessary


class Lottery(necessary):
    def __init__(self):
        super().__init__()
        self.black_up = None
        self.page = None

    async def check_group(self, csrf):
        try:
            group = await self.requests_method(self.url9, 'get')
            tag_id = next((i['tagid'] for i in group['data'] if i['name'] == '天选时刻'), None)
            if tag_id is not None:
                self.logger.info(f'{"@" * 5}存在天选时刻分组{"@" * 5}')
                # 分区
                await self.scan_all_partition(tag_id, csrf)
            else:
                self.logger.info('不存在分组,开始创建')
                tag_id = self.create_group(csrf)
        except Exception as e:
            self.logger.info(e)
            os.kill(os.getpid(), signal.SIGKILL)

    async def create_group(self, csrf):
            data = {'tag': '天选时刻', 'csrf': csrf}
            message = await self.requests_method(self.create_url, 'post', data=data)
            if message['code'] == 200:
                self.logger.info('创建天选时刻分组成功')
                return message['data']['tagid']
            else:
                return 0


    async def scan_all_partition(self,tag_id, csrf):
        all_partitions = await self.requests_method(self.url7, 'get')
        if all_partitions['code'] == 0:
            for subpartitions in all_partitions['data']:
                self.logger.info("扫描:【" + subpartitions['name']+"】")
                for small_partition in subpartitions['list']:
                    await self.scan_small_partitions(subpartitions['id'], small_partition['id'],tag_id, csrf)

    async def scan_small_partitions(self, parent_id, partition_id,tag_id,csrf):    # 扫描小分区多少页
        for i in range(1, self.page+1):
            live_page = self.url_all % (parent_id, partition_id, i)
            msg = await self.requests_method(live_page, 'get')
            if msg['code'] == 0 and msg['data']['list'] is not None:  # 如果是该分区最后一页则break掉，不是就循环到最设定页数
                for i in msg['data']['list']:
                    if '2' in i['pendant_info']:
                        if i['pendant_info']['2']['content'] == '天选时刻':
                            await self.confirm_room(i['roomid'],i['uname'],tag_id,csrf)
            else:
                break
            if msg['code'] == -412:
                self.logger.info("检测到被拦截,结束程序，一小时后再试")
                os.kill(os.getpid(), signal.SIGKILL)
                os._exit(0)

    
    async def confirm_room(self, *args):
        room_url = self.url_check % args[0]
        lottery_info = await self.requests_method(room_url, 'get')
        pattern = re.compile(r"大航海|舰长|.?车车?|手照|代金券|优惠券|勋章|提督|男")
        if lottery_info['code'] == 0:
            if pattern.findall(lottery_info['data']['award_name']) or pattern.findall(lottery_info['data']['require_text']):
                self.logger.info(f"✖️ {args[1]}: {lottery_info['data']['award_name']}，要求为：{lottery_info['data']['require_text']}")
            else:
                if lottery_info['data']['gift_id'] == 0:
                    self.logger.info(f'{args[1]}: 【{lottery_info["data"]["award_name"]}】-- <{lottery_info["data"]["require_text"]}>')
                    await self.join_lottery(lottery_info['data']['ruid'],lottery_info['data']['id'],args[1],args[0],args[2],args[3])
                

    async def join_lottery(self, *args):
        # 0 uid/ 1 tid/ 2 uname / 3 roomid/ 4 tagid /5 csrf
        if args[0] not in self.black_up:
            data = {'id': args[1], 'platfrom': 'pc', 'roomid': args[3], 'csrf': args[5]}
            join_info = await self.requests_method(self.url_tx,data=data, method='post')
            if join_info['code'] == 0:
                self.logger.info(f'✔️ 参加{args[2]}的天选')
                await self.send_danmu(args[3], args[5])
                await self.check_relationship(args[0], args[2],args[4], args[5])
            else:
                self.logger.info(f'参加{args[2]}的天选错误情况：{join_info["message"]}')
        else:
            return

    async def check_relationship(self, *args):
        # 0 uid /1 uname /2 tagid /3 csrf
        relationship_url = self.url_re % args[0]
        more_info = await self.requests_method(relationship_url, 'get')
        if more_info['code'] == 0:
            if more_info['data']['attribute'] == 1 or more_info['data']['attribute'] == 2:
                if more_info['data']['tag'] is None:
                    await self.move_up(args[2], args[0], args[1], args[3])

    async def move_up(self, *args):
        # 0 tagid, 1 uid 2 uname 3 csrf
        data = {'beforeTagids': 0, 'afterTagids': args[0], 'fids': args[1], 'csrf': args[3]}
        move_info = await self.requests_method(self.url_relationship, data=data, method='post')
        if move_info['code'] == 0:
            self.logger.info(f'{args[2]}移至 天选时刻')
        else:
            self.logger.info(move_info['message'])

    async def send_danmu(self, room_id, csrf):
        emotion_list = ['official_147', 'official_109', 'official_113', 'official_120', 'official_150', 'official_103',
                        'official_128', 'official_133', 'official_149', 'official_124', 'official_146', 'official_148',
                        'official_102', 'official_121', 'official_137', 'official_118', 'official_129', 'official_108',
                        'official_104', 'official_105', 'official_106', 'official_114', 'official_107', 'official_110',
                        'official_111', 'official_136', 'official_115', 'official_116', 'official_117', 'official_119',
                        'official_122', 'official_123', 'official_125', 'official_126', 'official_127', 'official_134',
                        'official_135', 'official_138']
        rnd = int(time.time())
        emotion = random.choice(emotion_list)
        data = {'bubble': 0, 'msg': emotion, 'color': 16777215, 'fontsize': 25, 'mode': 1, 'rnd': rnd, 'dm_type': 1,
                'roomid': room_id, 'csrf': csrf}
        time.sleep(1.5)
        danmu_info = await self.requests_method(self.send,method='post',data=data)
        if danmu_info['code'] == 0:
            self.logger.info(f'✔️发送弹幕')
        else:
            self.logger.info(danmu_info['message'])

    async def run(self):
        cfg = await self.start()
        self.headers['referer'] = "https://live.bilibili.com/"
        for key, value in cfg.items():
            self.black_up = await self.back_k_data(key, 'blacklist')
            self.page = await self.back_k_data(key, 'spider_page')
            self.headers['Cookie'] = value['cookie']
            self.headers['user-agent'] = random.choice(self.ua_list)
            csrf_match = re.search(r"bili_jct=([^;]+)", value['cookie'])
            if csrf_match:
                csrf = csrf_match.group(1)
            if await self.verification_cookie(self.url):
                await self.check_group(csrf)


if __name__ == '__main__':
    lottery = Lottery()
    asyncio.run(lottery.run())
