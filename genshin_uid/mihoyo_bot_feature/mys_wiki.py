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
get_weapon = on_startswith('武器', priority=priority)
get_char = on_startswith('角色', priority=priority)
get_cost = on_startswith('材料', priority=priority)
get_polar = on_startswith('命座', priority=priority)
get_talents = on_startswith('天赋', priority=priority)
get_enemies = on_startswith('原魔', priority=priority)
get_audio = on_startswith('语音', priority=priority)
get_artifacts = on_startswith('圣遗物', priority=priority)
get_food = on_startswith('食物', priority=priority)
get_char_adv = on_regex('[\u4e00-\u9fa5]+(用什么|能用啥|怎么养)', priority=priority)
get_weapon_adv = on_regex('[\u4e00-\u9fa5]+(能给谁|给谁用|要给谁|谁能用)', priority=priority)

get_guide_pic = on_regex('[\u4e00-\u9fa5]+(推荐|攻略)', priority=priority)

"""
米游社 活动列表 功能
"""


@get_event.handle()
async def send_events(bot: Bot, event: MessageEvent):
    try:
        img_mes = await get_event_pic()
        await get_event.send(MessageSegment.image(img_mes))
    except ActionFailed as e:
        await get_lots.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送活动列表失败")
    except Exception as e:
        await get_event.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("获取活动列表错误")


"""
武器给谁用
"""


@get_weapon_adv.handle()
async def send_weapon_adv(bot: Bot, event: MessageEvent):
    try:
        name = str(event.get_message()).strip().replace(' ', '')[:-3]
        im = await weapon_adv(name)
        await get_weapon_adv.send(im)
    except Exception:
        logger.exception('获取建议失败。')


"""
武器
"""


@get_weapon.handle()
async def send_weapon(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('武器', '')
        message = message.replace(' ', '')
        name = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        level = re.findall(r'[0-9]+', message)
        if len(level) == 1:
            im = await weapon_wiki(name, level=level[0])
        else:
            im = await weapon_wiki(name)
        await get_weapon.send(im)
    except ActionFailed as e:
        await get_weapon.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送武器信息失败')
    except Exception as e:
        await get_weapon.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('获取武器信息错误')


"""
角色
"""


@get_char.handle()
async def send_char(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('角色', '')
        message = message.replace(' ', '')
        name = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        level = re.findall(r'[0-9]+', message)
        if len(level) == 1:
            im = await char_wiki(name, 'char', level=level[0])
        else:
            im = await char_wiki(name)
        await get_char.send(im)
    except ActionFailed as e:
        await get_char.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送角色信息失败')
    except Exception as e:
        await get_char.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('获取角色信息错误')


"""
材料
"""


@get_cost.handle()
async def send_cost(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('材料', '')
        message = message.replace(' ', '')
        im = await char_wiki(message, 'costs')
        await get_cost.send(im)
    except ActionFailed as e:
        await get_cost.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送材料信息失败')
    except Exception as e:
        await get_cost.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('获取材料信息错误')


"""
命座
"""


@get_polar.handle()
async def send_polar(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('命座', '')
        message = message.replace(' ', '')
        num = int(re.findall(r'\d+', message)[0])  # str
        m = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        if num <= 0 or num > 6:
            await get_polar.finish('你家{}有{}命？'.format(m, num))
        im = await char_wiki(m, 'constellations', num)
        await get_polar.send(im)
    except ActionFailed as e:
        await get_polar.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送命座信息失败')
    except Exception as e:
        await get_polar.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('获取命座信息错误')


"""
天赋
"""


@get_talents.handle()
async def send_talents(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('天赋', '')
        message = message.replace(' ', '')
        name = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        num = re.findall(r'[0-9]+', message)
        if len(num) == 1:
            im = await char_wiki(name, 'talents', num[0])
            if isinstance(im, list):
                await bot.call_api('send_group_forward_msg', group_id=event.group_id, messages=im)
                return
        else:
            im = '参数不正确。'
        await get_talents.send(im)
    except ActionFailed as e:
        await get_talents.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送天赋信息失败')
    except Exception as e:
        await get_talents.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('获取天赋信息错误')


"""
原魔
"""


@get_enemies.handle()
async def send_enemies(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('原魔', '').replace(' ', '')
        im = await enemies_wiki(message)
        await get_enemies.send(im)
    except ActionFailed as e:
        await get_enemies.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送怪物信息失败')
    except Exception as e:
        await get_enemies.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('获取怪物信息错误')


"""
语音
"""


@get_audio.handle()
async def send_audio(bot: Bot, event: MessageEvent):
    message = str(event.get_message()).strip()
    message = message.replace('语音', '').replace(' ', '')
    name = ''.join(re.findall('[\u4e00-\u9fa5]', message))
    im = await audio_wiki(name, message)
    try:
        if name == '列表':
            await get_audio.send(MessageSegment.image(im))
        else:
            await get_audio.send(MessageSegment.record(im))
    except ActionFailed:
        await get_audio.send('语音发送失败。')
        logger.exception('语音发送失败')
    except Exception:
        await get_audio.send('可能是FFmpeg环境未配置。')
        logger.exception('ffmpeg未配置')


"""
圣遗物
"""


@get_artifacts.handle()
async def send_artifacts(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('圣遗物', '').replace(' ', '')
        im = await artifacts_wiki(message)
        await get_artifacts.send(im)
    except ActionFailed as e:
        await get_artifacts.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送圣遗物信息失败')
    except Exception as e:
        await get_artifacts.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('获取圣遗物信息错误')


"""
食物
"""


@get_food.handle()
async def send_food(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip()
        message = message.replace('食物', '').replace(' ', '')
        im = await foods_wiki(message)
        await get_food.send(im)
    except ActionFailed as e:
        await get_food.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送食物信息失败')
    except Exception as e:
        await get_food.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('获取食物信息错误')


"""
用什么，怎么养
"""


@get_char_adv.handle()
async def send_char_adv(bot: Bot, event: MessageEvent):
    try:
        name = str(event.get_message()).strip().replace(' ', '')[:-3]
        im = await char_adv(name)
        await get_char_adv.send(im)
    except Exception:
        logger.exception('获取建议失败。')


"""
攻略
"""


@get_guide_pic.handle()
async def send_guide_pic(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip().replace(' ', '')[:-2]
        with open(os.path.join(INDEX_PATH, 'char_alias.json'), 'r', encoding='utf8')as fp:
            char_data = json.load(fp)
        name = message
        for i in char_data:
            if message in i:
                name = i
            else:
                for k in char_data[i]:
                    if message in k:
                        name = i
        # name = str(event.get_message()).strip().replace(' ', '')[:-2]
        url = 'https://img.genshin.minigg.cn/guide/{}.jpg'.format(name)
        await get_guide_pic.send(MessageSegment.image(url))
    except Exception:
        logger.exception('获取建议失败。')
