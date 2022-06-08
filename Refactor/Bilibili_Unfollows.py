from Bilibili_Daily import *
import requests


class Unfollows(DailyMethod):
    def __init__(self):
        super().__init__()
        self.Number = self.fetch_num()

    def check_group(self):
        try:
            response = requests.get(self.url9, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 0:
                    for i in range(len(data['data'])):
                        if data['data'][i]['name'] == '天选时刻':
                            return data['data'][i]['tagid']
                        else:
                            pass
                else:
                    self.logger.error('获取粉丝分组失败，状态码%s' % data['code'])
                    return False
            else:
                self.logger.error("error: %s" % response.status_code)
                return False
        except Exception as e:
            self.logger.error("error: %s" % e)

    def collect_mid(self, tagid):
        mids = []
        url = self.url10 + '?tagid=%s' % tagid
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 0:
                    for i in range(len(data['data'])):
                        mids.append(data['data'][i]['mid'])
                    return mids
                else:
                    self.logger.error('获取粉丝分组失败，状态码%s' % data['code'])
                    return False
            else:
                self.logger.error("error: %s" % response.status_code)
                return False
        except Exception as e:
            self.logger.error("error: %s" % e)

    def unfollow(self, num, mid, csrf):
        if len(mid) == 0 or num == 0:
            self.logger.error('没有可取关的up主')
        elif len(mid) < num:
            for i in range(len(mid)):
                data = {'fid': mid[i], 'act': 2, 're_src': 11, 'csrf': csrf}
                self.post_request(mid[i], data)
                time.sleep(1)
        else:
            for i in range(num):
                data = {'fid': mid[i], 'act': 2, 're_src': 11, 'csrf': csrf}
                self.post_request(mid[i], data)
                time.sleep(1)

    def post_request(self, mid, data):
        try:
            response = requests.post(self.url1, headers=self.headers, data=data)
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 0:
                    self.logger.info('%s取关成功' % mid)
                else:
                    self.logger.error('%s取关失败，状态码%s' % (mid, data))
            else:
                self.logger.error("error: %s" % response.status_code)
        except Exception as e:
            self.logger.error("error: %s" % e)

    def run(self):
        self.logger.info('本脚本依赖于Bilibili_Daily.py，确保文件在同一目录下')
        self.logger.info('脚本为取关天选时刻分组的up主')
        self.logger.info("💕💕💕💕💕💕💕💕💕💕💕💕💕💕💕💕💕💕💕💕💕💕")
        for i in range(len(self.cookies)):
            self.headers['cookie'] = self.cookies[i]
            data = self.get_requests(self.url)
            self.cope_info(data)
            tagid = self.check_group()
            if tagid is not None:
                mids = self.collect_mid(tagid)
                self.unfollow(self.Number[i], mids, self.csrfs[i])
            else:
                print('没有天选时刻分组')
                continue
        self.logger.info("=============》结束《============")


if __name__ == '__main__':
    Unfollow = Unfollows()
    Unfollow.run()
