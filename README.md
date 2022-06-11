# Bilibili_Python
## 仅供个人学习，不得利用该仓库代码牟利，仅供学习参考  感兴趣可以给我点个star
我为什么写这个呢,主要就是闲的，其次就是我手机刷的青龙2.12.2模块运行不了 RayWangQvQ/BiliBiliToolPro 所以就写这个，其次就是想练习一下爬虫
目前功能还没有完善，完善后会进行一次代码封装去除多余函数。
可以关注我B站 猫三骂骂咧咧的说
有建议的功能可以告诉我我尽量加上
新手，不喜勿喷，不喜欢用觉得垃圾可以不用，不用骂我垃圾，写的垃圾是学艺不精ok
会青龙拉库命令的可以告诉我我还不会配置😂

## 修复了 Expecting value: line 1 column 1 (char 0)，感谢帮我测试的人tg上的 @Koo Natsuki 耐心帮我测试一下午，真的感谢

## 不用拉配置文件了，运行config.py就会生成配置文件的了，把cookie填进去就好了

6.8 新配置，可自定义每个视频投币数量 1-2之间 ，每个py都可运行，user可查看cookie是否读出来，method可查看cookie有效 多账户如图：
![image](https://user-images.githubusercontent.com/63834404/172534292-379beceb-fa2d-42dc-ab4e-39cb965181fc.png)

6.7 修复了天选部分bug,新增bug，待会更新daily bug

6.6 删除原来的天选，新的配置，线程可设置1到7，最好就是3避免并发冲突，代码重构了一部分，可设置最大扫描页数 如图 ![image](https://user-images.githubusercontent.com/63834404/172145153-d9772e37-55df-4455-b6e3-e616fdc32469.png)


6.4 新增取关up主，配置文件更新，在refactor里看，需要取关多少就写多少，多账户同cookie格式填两个num 如图![image](https://user-images.githubusercontent.com/63834404/171981480-0dff8dea-f96f-4aef-82e0-7e85e333de39.png)


6.3 天选多线程版

6.2 修改了文件名称，小bug依旧没修复

6.1 添加天选时刻，还没有分组功能过几天放假赶出来，小bug多，加入直播签到

5.29 修复小bug,今天写天选

改播放视频为动态视频随机播放一个
 
使用方法：青龙就挂着Daily.py 这个文件就行了定时随意，把cookie填进Bilibili_config.json,json文件和py都要在同一个目录才行

目前用于测试查看，后续添加天选时刻自动筛选关注抽奖,目前只有投币和转发任务

使用方法：json文件写入bilibili的cookie，多账户就多添加一个"cookie":"",如下：

不需要多账户就删掉一个，默认配置一个

api来源：bilibili-API-collect   和  bilibili.com
