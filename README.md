# Bilibili_Python  
### 目前代码重构了下，代码量缩减40%，目前代码还没重构完，写完弄个docker切换到分支就可以看新版了，不玩青龙了
## 想加入代理结果发现我没有代理。。。写出来也没办法测试。晚点更新
## 仅供个人学习，不得利用该仓库代码牟利，仅供学习参考  感兴趣可以给我点个 star 可以关注我B站 猫三骂骂咧咧的说
有建议的功能可以告诉我我尽量加上
新手，不喜勿喷，不喜欢用觉得垃圾可以不用，不用骂我垃圾，写的垃圾是学艺不精ok

## 配置文件详细的视频设置教程 http://b23.tv/cAyjDng  有能力就投两个币吧，我没多少硬币了
### ql repo https://github.com/wangquanfugui233/Bilibili_Python.git "Bilibili_" "Dev_"
    ql repo https://ghproxy.com/https://github.com/wangquanfugui233/Bilibili_Python.git "Bilibili_" "Dev_"  (带代理)
## 使用方法：
拉库完毕后，请跑一次Bilibili_cofig.py ，会自动生成json文件，把cookie填在对应位置就行了，修改投币数量为coin:1或者2，如图：

![image](https://user-images.githubusercontent.com/63834404/177083087-42d2cd19-d519-45d7-99ef-acc0eb6fa7a4.png)

扫描天选页数：max_page

扫描线程数：max_thread

黑名单：black_list  就是你不想关注的up主mid放在这里，一定要是英文逗号

白名单：white_list 就是你不想取关的，和中奖的up主mid会存在这里，一定要是英文逗号

多账号格式：---》：{"Cookie": ""},{"Cookie": ""},{"Cookie": ""}.....  一定要是英文逗号

代理格式:"proxy": ["183.236.232.160:8080","ip:端口",....]

添加完之后《再跑一次Bilibili_cofig.py》即可

## 不用拉配置文件了，运行config.py就会生成配置文件的了，把cookie填进去就好了
## 1.30 dev部分加入代理，取关作者（币够了🤣）
## 8.7 stable更新了可不投币选项，coin设置为0即可，帐号失效自动跳过该帐号任务

一天不要跑超过4次，不然你每天都得重新登录，我是用爱发电的，不欠你们什么，大会员的任务我写不了（没会员）

# 7.20 dev更新，加入漫画签到，关注我（为了0.1硬币不喜勿用勿喷）
我想吐槽好多啊但是算了。哎一言难尽

6.29 加入了天选中奖推送，推荐时间运行比天选晚半小时，推荐stable的版本

最近发现daily确实难用各位有什么推荐的建议可以说说，可以改改

6.25 dev新版本，有黑白名单功能 拉库 ql repo https://hub.fastgit.xyz/wangquanfugui233/Bilibili_Python.git "Dev_Bilibili_"

其他再改了再改了

api来源：bilibili-API-collect   和  bilibili.com
