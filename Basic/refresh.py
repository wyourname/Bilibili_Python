import random
import asyncio
import sys
import os
import re
import json
import http.cookies
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import binascii
import time
import requests
pythonpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(pythonpath)
from Basic.depend import necessary
import yaml

class Bilicookie(necessary):
    def __init__(self):
        super().__init__()

    # 检查csrf是否要刷新
    async def check_csrf(self, csrf):
        url = f"https://passport.bilibili.com/x/passport-login/web/cookie/info?csrf={csrf}"
        data = await self.requests_method(url, "get")
        # print(data)
        if data['data']['refresh'] is True:
            self.logger.info(f"csrf:{csrf} 需要刷新")
            return True
        else:
            self.logger.info(f"csrf:{csrf} 不需要刷新")
            return False



    async def get_refresh_csrf(self):
        ts = round(time.time() * 1000)
        key = RSA.importKey('''\
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDLgd2OAkcGVtoE3ThUREbio0Eg
Uc/prcajMKXvkCKFCWhJYJcLkcM2DKKcSeFpD/j6Boy538YXnR6VhcuUJOhH2x71
nzPjfdTcqMz7djHum0qSZA0AyCBDABUqCrfNgCiJ00Ra7GmRj+YCK1NJEuewlb40
JNrRuoEUXpabUzGB8QIDAQAB
-----END PUBLIC KEY-----''')
        cipher = PKCS1_OAEP.new(key, SHA256)
        encrypted = cipher.encrypt(f'refresh_{ts}'.encode())
        result = binascii.b2a_hex(encrypted).decode()
        get_refresh_token_url = f"https://www.bilibili.com/correspond/1/{result}"
        # print(self.headers)
        html = requests.get(get_refresh_token_url, headers=self.headers)
        # print(data.text)
        pattern = r'<div id="1-name">(.*?)</div>'
        match = re.search(pattern, html.text)
        if match:
            text = match.group(1)
            text = text.strip()
            # print(text)
            return text


    async def refresh_cookie(self,csrf,refresh_csrf,o_refresh_token):
        refresh_cookie_url = "https://passport.bilibili.com/x/passport-login/web/cookie/refresh"
        params = {
            "csrf": csrf,
            "refresh_csrf": refresh_csrf,
            "source": "main_web",
            "refresh_token": o_refresh_token
        }
        data, data_content = await self.requests_method(refresh_cookie_url, "post", data=params,other='headers')
        # print(data)
        # 创建一个字典来存储提取的值
        cookie_list = []
        n_csrf = None
        for set_cookie in data:
            cookies = http.cookies.SimpleCookie()
            cookies.load(set_cookie)
            if 'bili_jct' in cookies:
                n_csrf = cookies['bili_jct'].value
            cookie_str = "; ".join([f"{key}={cookie.value}" for key, cookie in cookies.items()])
            cookie_list.append(cookie_str)   
        cookie = "; ".join(cookie_list)
        n_refresh_token = data_content['data']['refresh_token']
        await self.insert_data('refresh_token',n_refresh_token)
        await self.insert_data('cookie',cookie)
        await self.confirm_refresh(csrf,o_refresh_token)

 
    async def confirm_refresh(self,o_csrf, o_refresh_token):
        confirm_refresh_url = "https://passport.bilibili.com/x/passport-login/web/confirm/refresh"
        post_data = {
            "csrf": o_csrf,
            "refresh_token": o_refresh_token
        }
        data = await self.requests_method(confirm_refresh_url, "post", data=post_data)
        if data['code'] == 0:
            self.logger.info("cookie刷新成功")
        else:
            self.logger.info(f"cookie刷新失败 error code:{data['code']}")


          


    
    async def start_refresh(self):
        cfg_data = await self.start()
        self.headers["Referer"] = "https://www.bilibili.com/"
        for key, value in cfg_data.items():
            # await self.send_pushplus_message(token=value['pushplus_token'], title='test', message="test")
            self.headers['Cookie'] = value['cookie']
            self.headers['User-Agent'] = random.choice(self.ua_list)
            csrf_match = re.search(r"bili_jct=([^;]+)", value['cookie'])
            if csrf_match:
                csrf = csrf_match.group(1)
            if await self.check_csrf(csrf):
                refresh_csrf=await self.get_refresh_csrf()
                await self.insert_data('refresh_csrf', refresh_csrf)
                self.logger.info(f"成功获得refresh_csrf:{refresh_csrf}")
                await self.refresh_cookie(csrf,refresh_csrf,value['refresh_token'])




if __name__ == "__main__":
    bilicookie = Bilicookie()
    asyncio.run(bilicookie.start_refresh())
