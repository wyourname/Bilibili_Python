import asyncio
import random
import time

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

    async def run(self):
        cfg_data = await self.start()
        self.headers["Referer"] = "https://www.bilibili.com/"
        for key, value in cfg_data.items():
            self.headers['Cookie'] = value['cookie']
            self.headers['User-Agent'] = random.choice(self.ua_list)
            csrf = {cookie_str.split("=")[0].strip(): cookie_str.split("=")[1].strip() for cookie_str in
                    value['cookie'].split(";")}.get("bili_jct", "")
            if await self.verification_cookie(self.url):
                await self.clockin_task()
                await self.live_task()
                if value['coin'] == 0:
                    self.logger.info("你设置了不投币，跳过")
                    continue
                else:
                    if not value['DesignateUp']:
                        await self.random_drop_task()
                        await self.drop_action(value['coin'], csrf, 3)
                    else:
                        await self.designate_uid_drop_task(value['DesignateUp'])
                        await self.drop_action(value['coin'], csrf, 3)
            else:
                self.logger.info(f"{key}cookie失效啦")
                continue


if __name__ == '__main__':
    dt = dailytask()
    asyncio.run(dt.run())
