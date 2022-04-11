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

check = on_command("校验全部Cookies", permission=SUPERUSER, priority=priority)

"""
校验Cookies 是否正常的功能，不正常自动删掉
"""

@check.handle()
async def check_cookies(bot: Bot):
    try:
        raw_mes = await check_db()
        im = raw_mes[0]
        await check.send(im)
        for i in raw_mes[1]:
            await bot.call_api(api='send_private_msg', **{
                'user_id': i[0],
                'message': ('您绑定的Cookies（uid{}）已失效，以下功能将会受到影响：\n'
                            '查看完整信息列表\n查看深渊配队\n自动签到/当前状态/每月统计\n'
                            '请及时重新绑定Cookies并重新开关相应功能。').format(i[1])
            })
            await asyncio.sleep(3 + random.randint(1, 3))
    except ActionFailed as e:
        await check.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送Cookie校验信息失败')
    except Exception as e:
        await check.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('Cookie校验错误')
