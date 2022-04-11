import asyncio, os, sys, re, random
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

add_cookie = on_startswith("添加", permission=PRIVATE_FRIEND, priority=priority)

"""
添加 cookie 功能
"""


@add_cookie.handle()
async def add_cookie_func(bot: Bot, event: MessageEvent):
    try:
        mes = str(event.get_message()).strip().replace('添加', '')
        im = await deal_ck(mes, int(event.sender.user_id))
        await add_cookie.send(im)
    except ActionFailed as e:
        await add_cookie.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送Cookie校验信息失败')
    except Exception as e:
        await add_cookie.send('校验失败！请输入正确的Cookies！\n错误信息为{}'.format(e))
        logger.exception('Cookie校验失败')
