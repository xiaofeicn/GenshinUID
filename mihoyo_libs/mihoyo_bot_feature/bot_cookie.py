import asyncio, os, sys, re, random
import base64

from src.plugins.GenshinUID import get_lots, check, check_db, add_cookie, deal_ck
from nonebot import (get_driver, logger)
from nonebot.adapters.cqhttp import (Bot, MessageEvent)
from nonebot.adapters.cqhttp.exception import ActionFailed

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
config = get_driver().config
priority = config.genshinuid_priority if config.genshinuid_priority else 2
superusers = {int(x) for x in config.superusers}

"""
添加 cookie 功能
"""


@add_cookie.handle()
async def add_cookie_func(bot: Bot, event: MessageEvent):
    try:
        mes = str(event.get_message()).strip().replace('添加', "")
        await deal_ck(mes, int(event.sender.user_id))
        await add_cookie.send(
            f'添加Cookies成功！\nCookies属于个人重要信息，如果你是在不知情的情况下添加，请马上修改米游社账户密码，保护个人隐私！\n————\n'
            f'如果需要【开启自动签到】和【开启推送】还需要使用命令“绑定uid”绑定你的uid。\n例如：绑定uid123456789。')
    except ActionFailed as e:
        await get_lots.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送Cookie校验信息失败")
    except Exception as e:
        await add_cookie.send('校验失败！请输入正确的Cookies！\n错误信息为{}'.format(e))
        logger.exception("Cookie校验失败")
