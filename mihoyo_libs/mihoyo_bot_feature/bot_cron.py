import asyncio, os, sys, re
import base64
import random
from src.plugins.GenshinUID import sign, config_check, draw_event_schedule, draw_event_pic, clean_cache_schedule, \
    delete_cache, resin_notic_schedule, daily, sqlite3, daily_sign_schedule
from nonebot import (get_bot, get_driver, logger)
from nonebot.adapters.cqhttp import (MessageSegment)

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
config = get_driver().config
priority = config.genshinuid_priority if config.genshinuid_priority else 2
superusers = {int(x) for x in config.superusers}


@draw_event_schedule.scheduled_job('cron', hour='2')
async def draw_event():
    await draw_event_pic()


"""
每日零点清空cookies使用缓存
"""


@clean_cache_schedule.scheduled_job('cron', hour='0')
async def clean_cache():
    await delete_cache()


"""
每隔半小时检测树脂是否超过设定值
"""


@resin_notic_schedule.scheduled_job('cron', minute="*/30")
async def push():
    bot = get_bot()
    now_data = await daily()
    if now_data is not None:
        for i in now_data:
            if i['gid'] == "on":
                await bot.call_api(api='send_private_msg', **{'user_id': i['qid'], 'message': i['message']})
            else:
                await bot.call_api(api='send_group_msg',
                                   **{'group_id': i['gid'],
                                      'message': MessageSegment.at(i['qid']) + f"\n{i['message']}"})
    else:
        pass


"""
 每日零点半进行米游社签到
"""


@daily_sign_schedule.scheduled_job('cron', hour='0', minute="30")
async def sign_at_night():
    await daily_sign()


async def daily_sign():
    bot = get_bot()
    conn = sqlite3.connect('ID_DATA.db')
    c = conn.cursor()
    cursor = c.execute(
        "SELECT *  FROM NewCookiesTable WHERE StatusB != ?", ("off",))
    c_data = cursor.fetchall()
    temp_list = []
    for row in c_data:
        im = await sign(str(row[0]))
        if row[4] == "on":
            try:
                await bot.call_api(api='send_private_msg',
                                   user_id=row[2], message=im)
            except Exception:
                logger.exception(f"{im} Error")
        else:
            message = MessageSegment.at(row[2]) + f"\n{im}"
            if await config_check("SignReportSimple"):
                for i in temp_list:
                    if row[4] == i["push_group"]:
                        if im == "签到失败，请检查Cookies是否失效。" or im.startswith("网络有点忙，请稍后再试~!"):
                            i["failed"] += 1
                            i["push_message"] += "\n" + message
                        else:
                            i["success"] += 1
                        break
                else:
                    if im == "签到失败，请检查Cookies是否失效。":
                        temp_list.append(
                            {"push_group": row[4], "push_message": message, "success": 0, "failed": 1})
                    else:
                        temp_list.append(
                            {"push_group": row[4], "push_message": "", "success": 1, "failed": 0})
            else:
                for i in temp_list:
                    if row[4] == i["push_group"] and i["num"] < 4:
                        i["push_message"] += "\n" + message
                        i["num"] += 1
                        break
                else:
                    temp_list.append(
                        {"push_group": row[4], "push_message": message, "num": 1})
        await asyncio.sleep(6 + random.randint(1, 3))
    if await config_check("SignReportSimple"):
        for i in temp_list:
            try:
                report = "以下为签到失败报告：{}".format(
                    i["push_message"]) if i["push_message"] != "" else ""
                await bot.call_api(
                    api='send_group_msg', group_id=i["push_group"],
                    message="今日自动签到已完成！\n本群共签到成功{}人，共签到失败{}人。{}".format(i["success"], i["failed"], report))
            except Exception:
                logger.exception("签到报告发送失败：{}".format(i["push_message"]))
            await asyncio.sleep(4 + random.randint(1, 3))
    else:
        for i in temp_list:
            try:
                await bot.call_api(
                    api='send_group_msg', group_id=i["push_group"], message=i["push_message"])
            except Exception:
                logger.exception("签到报告发送失败：{}".format(i["push_message"]))
            await asyncio.sleep(4 + random.randint(1, 3))
