# Bilibili_Python
仅供个人学习

目前用于测试查看，后续添加天选时刻自动筛选关注抽奖,目前只有投币和转发任务

使用方法：json文件写入bilibili的cookie，多账户就多添加一个"cookie":"",如下：
格式：{
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
