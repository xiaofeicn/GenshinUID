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
chat = on_message(priority=10)

@chat.handle()
async def use_chat_func(bot: Bot, event: MessageEvent):
    target = 'https://api.ownthink.com/bot?appid=f40e478ad5d244b3b286807ec5b46880&userid=user&spoken='
    im = "干什么？"
    message = str(event.get_message()).strip().replace(
        ' ', "")
    # logger.exception(event.to_me)
    m = event.get_plaintext()
    yd = event.to_me
    try:
        if yd:
            tmp = target + m
            res = requests.get(tmp)
            im = str(res.json()['data']['info']['text']).replace("小思", "派蒙").replace("思知", "提瓦特")
            await chat.send(im, at_sender=False)
    except ActionFailed as e:
        await chat.send(im)