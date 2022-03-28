import asyncio, os, sys, re
import base64

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from nonebot import (get_bot, get_driver, on_command, on_regex, on_startswith, on_message, require)
from nonebot.adapters.cqhttp import (Bot, GROUP, GroupMessageEvent, MessageEvent, PRIVATE_FRIEND, MessageSegment)
from nonebot.adapters.cqhttp.exception import ActionFailed
from nonebot.permission import SUPERUSER

from ..get_image import *
from ..get_mihoyo_bbs_data import *
from ..get_data import *

config = get_driver().config
priority = config.genshinuid_priority if config.genshinuid_priority else 2
superusers = {int(x) for x in config.superusers}

FILE_PATH = os.path.join(os.path.join(os.path.dirname(__file__), 'mihoyo_libs'), 'mihoyo_bbs')
INDEX_PATH = os.path.join(FILE_PATH, 'index')
TEXTURE_PATH = os.path.join(FILE_PATH, 'texture2d')

get_event = on_command("活动列表", priority=priority)
get_lots = on_command("御神签", priority=priority)

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
