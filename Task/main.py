import asyncio
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Daily import dailytask


async def job():
    daily = dailytask()
    await daily.run()


# 创建调度程序对象
scheduler = AsyncIOScheduler()
tz = pytz.timezone('Asia/Shanghai')
# 设置定时任务，在每天晚上8点执行job函数
scheduler.add_job(job, 'cron', hour='18', minute=17, timezone=tz)
scheduler.add_job(job, 'cron', hour=18, minute=18, timezone=tz)
# 启动调度程序
scheduler.start()

# 进入事件循环 调度程序
asyncio.get_event_loop().run_forever()
