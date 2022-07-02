from Dev_Bilibili_Daily import *


class Unfollows(Basic):
    def __init__(self):
        super().__init__()
        self.white_list = self.fetch_white_list()

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

    def screen_white_list(self, userid):
        if self.white_list is None:
            return False
        if userid in self.white_list:
            return True
        else:
            return False

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
            if self.screen_white_list(mid[i]):
                self.logger.info('【%s】在白名单中，跳过' % uname[i])
                continue
            else:
                self.unfollow(mid[i], csrf)
                self.logger.info('取关: 【%s】' % uname[i])

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
        self.logger.info('脚本支持白名单，可以在Bilibili_config.json设置不取关的用户ID')
        self.logger.info('白名单格式: [uid1, uid2, uid3, ...] uid为数字，逗号为英文逗号')
        self.logger.info('脚本作者为github@wangquanfugui233')
        self.logger.info("*" * 6 + "开始取关" + "*" * 6)
        for i in range(len(self.cookies)):
            self.headers['cookie'] = self.cookies[i]
            self.check_group(self.csrfs[i])
        self.logger.info("=============》结束《============")


if __name__ == '__main__':
    Unfollow = Unfollows()
    Unfollow.run()
