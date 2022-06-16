from Bilibili_Daily import *


class Unfollows(Basic):
    def __init__(self):
        super().__init__()

    def check_group(self, csrf):
        self.logger.info('检查是否有天选时刻分组')
        group = self.get_requests(self.url9)
        self.cope_group(group, csrf)

    def cope_group(self, group, csrf):
        for i in group['data']:
            if i['name'] == '天选时刻':
                self.logger.info('有天选时刻分组，开始检查关注人数')
                if i['count'] > 0:
                    self.logger.info('天选时刻分组关注人数: %s ***>开始执行取关任务' % i['count'])
                    self.fetch_mid(i['tagid'], i['count'], csrf)
                else:
                    self.logger.info('天选时刻分组关注人数: %s ***>无需取关' % i['count'])
                break
        else:
            self.logger.info('没有天选时刻分组，结束检查')
            return None

    def fetch_mid(self, group_id, count, csrf):
        url = self.url10 + '?tagid=%s' % group_id
        if count <= 50:
            group_info = self.get_requests(url)
            userid, uname = self.cope_User(group_info)
            self.cyc_unfollow(userid, uname, csrf)
        else:
            for i in range(int(count / 50) + 1):
                group_info = self.get_requests(url)
                userid, uname = self.cope_User(group_info)
                self.cyc_unfollow(userid, uname, csrf)

    @staticmethod
    def cope_User(group_info):
        mid = []
        uname = []
        for i in group_info['data']:
            mid.append(i['mid'])
            uname.append(i['uname'])
        return mid, uname

    def cyc_unfollow(self, mid, uname, csrf):
        for i in range(len(mid)):
            self.unfollow(mid[i], csrf)
            self.logger.info('取关: %s' % uname[i])

    def unfollow(self, mid, csrf):
        data = {'fid': mid, 'act': 2, 're_src': 11, 'csrf': csrf}
        unfollow = self.post_requests(self.url1, data)
        self.unfollow_info(unfollow)

    def unfollow_info(self, unfollow):
        if unfollow['code'] == 0:
            self.logger.info('取关成功')
        else:
            self.logger.info('取关失败')

    def run(self):
        self.logger.info('本脚本依赖于Bilibili_User.py，确保文件在同一目录下')
        self.logger.info('脚本为取关天选时刻分组的up主')
        self.logger.info("*" * 5 + "开始取关" + "*" * 5)
        for i in range(len(self.cookies)):
            self.headers['cookie'] = self.cookies[i]
            self.check_group(self.csrfs[i])
        self.logger.info("=============》结束《============")


if __name__ == '__main__':
    Unfollow = Unfollows()
    Unfollow.run()
