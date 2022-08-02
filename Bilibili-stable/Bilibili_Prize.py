"""
new Env("哔哩哔哩-天选中奖通知")
cron 1 23 * * *

"""
from Bilibili_User import *
from notify import send
import datetime


class prize(Basic):
    def __init__(self):
        super().__init__()
        self.msg = '详细信息:\n'

    def get_prize(self):
        data = self.get_requests(self.prize)
        if data['code'] == 0:
            self.cope_prize(data['data']['list'])
        else:
            self.logger.info(data)

    def cope_prize(self, data):
        dt = time.strftime("%Y-%m-%d ", time.localtime())
        for i in data:
            date_time = datetime.datetime.strptime(i['end_time'], '%Y-%m-%d %H:%M:%S')
            if date_time.strftime('%Y-%m-%d ') == dt:
                self.logger.info('恭喜你中奖，奖品是：%s --- 兑奖up主是：%s' % (i['award_name'], i['anchor_name']))
                self.logger.info('中将时间是：%s' % i['end_time'])
                self.msg += '\n 中将时间：【%s】 今天的天选中奖，奖品是：%s --- 兑奖up主是：%s' % (
                    i['end_time'], i['award_name'], i['anchor_name'])
                self.logger.info("检查白名单")
                self.check_white_list(i['anchor_uid'])
            else:
                pass

    def check_white_list(self, uid):
        num = 0
        with open('./Bilibili_config.json', 'r') as f:
            data = json.load(f)
            if data['white_list']:
                for i in data['white_list']:
                    if i == uid:
                        self.logger.info('已存在于白名单')
                        num += 1
                        break  # 如果存在于白名单，则跳出循环
            else:
                self.logger.info('白名单为空')
                self.update_white_list(data, uid)
        if num == 0:
            self.update_white_list(data, uid)

    @staticmethod
    def update_white_list(data, uid):
        data['white_list'].append(uid)
        with open('./Bilibili_config.json', 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print('加入白名单成功')

    def ql_send(self):
        send("Bilibili天选通知", self.msg)

    def run(self):
        cookies = self.fetch_cookies()
        for i in cookies:
            self.headers['Cookie'] = i
            user = self.get_requests(self.url)
            self.msg += " %s：" % user['data']['uname']
            self.cope_info(user)
            self.get_prize()
        try:
            self.ql_send()
        except Exception as e:
            self.logger.info('推送失败')
            print(e)


if __name__ == '__main__':
    prize = prize()
    prize.run()
