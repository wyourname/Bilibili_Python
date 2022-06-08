import time

from Bilibili_Method import *


class CopeMethod(DailyMethod):
    def __init__(self):
        super().__init__()

    def cope_dynamic(self, data):
        title = []
        bv = []
        if data['code'] == 0:
            for i in data['data']['items']:
                if i['basic']['comment_type'] == 1:
                    if i['modules']['module_dynamic']['major']['type'] == 'MAJOR_TYPE_ARCHIVE':
                        title.append(i['modules']['module_dynamic']['major']['archive']['title'])
                        bv.append(i['modules']['module_dynamic']['major']['archive']['bvid'])
                else:
                    pass
            return title, bv
        elif data['code'] == -101:
            self.logger.info(data['message'] + "请检查cookie")
        else:
            self.logger.info(data['message'])

    def check_bv_num(self, bv, title, num, csrf):
        if len(bv) == 0:
            self.logger.info('没有发现可投币视频，多关注几个人吧')
            return False
        elif 1 <= len(bv) < 5 and (num == 1 or num == 2):
            self.logger.info('可投币视频数量%s，开始投币,不足5个投币给推荐视频' % len(bv))
            a = random.randint(0, len(bv) - 1)
            self.logger.info('可投币视频数量%s，开始投币' % len(bv))
            for i in range(len(bv)):
                self.logger.info('开始投币，标题%s' % title[i])
                self.drop_coin(bv[i], num, csrf)
                time.sleep(1)
            url = self.url5 + "?bvid=" + bv[a]  # 动态视频下的推荐视频
            recommend = self.get_requests(url)
            re_title, re_bv = self.cope_recommend(recommend)
            for j in range(5 - len(bv)):
                self.logger.info('开始投币于推荐视频，标题%s' % re_title[j])
                self.drop_coin(re_bv[j], num, csrf)
                time.sleep(1)
            return True
        elif len(bv) >= 5 and (num == 1 or num == 2):
            for i in range(len(bv)):
                self.logger.info('开始投币，标题%s' % title[i])
                self.drop_coin(bv[i], num, csrf)
                if i == 4:
                    self.logger.info('投币数量到达5个，结束投币')
                    break
                time.sleep(1)
            return True
        else:
            self.logger.info('可投币视频数量%s，不投币' % len(bv))
            return False

    def drop_coin(self, bv, coin, csrf):
        data = {
            'bvid': bv,
            'multiply': coin,
            'csrf': csrf
        }
        drop = self.post_requests(self.url3, data)
        self.cope_drop_coin(drop)

    def cope_drop_coin(self, data):  # 接收打赏返回数据，处理数据
        if data['code'] == 0:
            self.logger.info("投币成功 ௹ ✓")
        elif data['code'] == -101:
            self.logger.info(data['message'] + "请检查cookie")
        elif data['code'] == -111:
            self.logger.info(data['message'] + "请检查csrf")
        elif data['code'] == -104:
            self.logger.info(data['message'] + "硬币不足")
        else:
            self.logger.info(data['message'])

    def cope_recommend(self, data):
        title = []
        bv = []
        if data['code'] == 0:
            for i in range(len(data['data'])):
                title.append(data['data'][i]['title'])
                bv.append(data['data'][i]['bvid'])
                if i == 4:
                    break
            return title, bv
        elif data['code'] == -101:
            self.logger.info(data['message'] + "请检查cookie")
        elif data['code'] == -111:
            self.logger.info(data['message'] + "请检查csrf")
        else:
            self.logger.info(data['message'])

    def share_dynamic(self, title, bv, csrf):
        data = {
            "bvid": bv,
            "csrf": csrf
        }
        self.logger.info('开始分享动态，标题%s' % title)
        share = self.post_requests(self.url4, data)
        self.cope_share_dynamic(share)

    def cope_share_dynamic(self, data):
        if data['code'] == 0:
            self.logger.info("分享成功 ௹ ✓")
        elif data['code'] == -101:
            self.logger.info(data['message'] + "请检查cookie")
        elif data['code'] == -111:
            self.logger.info(data['message'] + "请检查csrf")
        else:
            self.logger.info(data['message'])

    def play_video(self, bv, title):
        data = {
            "bvid": bv,
            "play_time": random.randint(30, 45),
            "realtime": random.randint(30, 45)
        }
        self.logger.info('开始播放视频，标题%s' % title)
        play = self.post_requests(self.url6, data)
        self.cope_play_video(play)

    def cope_play_video(self, data):
        if data['code'] == 0:
            self.logger.info("播放成功 ௹ ✓")
        else:
            self.logger.info(data['message'])

    def DoSign(self):
        self.logger.info('开始直播签到')
        sign = self.get_requests(self.url8)
        self.cope_sign(sign)

    def cope_sign(self, data):
        if data['code'] == 0:
            self.logger.info("签到成功 ௹ ✓")
        else:
            self.logger.info(data['message'])

    def decorate(self):
        self.logger.info("该脚本由GitHub@王权富贵233制作")
        self.logger.info("脚本依赖于requests，和Bilibili.Method.py")
        self.logger.info("每天自动任务65经验,可以自行设置投币数量,推荐cron 1 1 * * *")
        self.logger.info("✌️✌️✌️✌️✌️✌️✌️✌️✌️✌️✌️✌️✌️✌️✌️✌️✌️")

    def run(self):
        self.decorate()
        for i in range(len(self.cookies)):
            self.headers['Cookie'] = self.cookies[i]
            info = self.get_requests(self.url)
            self.cope_info(info)
            self.DoSign()
            dynamic = self.get_requests(self.url2)
            title, bv = self.cope_dynamic(dynamic)
            self.check_bv_num(bv, title, self.coin[i], self.csrfs[i])
            if len(bv) > 0:
                s_bv = random.randint(0, len(bv))
                self.share_dynamic(title[s_bv], bv[s_bv], self.csrfs[i])
                self.play_video(bv[s_bv], title[s_bv])
            else:
                self.logger.info('没有可分享的动态')
                self.logger.info('也没有可播放的视频')
            self.logger.info('第%s个帐号结束' % (i + 1))
        self.logger.info('😎😎😎😎😎😎😎😎😎😎😎全部结束😎😎😎😎😎😎😎😎😎😎😎')


if __name__ == '__main__':
    cope = CopeMethod()
    cope.run()
