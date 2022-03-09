import asyncio, os, sys, re
import base64

from src.plugins.GenshinUID import get_lots, FILE_PATH, get_event
from nonebot import get_driver, logger
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment
from nonebot.adapters.cqhttp.exception import ActionFailed
from nonebot.permission import SUPERUSER

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
config = get_driver().config
priority = config.genshinuid_priority if config.genshinuid_priority else 2
superusers = {int(x) for x in config.superusers}

"""
米游社 活动列表 功能
"""


@get_event.handle()
async def send_events(bot: Bot, event: MessageEvent):
    try:
        img_path = os.path.join(FILE_PATH, "event.jpg")
        while True:
            if os.path.exists(img_path):
                f = open(img_path, 'rb')
                ls_f = base64.b64encode(f.read()).decode()
                img_mes = 'base64://' + ls_f
                f.close()
                im = MessageSegment.image(img_mes)
                break
            else:
                await draw_event_pic()
        await get_event.send(im)
    except ActionFailed as e:
        await get_lots.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送活动列表失败")
    except Exception as e:
        await get_event.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("获取活动列表错误")
