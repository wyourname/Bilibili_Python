import asyncio
import random
import time
import os
import sys
import urllib.parse
import re
pythonpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(pythonpath)
from Basic.depend import necessary


class dailytask(necessary):
    def __init__(self):
        super().__init__()
        self.drop_up_list = []
        self.drop_uname_list = []
        self.drop_video_list = []
        self.drop_title_list = []

    async def random_drop_task(self):  # 随机找个人投币的任务
        url = self.url10 + '?tagid=0'
        group_info = await self.requests_method(url, "get")
        if group_info['code'] == 0:
            self.drop_up_list = [i['mid'] for i in group_info['data']]
            self.drop_uname_list = [i['uname'] for i in group_info['data']]
            # print(self.drop_up_list)
            await self.designate_uid_drop_task(self.drop_up_list)
        else:
            self.logger.error("随机找个人投币任务失败")

    async def designate_uid_drop_task(self, uid_list):  # 设定uid的投币任务
        if len(uid_list) < 5:
            for uid in uid_list:  # 循环uidlist
                await self.get_up_video(uid)  # 只获取一个up的视频投币
            if len(self.drop_video_list) < 5:
                bv = random.choice(self.drop_video_list)  # 随机找一个推荐视频从里挑剩余的
                title, bvid = await self.video_for_recommend(bv)
                await self.cycle_data(bvid, title)
        else:
            for uid in uid_list:  # 写到累了
                await self.get_up_video(uid)  # 只获取一个up的视频
                if len(self.drop_video_list) == 5:
                    break
            if len(self.drop_video_list) < 5:
                bv = random.choice(self.drop_video_list)  # 随机找一个推荐视频从里挑剩余的
                title, bvid = await self.video_for_recommend(bv)
                await self.cycle_data(bvid, title)

    async def cycle_data(self, bvid_list, title_list):
        while True:
            if len(self.drop_video_list) == 5:
                break
            bv = random.choice(bvid_list)
            if await self.check_bvid(bv) and bv not in self.drop_video_list:
                self.drop_video_list.append(bv)
                self.drop_title_list.append(title_list[bvid_list.index(bv)])

    async def get_up_video(self, mid):
        url = self.url11 + str(mid) + "&ps=50"
        bv_info = await self.requests_method(url, method="get")
        if bv_info['code'] == 0:
            bvid_list = [i['bvid'] for i in bv_info['data']['list']['vlist']]
            video_title = [i['title'] for i in bv_info['data']['list']['vlist']]
            if len(bvid_list) > 0:
                bv = random.choice(bvid_list)
                if await self.check_bvid(bv):
                    self.drop_video_list.append(bv)
                    self.drop_title_list.append(video_title[bvid_list.index(bv)])
            else:
                self.logger.info("bvid is empty")
        else:
            self.logger.error(f'request error {bv_info["code"]}')

    async def check_bvid(self, bvid):
        url = "https://api.bilibili.com/x/web-interface/archive/coins?bvid=%s" % bvid
        data = await self.requests_method(url, method="get")
        if data['code'] == 0:
            if data['data']['multiply'] == 0:
                return True
            else:
                return False
        else:
            self.logger.error('检查投币情况失败，错误码：%s' % data['code'])
            return False

    async def video_for_recommend(self, bvid):  # 防止up视频太少投币次数不够5次
        url = self.url5 + '?bvid=' + bvid
        rec = await self.requests_method(url, method="get")
        if rec['code'] == 0:
            title = [i['title'] for i in rec['data']]
            bv = [i['bvid'] for i in rec['data']]
            return title, bv
        else:
            self.logger.error(rec['message'])

    async def drop_action(self, coin, csrf, delay):
        for bv in self.drop_video_list:
            self.logger.info(f"即将消耗{coin}硬币于{self.drop_title_list[self.drop_video_list.index(bv)]}")
            time.sleep(delay)
            data = {
                'bvid': bv,
                'multiply': coin,
                'csrf': csrf
            }
            drop = await self.requests_method(self.url3, method="post", data=data)
            if drop['code'] == 0:
                self.logger.info(f"drop success for {bv}")
            else:
                self.logger.info(f"drop failed for {bv},message is {drop['message']}")

    async def clockin_task(self):
        data = {'platform': 'android'}
        clock_info = await self.requests_method(self.clockin_url, method="post", data=data)
        if clock_info['code'] == 0:
            self.logger.info("漫画签到成功")
        else:
            self.logger.info(clock_info['msg'])

    async def live_task(self):
        live_sign = await self.requests_method(self.url8, method="get")
        if live_sign['code'] == 0:
            self.logger.info("直播签到成功")
        else:
            self.logger.info(live_sign['message'])

    async def receive_b_money(self, csrf):
        receive = "https://api.bilibili.com/x/vip/privilege/receive"
        vip_info = await self.requests_method(self.vip_url, "get")
        if vip_info['code'] == 0:
            for status in vip_info['data']['list']:
                if status['vip_type'] == 2 and status['state'] == 0:
                    data = {
                        "type": status['type'],
                        "csrf": csrf
                    }
                    result = await self.requests_method(receive, method='post', data=data)
                    if result['code'] == 0:
                        self.logger.info("年度大会员B币等优惠领取成功")
                    else:
                        self.logger.error(f"错误代码{result['code']} 如：-400：请求错误 69800：网络繁忙 请稍后再试 69801：你已领取过该权益")
                else:
                    break

    async def run(self):
        cfg_data = await self.start()
        self.headers["Referer"] = "https://www.bilibili.com/"
        for key, value in cfg_data.items():
            # if value['pushplus_token'] is None:
            #     self.logger.info(f"{key}有pushplus_token为空，跟不上")
            # else:
            #     await self.send_pushplus_message(token=value['pushplus_token'], title='test', message="test")
            self.headers['Cookie'] = value['cookie']
            self.headers['User-Agent'] = random.choice(self.ua_list)
            csrf_match = re.search(r"bili_jct=([^;]+)", value['cookie'])
            if csrf_match:
                csrf = csrf_match.group(1)
                # print(csrf)
            if await self.verification_cookie(self.url):
                await self.clockin_task()
                await self.receive_b_money(csrf)
                await self.live_task()
                # if value['coin'] == 0:
                #     self.logger.info("你设置了不投币，跳过")
                #     continue
                if not value['DesignateUp']:
                    await self.random_drop_task()
                    await self.drop_action(value['coin'], csrf, 3)  # 数字3代表延迟3秒
                else:
                    await self.designate_uid_drop_task(value['DesignateUp'])
                    await self.drop_action(value['coin'], csrf, 3)
            else:
                msg = f"{key}cookie失效啦"
                self.logger.info(msg)
                await self.send_pushplus_message(token=value['pushplus_token'], title='B站账号失效', message=msg)
                continue


if __name__ == '__main__':
    dt = dailytask()
    asyncio.run(dt.run())
