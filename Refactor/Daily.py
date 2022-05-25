import random
from Method import *


class Daily(User):
    def __init__(self):
        super().__init__()

    def receive_message(self, data_get):  # 接受get_requests返回的数据,并筛选处理
        if data_get['code'] == 0:
            self.logger.info('获取用户信息成功，每天登录经验+5,一天只能加一次 ☆*: .｡. o(≧▽≦)o .｡.:*☆')
            self.logger.info(
                data_get['data']['uname'] + " 当前等级为：" + str(data_get['data']['level_info']['current_level']))
            self.logger.info(
                data_get['data']['uname'] + " 当前经验值为：" + str(data_get['data']['level_info']['current_exp']))
            self.logger.info(data_get['data']['uname'] + " 当前硬币数为：" + str(data_get['data']['money']))
        elif data_get['code'] == -101:
            self.logger.info(data_get['message'] + "请检查cookie")
        elif data_get['code'] == -111:
            self.logger.info(data_get['message'] + "请检查csrf")
        else:
            self.logger.info(data_get['message'])

    def cope_dynamic(self, dynamic):  # 接收动态数据，筛选视频bv和title
        title = []
        bv = []
        if dynamic['code'] == 0:
            for i in range(len(dynamic['data']['items'])):
                if dynamic['data']['items'][i]['basic']['comment_type'] == 1:
                    title.append(dynamic['data']['items'][i]['modules']['module_dynamic']['major']['archive']['title'])
                    bv.append(dynamic['data']['items'][i]['modules']['module_dynamic']['major']['archive']['bvid'])
            return title, bv
        elif dynamic['code'] == -101:
            self.logger.info(dynamic['message'] + "请检查cookie")
        else:
            self.logger.info(dynamic['message'])

    def check_bv_num(self, title, bv, csrf):  # 检查视频数量
        final_bv = list(set(bv))
        final_title = list(set(title))
        for i in range(len(final_bv)):
            self.drop_coin(final_bv[i], csrf)  # 打赏视频
            self.logger.info("视频标题：" + final_title[i] + "，视频bv：" + final_bv[i])
            if i == 4:
                self.logger.info("视频数量到5,到此结束")
                break
            time.sleep(random.randint(3, 5))

    def run_daily(self):
        for i in range(len(self.a)):
            self.headers['Cookie'] = self.a[i]  # 获取cookies设置到headers中
            # data = self.get_requests(self.url)                                                # 获取用户信息,返回数据
            # self.receive_message(data)                                                        # 接收用户信息，处理数据
            dynamic = self.consult_dynamic(self.url2)  # 获取动态信息
            title, bv = self.cope_dynamic(dynamic)  # 处理动态信息
            self.check_bv_num(title, bv, self.csrf[i])  # 检查bv数量
            self.logger.info("==================")
            if i == len(self.a) - 1:
                break
            time.sleep(5)


if __name__ == '__main__':
    daily = Daily()
    daily.run_daily()
