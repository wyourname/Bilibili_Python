"""
new Env("哔哩哔哩-【日常】")
cron : 5 1 * * *
"""
from Bilibili_User import *


class Daily(Basic):
    def __init__(self):
        super().__init__()
        self.specify = self.fetch_favorite()

    def check_group(self):
        follows = self.get_requests(self.url9)
        if follows['code'] == 0:
            for i in follows['data']:
                if i['tagid'] == 0:
                    return i['count']
        else:
            return None

    def uid_info(self, coin, csrf):
        count = self.check_group()
        if count == 0:
            self.logger.info("默认分组为空")
        elif 55 >= count > 0:
            url = self.url10 + '?tagid=0'
            self.fetch_uid(url, coin, csrf)
        else:
            page = random.randint(1, int(count / 50) + 1)
            url = self.url10 + '?tagid=0&pn=%s' % page
            self.fetch_uid(url, coin, csrf)

    def fetch_uid(self, url, coin, csrf):
        if len(self.specify) > 0:
            num = 0
            while True:
                mid = random.choice(self.specify)
                self.logger.info("你选择了指定用户投币，uid：%s" % mid)
                bvid_list, video_title = self.cyc_search_uid(mid)
                if bvid_list:
                    if self.cope_video(bvid_list, video_title, coin, csrf):
                        num += 1
                    else:
                        pass
                else:
                    if len(self.specify) == 1:
                        break
                if num == 5:
                    break
            if num < 5:
                self.logger.info("指定up没有可投币的视频，随机投币")
                self.cycle_uid(url, coin, csrf)
        else:
            self.cycle_uid(url, coin, csrf)

    def other_task(self, csrf):
        url = self.url10 + '?tagid=0'
        group_info = self.get_requests(url)
        mid_list, uname_list = self.list_uid(group_info['data'])
        mid = random.choice(mid_list)
        self.logger.info("随机选择了用户：" + uname_list[mid_list.index(mid)])
        bvid_list, video_title = self.cyc_search_uid(mid)
        if bvid_list:
            video = random.choice(bvid_list)
            self.play_video(video, video_title[bvid_list.index(video)])
            self.share_dynamic(video_title[bvid_list.index(video)], video, csrf)
            return True
        else:
            return False

    def cycle_uid(self, url, coin, csrf):
        group_info = self.get_requests(url)
        mid_list, uname_list = self.list_uid(group_info['data'])
        num = 0
        while True:
            mid = random.choice(mid_list)
            self.logger.info("本次投币对象："+uname_list[mid_list.index(mid)])
            bvid_list, video_title = self.cyc_search_uid(mid)
            if bvid_list:
                if self.cope_video(bvid_list, video_title, coin, csrf):
                    num += 1
                else:
                    pass
            else:
                pass
            if num == 5:
                break

    def cope_video(self, bvid_list, video_title, coin, csrf):
        choice_video = []
        num = 0
        for i in range(len(bvid_list)):
            video = random.choice(bvid_list)
            self.logger.info("视频：%s" % video_title[bvid_list.index(video)])
            if self.c_v_d_i(video, coin, csrf) and video is not choice_video:
                num += 1
                break
            else:
                choice_video.append(video)
        if num == 1:
            return True
        else:
            return False

    @staticmethod
    def list_uid(data):
        mid_list = []
        uname_list = []
        for i in data:
            mid_list.append(i['mid'])
            uname_list.append(i['uname'])
        return mid_list, uname_list

    def search_uid(self, mid):
        url = self.url11 % mid
        video_num = self.get_requests(url)
        if video_num['code'] == 0:
            return video_num['data']['page']['count']
        else:
            return None

    def cyc_search_uid(self, mid):
        num = self.search_uid(mid)
        if num > 50:
            page = random.randint(1, int(num / 50) + 1)
            bvid_list, video_title = self.bvid_page(mid, page)
            return bvid_list, video_title
        elif 0 < num <= 50:
            bvid_list, video_title = self.bvid_page(mid, 1)
            return bvid_list, video_title
        else:
            return None, None

    def bvid_page(self, mid, page):
        url = self.url11 % mid + "&ps=50&pn=%s" % page
        bvid_data = self.get_requests(url)
        if bvid_data['code'] == 0:
            bvid_list, video_title = self.bvid_list(bvid_data['data']['list']['vlist'])
            return bvid_list, video_title
        else:
            self.logger.error(bvid_data)

    @staticmethod
    def bvid_list(data):
        bvid_list = []
        video_title = []
        for i in data:
            bvid_list.append(i['bvid'])
            video_title.append(i['title'])
        return bvid_list, video_title

    def c_v_d_i(self, bvid, coin, csrf):
        url = "https://api.bilibili.com/x/web-interface/archive/coins?bvid=%s" % bvid
        data = self.get_requests(url)
        if data['code'] == 0:
            if data['data']['multiply'] == 0:
                self.drop_coin(bvid, coin, csrf)
                return True
            else:
                self.logger.info("该视频已经投币过，不再投币")
                return False
        else:
            self.logger.error('检查投币情况失败，错误码：%s' % data['code'])
            return False

    def recommend_video(self, bvid):
        url = self.url5 + "?bvid=" + bvid
        data = self.get_requests(url)
        if data['code'] == 0:
            return self.cope_recommend(data['data'])
        else:
            self.logger.error(data['message'])

    @staticmethod
    def cope_recommend(data):
        title = []
        bv = []
        for i in data:
            title.append(i['title'])
            bv.append(i['bvid'])
        return title, bv

    def drop_coin(self, bv, coin, csrf):
        data = {
            'bvid': bv,
            'multiply': coin,
            'csrf': csrf
        }
        drop = self.post_requests(self.url3, data)
        if drop['code'] == 0:
            self.logger.info("【投币成功】")
        else:
            self.logger.error(drop['message'])

    def sign_live(self):
        self.logger.info('开始直播签到')
        sign = self.get_requests(self.url8)
        if sign['code'] == 0:
            self.logger.info('【直播签到成功】')
        else:
            self.logger.info(sign['message'])

    def share_dynamic(self, title, bv, csrf):
        data = {
            "bvid": bv,
            "csrf": csrf
        }
        self.logger.info('开始分享动态，标题%s' % title)
        share = self.post_requests(self.url4, data)
        if share['code'] == 0:
            self.logger.info('【分享动态成功】')
        else:
            self.logger.info(share['message'])

    def play_video(self, bv, title):
        data = {
            "bvid": bv,
            "play_time": random.randint(30, 45),
            "realtime": random.randint(30, 45)
        }
        self.logger.info('开始播放视频，标题%s' % title)
        play = self.post_requests(self.url6, data)
        if play['code'] == 0:
            self.logger.info('【播放视频成功】')
        else:
            self.logger.info(play['message'])

    def clockin(self):
        data = {'platform': 'android'}
        clock_info = self.post_requests(self.clockin_url, data)
        if clock_info['code'] == 0:
            self.logger.info("漫画签到成功")
        else:
            self.logger.info(clock_info['msg'])

    def run(self):
        self.manual()
        self.logger.info('目的是随机给我回点硬币，是随机')
        self.logger.info('本次更新支持不投币，coin设置为0即可')
        cookies = self.fetch_cookies()
        coins = self.fetch_drop_coin()
        csrfs = self.fetch_csrf(cookies)
        for i in cookies:
            self.headers['Cookie'] = i
            self.headers['user-agent'] = random.choice(self.ua_list)
            self.headers['Referer'] = 'https://www.bilibili.com/'
            user_info = self.get_requests(self.url)
            if self.cope_info(user_info):
                self.logger.info('--》帐号有效《--')
            else:
                self.logger.info('--》帐号无效,跳出该帐号《--')
                continue
            self.mao_san(csrfs[cookies.index(i)])
            self.clockin()
            self.sign_live()
            if self.other_task(csrfs[cookies.index(i)]):
                pass
            else:
                self.other_task(csrfs[cookies.index(i)])
            if coins[cookies.index(i)] == 0:
                self.logger.info('设置了不投币，跳过投币任务')
                continue
            else:
                self.uid_info(coins[cookies.index(i)], csrfs[cookies.index(i)])
        self.logger.info("= "*8+"任务完成"+"= "*8)


if __name__ == '__main__':
    Daily = Daily()
    Daily.run()
