# 群聊内 绑定米游社通行证 的命令，会绑定至当前qq号上，和绑定uid不冲突，两者可以同时绑定
from src.plugins.GenshinUID import link_mys, get_lots, connect_db, link_uid
import asyncio, os, sys, re
import base64

from nonebot import (get_bot, get_driver, logger, on_command, on_startswith,
                     on_regex, require)
from nonebot.adapters.cqhttp import (GROUP, PRIVATE_FRIEND, Bot,
                                     GroupMessageEvent, MessageEvent,
                                     MessageSegment)
from nonebot.adapters.cqhttp.exception import ActionFailed
from nonebot.permission import SUPERUSER

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
config = get_driver().config
priority = config.genshinuid_priority if config.genshinuid_priority else 2
superusers = {int(x) for x in config.superusers}

"""
绑定uid 的命令，会绑定至当前qq号上
"""


@link_uid.handle()
async def link_uid_to_qq(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip().replace(
            ' ', "").replace('绑定uid', "")
        uid = re.findall(r"\d+", message)[0]  # str
        await connect_db(int(event.sender.user_id), uid)
        await link_uid.send('绑定uid成功！试试 命令 查询', at_sender=True)
    except ActionFailed as e:
        await get_lots.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送绑定信息失败")
    except Exception as e:
        await link_uid.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("绑定uid异常")


"""
绑定米游社通行证 的命令，会绑定至当前qq号上，和绑定uid不冲突，两者可以同时绑定
"""


@link_mys.handle()
async def link_mihoyo_bbs_to_qq(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip().replace(
            ' ', "").replace('绑定mys', "")
        mys = re.findall(r"\d+", message)[0]  # str
        await connect_db(int(event.sender.user_id), None, mys)
        await link_mys.send('绑定米游社id成功！发送：查询 获取信息', at_sender=True)
    except ActionFailed as e:
        await get_lots.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送绑定信息失败")
    except Exception as e:
        await link_mys.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("绑定米游社通行证异常")
