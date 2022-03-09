import asyncio, os, sys
import base64

from nonebot import (get_bot, get_driver, logger, on_command, on_startswith,
                     on_regex, require)
from nonebot.adapters.cqhttp import (GROUP, PRIVATE_FRIEND, Bot,
                                     GroupMessageEvent, MessageEvent,
                                     MessageSegment)
from nonebot.adapters.cqhttp.exception import ActionFailed
from nonebot.permission import SUPERUSER


sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from mihoyo_libs.get_data import *
from mihoyo_libs.get_image import *
from mihoyo_libs.get_mihoyo_bbs_data import *
from mihoyo_libs.mihoyo_bot_feature.super_command import *
from mihoyo_libs.mihoyo_bot_feature.query_mys_info import *

config = get_driver().config
priority = config.genshinuid_priority if config.genshinuid_priority else 2
superusers = {int(x) for x in config.superusers}

draw_event_schedule = require("nonebot_plugin_apscheduler").scheduler
clean_cache_schedule = require("nonebot_plugin_apscheduler").scheduler
daily_sign_schedule = require("nonebot_plugin_apscheduler").scheduler
resin_notic_schedule = require("nonebot_plugin_apscheduler").scheduler

get_weapon = on_startswith("武器", priority=priority)
get_char = on_startswith("角色", priority=priority)
get_cost = on_startswith("材料", priority=priority)
get_polar = on_startswith("命座", priority=priority)
get_talents = on_startswith("天赋", priority=priority)
get_enemies = on_startswith("原魔", priority=priority)
get_audio = on_startswith("语音", priority=priority)
get_artifacts = on_startswith("圣遗物", priority=priority)
get_food = on_startswith("食物", priority=priority)

# 米游社查询个人信息
get_uid_info = on_startswith("#uid", priority=priority)
get_mys_info = on_startswith("#mys", priority=priority)
search = on_command("查询", priority=priority)

# 米游社查询公共信息
get_event = on_command("活动列表", priority=priority)
get_lots = on_command("御神签", priority=priority)

# 米游社功能 签到|树脂
get_sign = on_command("签到", priority=priority)
monthly_data = on_command("每月统计", priority=priority)
daily_data = on_command("当前状态", priority=priority)
open_switch = on_command("开启", priority=priority)
close_switch = on_command("关闭", priority=priority)

# bot信息绑定
link_mys = on_startswith("绑定mys", priority=priority)
link_uid = on_startswith("绑定uid", priority=priority)

# cookie
add_cookie = on_startswith("添加", permission=PRIVATE_FRIEND, priority=priority)

# 管理员
check = on_command("校验全部Cookies", permission=SUPERUSER, priority=priority)
all_recheck = on_command("#全部重签", permission=SUPERUSER, priority=priority)
# other
get_char_adv = on_regex("[\u4e00-\u9fa5]+(用什么|能用啥|怎么养)", priority=priority)
get_weapon_adv = on_regex("[\u4e00-\u9fa5]+(能给谁|给谁用|要给谁|谁能用)", priority=priority)

FILE_PATH = os.path.join(os.path.dirname(__file__), 'mihoyo_bbs')
INDEX_PATH = os.path.join(FILE_PATH, 'index')
TEXTURE_PATH = os.path.join(FILE_PATH, 'texture2d')
# FILE_PATH_1 = os.path.join(os.path.dirname(__file__), 'mihoyo_bot_feature')

@get_char_adv.handle()
async def send_char_adv(bot: Bot, event: MessageEvent):
    try:
        name = str(event.get_message()).strip().replace(" ", "")[:-3]
        im = await char_adv(name)
        await get_char_adv.send(im)
    except Exception as e:
        logger.exception("获取建议失败。")


@get_weapon_adv.handle()
async def send_weapon_adv(bot: Bot, event: MessageEvent):
    try:
        name = str(event.get_message()).strip().replace(" ", "")[:-3]
        im = await weapon_adv(name)
        await get_weapon_adv.send(im)
    except Exception as e:
        logger.exception("获取建议失败。")


@get_audio.handle()
async def send_audio(bot: Bot, event: MessageEvent):
    message = str(event.get_message()).strip()
    message = message.replace('语音', "").replace(' ', "")
    name = ''.join(re.findall('[\u4e00-\u9fa5]', message))
    im = await audio_wiki(name, message)
    try:
        if name == "列表":
            await get_audio.send(MessageSegment.image(im))
        else:
            await get_audio.send(MessageSegment.record(im))
    except ActionFailed:
        await get_audio.send("不存在该语音ID或者不存在该角色。")
        logger.exception("获取语音失败")
    except Exception:
        await get_audio.send("可能是FFmpeg环境未配置。")
        logger.exception("获取语音失败")


@get_lots.handle()
async def send_lots(bot: Bot, event: MessageEvent):
    try:
        qid = int(event.sender.user_id)
        raw_data = await get_a_lots(qid)
        im = base64.b64decode(raw_data).decode("utf-8")
        await get_lots.send(im)
    except ActionFailed as e:
        await get_lots.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送御神签失败")
    except Exception as e:
        await get_lots.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("获取御神签错误")


@get_enemies.handle()
async def send_enemies(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('原魔', "").replace(' ', "")
        im = await enemies_wiki(message)
        await get_enemies.send(im)
    except ActionFailed as e:
        await get_lots.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送怪物信息失败")
    except Exception as e:
        await get_enemies.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("获取怪物信息错误")


@get_food.handle()
async def send_food(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('食物', "").replace(' ', "")
        im = await foods_wiki(message)
        await get_food.send(im)
    except ActionFailed as e:
        await get_lots.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送食物信息失败")
    except Exception as e:
        await get_food.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("获取食物信息错误")


@get_artifacts.handle()
async def send_artifacts(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('圣遗物', "").replace(' ', "")
        im = await artifacts_wiki(message)
        await get_artifacts.send(im)
    except ActionFailed as e:
        await get_lots.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送圣遗物信息失败")
    except Exception as e:
        await get_artifacts.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("获取圣遗物信息错误")


@get_weapon.handle()
async def send_weapon(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('武器', "")
        message = message.replace(' ', "")
        name = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        level = re.findall(r"[0-9]+", message)
        if len(level) == 1:
            im = await weapon_wiki(name, level=level[0])
        else:
            im = await weapon_wiki(name)
        await get_weapon.send(im)
    except ActionFailed as e:
        await get_lots.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送武器信息失败")
    except Exception as e:
        await get_weapon.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("获取武器信息错误")


@get_talents.handle()
async def send_talents(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('天赋', "")
        message = message.replace(' ', "")
        name = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        num = re.findall(r"[0-9]+", message)
        if len(num) == 1:
            im = await char_wiki(name, "talents", num[0])
            if isinstance(im, list):
                await bot.call_api("send_group_forward_msg", group_id=event.group_id, messages=im)
                return
        else:
            im = "参数不正确。"
        await get_talents.send(im)
    except ActionFailed as e:
        await get_lots.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送天赋信息失败")
    except Exception as e:
        await get_talents.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("获取天赋信息错误")


@get_char.handle()
async def send_char(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('角色', "")
        message = message.replace(' ', "")
        name = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        level = re.findall(r"[0-9]+", message)
        if len(level) == 1:
            im = await char_wiki(name, "char", level=level[0])
        else:
            im = await char_wiki(name)
        await get_char.send(im)
    except ActionFailed as e:
        await get_lots.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送角色信息失败")
    except Exception as e:
        await get_char.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("获取角色信息错误")


@get_cost.handle()
async def send_cost(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('材料', "")
        message = message.replace(' ', "")
        im = await char_wiki(message, "costs")
        await get_cost.send(im)
    except ActionFailed as e:
        await get_lots.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送材料信息失败")
    except Exception as e:
        await get_cost.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("获取材料信息错误")


@get_polar.handle()
async def send_polar(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('命座', "")
        message = message.replace(' ', "")
        num = int(re.findall(r"\d+", message)[0])  # str
        m = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        if num <= 0 or num > 6:
            await get_weapon.finish("你家{}有{}命？".format(m, num))
        im = await char_wiki(m, "constellations", num)
        await get_polar.send(im)
    except ActionFailed as e:
        await get_lots.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送命座信息失败")
    except Exception as e:
        await get_polar.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("获取命座信息错误")
