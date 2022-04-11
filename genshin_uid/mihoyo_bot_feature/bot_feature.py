import asyncio, os, sys, re, random
import base64

from nonebot.typing import T_State

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from nonebot import (get_bot, get_driver, on_command, on_regex, on_startswith, on_message, require, on_notice)
from nonebot.adapters.cqhttp import (Bot, GROUP, GroupMessageEvent, MessageEvent, PRIVATE_FRIEND, MessageSegment,
                                     GroupIncreaseNoticeEvent, Message)
from nonebot.adapters.cqhttp.exception import ActionFailed
from nonebot.permission import SUPERUSER

from ..get_image import *
from ..get_mihoyo_bbs_data import *
from ..get_data import *

config = get_driver().config
priority = config.genshinuid_priority if config.genshinuid_priority else 2
superusers = {int(x) for x in config.superusers}
chat = on_message(priority=10)
welcom = on_notice()
get_help = on_command('help', aliases={'帮助'}, priority=priority)
tell_master = on_startswith('带话', priority=priority)


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


"""
帮助
"""


@get_help.handle()
async def send_help_pic(bot: Bot, event: MessageEvent):
    try:
        help_path = os.path.join(INDEX_PATH, 'help.png')
        f = open(help_path, 'rb')
        ls_f = b64encode(f.read()).decode()
        img_mes = 'base64://' + ls_f
        f.close()
        await get_help.send(MessageSegment.image(img_mes))
    except Exception:
        logger.exception('获取帮助失败。')


# 群友入群
@welcom.handle()  # 监听 welcom
async def h_r(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):  # event: GroupIncreaseNoticeEvent  群成员增加事件
    user = event.get_user_id()  # 获取新成员的id
    at_ = "本群通过祈愿召唤了旅行者：[CQ:at,qq={}]".format(user)
    msg = at_ + '欢迎：\n 派蒙好伙伴、捕风的异乡人、蒙德荣誉骑士、脱手型元素专家、一锅乱炖小食神、风魔龙净化者、雪山派炼金术师、秘境闯关人、地图收割机、萍姥姥冲击波受益者、滴水不沾外卖员、海灯节霄灯制作人、尘歌壶洞主、浪船驾驶员、七七守护人、公子好基友、若坨再度封印推动者、神里心上人、心海心情增益量、申鹤红绳羁绊者、女士被灭助推器、海祈岛第一战力、鹤观无尽轮回终结者、渊下宫传承人、深渊破坏者、天空岛顶级通缉犯、提瓦特故事见证人，杀怪放火第一人、世人敬仰旅行者\n发送help查看派蒙功能哦'
    msg = Message(msg)

    await welcom.finish(message=Message(f'{msg}'))  # 发送消息


# 带话
@tell_master.handle()
async def tell_master_func(bot: Bot, event: MessageEvent):
    is_to_me = event.to_me
    qid = event.user_id
    if is_to_me:
        message = str(event.get_message()).strip().replace(
            '带话', "")
        im = ''
        if event.message_type == 'group':
            im = '群：{}，成员：{} {} 带话说：{}'.format(event.group_id, event.sender.nickname, qid, message)
        else:
            im = '{} {} 带话说：{}'.format(event.sender.nickname, qid, message)
        yy = '我这就去带话'
        await tell_master.send(yy, at_sender=False)
        await bot.call_api(api='send_private_msg', **{'user_id': 271986756, 'message': im})
