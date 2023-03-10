"""
author:wangquanfugui233

"""
import asyncio
import sys
import aiohttp
from Basic.config import Config


class necessary(Config):
    def __init__(self):
        super().__init__()

    async def requests_method(self, url, method, data=None, p=None):
        try:
            async with aiohttp.ClientSession() as session:
                if method == 'get':
                    async with session.get(url, params=data, headers=self.headers, proxy=p) as response:
                        if response.status == 200:
                            return await response.json()
                        else:
                            return await response.json()
                if method == 'post':
                    async with session.post(url, data=data, headers=self.headers, proxy=p) as response:
                        if response.status == 200:
                            return await response.json()
                        else:
                            return await response.json()
        except Exception as e:
            self.logger.error(f'请求失败：{e}')

    async def verification_cookie(self, url, method='get'):
        data = await self.requests_method(url=url, method=method)
        if data['code'] == 0:
            msg = data['data']
            if msg['level_info']['current_level'] == 6:
                self.logger.info(f'{msg["uname"]}-》 你已经是lv6了,无需设置投币了《-')
            else:
                day = (data['data']['level_info']['next_exp'] - data['data']['level_info']['current_exp']) / 65
                self.logger.info(f"{msg['uname']}当前等级: {msg['level_info']['current_level']}，银币：{msg['money']},乐观情况下约{day}天升级")
            return True
        elif data['code'] == -101:
            self.logger.info(data['message'] + "请检查cookie")
            return False
        else:
            self.logger.info(data['message'])
            return False

    async def userinfo(self):
        parameter = await self.start()
        for k1, v1 in parameter.items():
            self.headers['Cookie'] = v1['cookie']
            # print(self.headers)
            await self.verification_cookie(self.url)


if __name__ == '__main__':
    nec = necessary()
    asyncio.run(nec.userinfo())
