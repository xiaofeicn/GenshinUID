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

use_book = on_command("help", priority=priority)

@use_book.handle()
async def use_book_func(bot: Bot, event: MessageEvent):
    im = "绑定mys+通行证ID  👉  绑定通行证\n" \
         "绑定uid+uid 👉  绑定UID\n" \
         "原魔公子 👉  原魔数据\n" \
         "#uid+uid 👉  查询此uid数据\n" \
         "#mys+通行证ID 👉  查询此通行证数据\n" \
         "添加+空格+cookie 👉  添加自己cookie【仅限好友私聊】\n" \
         "签到 👉  米游社签到【需绑定自己的cookie】\n" \
         "每月统计 👉  当月原石摩拉收入【需绑定自己的cookie】\n" \
         "当前状态 👉  当前任务|树脂|派遣【需绑定自己的cookie】\n" \
         "查看其他功能请发送 help\n"
    try:
        await use_book.send(im)
    except ActionFailed as e:
        await use_book.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送签到信息失败")