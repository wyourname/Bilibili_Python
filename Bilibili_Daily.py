from Bilibili_Method import *


class CopeMethod(DailyMethod):
    def __init__(self):
        super().__init__()
        self.url_re = self.url5 + "?bvid="

    def cope_user(self, data):
        if data['code'] == 0:
            self.logger.info("**********" + data['data']['uname'] + "**********")
            self.logger.info("当前经验值：" + str(data['data']['level_info']['current_exp']))
            level_day = (data['data']['level_info']['next_exp'] - data['data']['level_info']['current_exp']) / 65
            self.logger.info('当前硬币数：' + str(data['data']['money']) + "，剩余升级天数" + str(int(level_day)))
        elif data['code'] == -101:
            self.logger.info(data['message'] + "请检查cookie")
        elif data['code'] == -111:
            self.logger.info(data['message'] + "请检查csrf")
        else:
            self.logger.info(data['message'])

    def cope_dynamic(self, data):
        title = []
        bv = []
        if data['code'] == 0:
            for i in range(len(data['data']['items'])):
                if data['data']['items'][i]['basic']['comment_type'] == 1:
                    if data['data']['items'][i]['modules']['module_dynamic']['major']['type'] == 'MAJOR_TYPE_ARCHIVE':
                        title.append(data['data']['items'][i]['modules']['module_dynamic']['major']['archive']['title'])
                        bv.append(data['data']['items'][i]['modules']['module_dynamic']['major']['archive']['bvid'])
                else:
                    pass
            return title, bv
        elif data['code'] == -101:
            self.logger.info(data['message'] + "请检查cookie")
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

    def run(self):
        for i in range(len(self.cookie)):
            self.headers['Cookie'] = self.cookie[i]
            # user = self.get_requests(self.url)
            # self.cope_user(user)
            dynamic = self.get_requests(self.url2)
            title, bv = self.cope_dynamic(dynamic)


if __name__ == '__main__':
    cope = CopeMethod()
    cope.run()
