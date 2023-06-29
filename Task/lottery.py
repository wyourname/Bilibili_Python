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

    async def check_group(self, csrf):
        try:
            group = await self.requests_method(self.url9, 'get')
            tag_id = next((i['tagid'] for i in group['data'] if i['name'] == '天选时刻'), None)
            if tag_id is not None:
                self.logger.info(f'{"@" * 5}存在天选时刻分组{"@" * 5}')
                # 分区
                await self.scan_all_partition()
            else:
                self.logger.info('不存在分组,开始创建')
                tag_id = self.create_group(csrf)
        except Exception as e:
            self.logger.info(e)
            os.kill(os.getpid(), signal.SIGKILL)

    async def scan_all_partition(self):
        all_partitions = await self.requests_method(self.url7, 'get')
        if all_partitions['code'] == 0:
            for subpartitions in all_partitions['data']:
                self.logger.info("开始扫描分区: " + subpartitions['name'])
                for small_partition in subpartitions['list']:
                    await self.scan_small_partitions(subpartitions['id'], small_partition['id'])

    async def scan_small_partitions(self, parent_id, partition_id):    # 扫描小分区多少页
        for i in range(1, 2):
            live_page = self.url_all % (parent_id, partition_id, i)
            msg = await self.requests_method(live_page, 'get')
            if msg['code'] == 0 and msg['data']['list'] is not None:  # 如果是该分区最后一页则break掉，不是就循环到最设定页数
                print(msg['data']['list'])
            else:
                break
            if msg['code'] == -412:
                self.logger.info("检测到被拦截,结束程序，一小时后再试")
                os.kill(os.getpid(), signal.SIGKILL)
                os._exit(0)

    async def create_group(self, csrf):
        data = {'tag': '天选时刻', 'csrf': csrf}
        message = await self.requests_method(self.create_url, 'post', data=data)
        if message['code'] == 200:
            self.logger.info('创建天选时刻分组成功')
            return message['data']['tagid']
        else:
            return 0

    async def run(self):
        cfg = await self.start()
        self.headers['referer'] = "https://live.bilibili.com/"
        for key, value in cfg.items():
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
