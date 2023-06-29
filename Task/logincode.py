import os
import sys
pythonpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(pythonpath)
from Basic.depend import necessary
from depend import necessary
import asyncio
import qrcode
import time


class login(necessary):
    def __init__(self):
        super().__init__()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
            "Referer": "https://passport.bilibili.com/login"
        }
        self.qrcode_url = "https://passport.bilibili.com/x/passport-login/web/qrcode/generate"
        self.scan_code_url = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll"

    async def get_login_code(self):
        qrcode_data = await self.requests_method(self.qrcode_url,'get')
        return qrcode_data['data']['url'], qrcode_data['data']['qrcode_key']

    async def generate_login_code(self):
        # 生成二维码
        url, qrcode_key = await self.get_login_code()
        # 生成url的二维码，在控制台输出
        qr = qrcode.QRCode(version=1, box_size=1, border=0)
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image()
        qr_img.save("qrcode.png")
        # 获取二维码数据矩阵
        matrix = qr.get_matrix()
        # 定义用于绘制二维码的字符集
        char_blocks = ["  ", "██"]
        # 打印二维码
        for row in matrix:
            line = "".join(char_blocks[pixel] for pixel in row)
            self.logger.info(line)

        return qrcode_key

    async def draw_url_params(self,url, refresh_token):
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        params_string = parsed_url.query
        cookie = params_string.replace("&","; ")
        await self.insert_data('cookie', cookie)
        await self.insert_data('refresh_token', refresh_token)
        print("Params String:", cookie)

    async def get_login_status(self):
        await self.start()
        qrcode_key = await self.generate_login_code()
        while True:
            data = await self.requests_method(f"{self.scan_code_url}?qrcode_key={qrcode_key}",'get')
            if data['data']['code'] == 0:
                self.logger.info("登录成功!")
                await self.draw_url_params(data['data']['url'], data['data']['refresh_token'])
                break
            elif data['data']['code'] == 86038:
                self.logger.info("二维码失效，退出")
                break
            elif data['data']['code'] == 86090:
                self.logger.info("给阿姨倒杯卡布奇诺，阿姨你快点啊")
            elif data['data']['code'] == 86101:
                self.logger.info("你有180秒的时间，请用B站客户端扫码登录确认，可以在输出日志查找二维码，脚本不要停止！")
            time.sleep(2)

       

if __name__ == '__main__':
    login = login()
    asyncio.run(login.get_login_status())
