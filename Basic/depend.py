"""
author:wangquanfugui233

"""
import os 
import sys
import asyncio
import aiohttp
import json
pythonpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(pythonpath)
from Basic.config import Config

class necessary(Config):
    def __init__(self):
        super().__init__()

    async def requests_method(self, url, method, data=None, p=None,other=None):
        max_retries = 3
        retries = 0
        while retries < max_retries:
            try:
                connector = aiohttp.TCPConnector(ssl=False)
                async with aiohttp.ClientSession(connector=connector) as session:
                    if method == 'get':
                        async with session.get(url, params=data, headers=self.headers, proxy=p) as response:
                            if response.status == 200:
                                if other == 'headers':
                                    content = dict(response.headers)
                                    return content
                                else:
                                    content = await response.text()
                                    return json.loads(content)
                            else:
                                content = await response.text()
                                return json.loads(content)
                    if method == 'post':
                        async with session.post(url, data=data, headers=self.headers, proxy=p) as response:
                            if response.status == 200:
                                if other == 'headers':
                                    header = response.headers.getall("Set-Cookie")
                                    content = await response.text()
                                    return header, json.loads(content)
                                else:
                                    content = await response.text()
                                    return json.loads(content)
                            else:
                                content = await response.text()
                                return json.loads(content)
            except Exception as e:
                self.logger.error(f'请求失败：{e}')
                retries += 1
                print(f'Request failed. Retrying ({retries}/{max_retries})...')
        if retries == max_retries:
            print('Max retries exceeded. Unable to establish connection.')

    async def verification_cookie(self, url, method='get'):
        data = await self.requests_method(url=url, method=method)
        if data['code'] == 0:
            msg = data['data']
            if msg['level_info']['current_level'] == 6:
                self.logger.info(f'{msg["uname"]}-》 你已经是lv6了,无需设置投币了《-')
            else:
                day = (data['data']['level_info']['next_exp'] - data['data']['level_info']['current_exp']) / 65
                self.logger.info(
                    f"{msg['uname']}当前等级: {msg['level_info']['current_level']}，银币：{msg['money']},乐观情况下约{day}天升级")
            return True
        elif data['code'] == -101:
            self.logger.info(data['message'] + "请检查cookie")
            return False
        else:
            self.logger.info(data['message'])
            return False

    async def send_pushplus_message(self, token: str, title, message: str):
        url = f"http://www.pushplus.plus/send?token={token}&title={title}&content={message}&template=html"
        data = await self.requests_method(url=url, method="get")
        if data['code'] == 200:
            self.logger.info("Sent push plus message successfully")
        else:
            self.logger.error("occurred an error when sending push plus message")

    async def userinfo(self):
        parameter = await self.start()
        for k1, v1 in parameter.items():
            self.headers['Cookie'] = v1['cookie']
            # print(self.headers)
            await self.verification_cookie(self.url)
            #你好


"""
"""


if __name__ == '__main__':
    nec = necessary()
    asyncio.run(nec.userinfo())
