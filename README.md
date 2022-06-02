# Bilibili_Python
仅供个人学习
我为什么写这个呢,主要就是闲的，其次就是我手机刷的青龙2.12.2模块运行不了 RayWangQvQ/BiliBiliToolPro 所以就写这个，其次就是想练习一下爬虫
目前功能还没有完善，完善后会进行一次代码封装去除多余函数。
可以关注我B站uid：289549318
有建议的功能可以告诉我我尽量加上
新手，不喜勿喷
## 注意：拉要四个py文件一个config.json 在青龙之需要挂着Bilibili_Daily.py和Bilibili_CT.py(一个任务，一个天选，取关还没写)

6.2 修改了文件名称，小bug依旧没修复

6.1 添加天选时刻，还没有分组功能过几天放假赶出来，小bug多，加入直播签到

5.29 修复小bug,今天写天选

改播放视频为动态视频随机播放一个
 
使用方法：青龙就挂着Daily.py 这个文件就行了定时随意，把cookie填进Bilibili_config.json,json文件和py都要在同一个目录才行

目前用于测试查看，后续添加天选时刻自动筛选关注抽奖,目前只有投币和转发任务

使用方法：json文件写入bilibili的cookie，多账户就多添加一个"cookie":"",如下：

### 格式：
{
  "Users": [
    {
      "Cookie": ""
    },
    {
      "Cookie": ""
    }
  ]
}


不需要多账户就删掉一个，默认配置一个

api来源：bilibili-API-collect   和  bilibili.com
