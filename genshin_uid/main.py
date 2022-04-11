import base64

from nonebot import (get_bot, get_driver, on_command, on_regex, on_startswith, on_message, require, on_notice)
from nonebot.adapters.cqhttp import (Bot, GROUP, GroupMessageEvent, MessageEvent, PRIVATE_FRIEND, MessageSegment,
                                     GroupIncreaseNoticeEvent,Message)
from nonebot.adapters.cqhttp.exception import ActionFailed
from nonebot.permission import SUPERUSER

# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# from .get_data import *
from nonebot.typing import T_State

from .get_image import *
from .get_mihoyo_bbs_data import *

config = get_driver().config
priority = config.genshinuid_priority if config.genshinuid_priority else 2
superusers = {int(x) for x in config.superusers}

draw_event_schedule = require('nonebot_plugin_apscheduler').scheduler
clean_cache_schedule = require('nonebot_plugin_apscheduler').scheduler
daily_sign_schedule = require('nonebot_plugin_apscheduler').scheduler
daily_mihoyo_bbs_sign_schedule = require('nonebot_plugin_apscheduler').scheduler
resin_notic_schedule = require('nonebot_plugin_apscheduler').scheduler

get_weapon = on_startswith('武器', priority=priority)
get_char = on_startswith('角色', priority=priority)
get_cost = on_startswith('材料', priority=priority)
get_polar = on_startswith('命座', priority=priority)
get_talents = on_startswith('天赋', priority=priority)
get_enemies = on_startswith('原魔', priority=priority)
get_audio = on_startswith('语音', priority=priority)
get_artifacts = on_startswith('圣遗物', priority=priority)
get_food = on_startswith('食物', priority=priority)
tell_master = on_startswith('带话', priority=priority)

get_uid_info = on_startswith("uid", priority=priority)
get_mys_info = on_startswith("mys", priority=priority)

get_event = on_command('活动列表', priority=priority)
get_lots = on_command('御神签', priority=priority)
get_help = on_command('help',aliases={'帮助'}, priority=priority)

open_switch = on_startswith('开启', priority=priority)
close_switch = on_startswith('关闭', priority=priority)

link_mys = on_startswith('绑定mys', priority=priority)
link_uid = on_startswith('绑定uid', priority=priority)

monthly_data = on_command('每月统计', priority=priority)
daily_data = on_command('当前状态', priority=priority)

get_genshin_info = on_command('当前信息', priority=priority)

add_cookie = on_startswith('添加', permission=PRIVATE_FRIEND, priority=priority)

search = on_command("查询", priority=priority)
get_sign = on_command("签到", priority=priority)
get_mihoyo_coin = on_command("开始获取米游币", priority=priority)
check = on_command("校验全部Cookies", priority=priority)

all_genshinsign_recheck = on_command('全部重签', permission=SUPERUSER, priority=priority)
all_bbscoin_recheck = on_command('全部重获取', permission=SUPERUSER, priority=priority)

get_char_adv = on_regex('[\u4e00-\u9fa5]+(用什么|能用啥|怎么养)', priority=priority)
get_weapon_adv = on_regex('[\u4e00-\u9fa5]+(能给谁|给谁用|要给谁|谁能用)', priority=priority)

get_guide_pic = on_regex('[\u4e00-\u9fa5]+(推荐|攻略)', priority=priority)

welcom = on_notice()

use_book = on_command("fqhelp", priority=priority)
chat = on_message(priority=10)
FILE_PATH = os.path.join(os.path.join(os.path.dirname(__file__), 'mihoyo_libs'), 'mihoyo_bbs')
INDEX_PATH = os.path.join(FILE_PATH, 'index')
TEXTURE_PATH = os.path.join(FILE_PATH, 'texture2d')


# 群友入群
@welcom.handle()  # 监听 welcom
async def h_r(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):  # event: GroupIncreaseNoticeEvent  群成员增加事件
    user = event.get_user_id()  # 获取新成员的id
    at_ = "本群通过祈愿召唤了旅行者：[CQ:at,qq={}]".format(user)
    msg = at_ + '欢迎：\n 派蒙好伙伴、捕风的异乡人、蒙德荣誉骑士、脱手型元素专家、一锅乱炖小食神、风魔龙净化者、雪山派炼金术师、秘境闯关人、地图收割机、萍姥姥冲击波受益者、滴水不沾外卖员、海灯节霄灯制作人、尘歌壶洞主、浪船驾驶员、七七守护人、公子好基友、若坨再度封印推动者、神里心上人、心海心情增益量、申鹤红绳羁绊者、女士被灭助推器、海祈岛第一战力、鹤观无尽轮回终结者、渊下宫传承人、深渊破坏者、天空岛顶级通缉犯、提瓦特故事见证人，杀怪放火第一人、世人敬仰旅行者'
    msg = Message(msg)
    print(at_)
    # if event.group_id == QQ群号:
    await welcom.finish(message=Message(f'{msg}'))  # 发送消息

# 带话
@tell_master.handle()
async def tell_master_func(bot: Bot, event: MessageEvent):
    is_to_me=event.to_me
    qid=event.user_id
    group_id=event.group_id
    if is_to_me:
        message = str(event.get_message()).strip().replace(
            '带话', "")
        im =''
        if group_id is not None:
            im='群：{}，成员：{} 带话说：{}'.format(group_id,qid,message)
        else:
            im = '{} 带话说：{}'.format( qid, message)
        await bot.call_api(api='send_private_msg', **{'user_id': 271986756, 'message': im})


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

@use_book.handle()
async def use_book_func(bot: Bot, event: MessageEvent):
    im = "绑定mys+通行证ID  👉  绑定通行证\n" \
         "绑定uid+uid 👉  绑定UID\n" \
         "查询 👉  查询账号数据\n" \
         "活动列表 👉  当前活动\n" \
         "原魔公子 👉  原魔数据\n" \
         "#uid+uid 👉  查询此uid数据\n" \
         "#mys+通行证ID 👉  查询此通行证数据\n" \
         "添加+空格+cookie 👉  添加自己cookie【仅限好友私聊】\n" \
         "签到 👉  米游社签到【需绑定自己的cookie】\n" \
         "每月统计 👉  当月原石摩拉收入【需绑定自己的cookie】\n" \
         "当前状态 👉  当前任务|树脂|派遣【需绑定自己的cookie】\n" \
         "当前信息 👉  当前状态图片版\n" \
         "gs开启(自动签到|推送|简洁签到报告) 👉  开启米游社自动签到,推送【需绑定自己的cookie】\n" \
         "gs关闭(自动签到|推送|简洁签到报告) 👉  关闭米游社自动签到,推送【需绑定自己的cookie】\n" \
         "角色+角色名称 👉  角色信息\n" \
         "武器+角色名称 👉  武器信息\n" \
         "材料+角色名称 👉  材料信息\n" \
         "角色+(用什么|能用啥|怎么养) 👉  角色武器材料圣遗物\n" \
         "(材料名|圣遗物名|武器名)+(能给谁|给谁用|要给谁|谁能用) 👉  给谁用\n" \
         "查看其他功能请发送 help\n"
    try:
        await use_book.send(im)
    except ActionFailed as e:
        await use_book.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送签到信息失败")

@draw_event_schedule.scheduled_job('cron', hour='2')
async def draw_event():
    await draw_event_pic()


# 每日零点清空cookies使用缓存
@clean_cache_schedule.scheduled_job('cron', hour='0')
async def clean_cache():
    await delete_cache()


# 每隔半小时检测树脂是否超过设定值
@resin_notic_schedule.scheduled_job('cron', minute='*/30')
async def push():
    bot = get_bot()
    now_data = await daily()
    if now_data is not None:
        for i in now_data:
            if i['gid'] == 'on':
                await bot.call_api(api='send_private_msg', **{'user_id': i['qid'], 'message': i['message']})
            else:
                await bot.call_api(api='send_group_msg',
                                   **{'group_id': i['gid'],
                                      'message' : MessageSegment.at(i['qid']) + f'\n{i["message"]}'})


# 每日零点半进行米游社签到
@daily_sign_schedule.scheduled_job('cron', hour='0', minute='30')
async def sign_at_night():
    await daily_sign()

async def daily_sign():
    bot = get_bot()
    conn = sqlite3.connect('ID_DATA.db')
    c = conn.cursor()
    cursor = c.execute(
        'SELECT *  FROM NewCookiesTable WHERE StatusB != ?', ('off',))
    c_data = cursor.fetchall()
    temp_list = []
    for row in c_data:
        im = await sign(str(row[0]))
        if row[4] == 'on':
            try:
                await bot.call_api(api='send_private_msg',
                                   user_id=row[2], message=im)
            except Exception:
                logger.exception(f'{im} Error')
        else:
            message = MessageSegment.at(row[2]) + f'\n{im}'
            if await config_check('SignReportSimple'):
                for i in temp_list:
                    if row[4] == i['push_group']:
                        if im == '签到失败，请检查Cookies是否失效。' or im.startswith('网络有点忙，请稍后再试~!'):
                            i['failed'] += 1
                            i['push_message'] += '\n' + message
                        else:
                            i['success'] += 1
                        break
                else:
                    if im == '签到失败，请检查Cookies是否失效。':
                        temp_list.append(
                            {'push_group': row[4], 'push_message': message, 'success': 0, 'failed': 1})
                    else:
                        temp_list.append(
                            {'push_group': row[4], 'push_message': '', 'success': 1, 'failed': 0})
            else:
                for i in temp_list:
                    if row[4] == i['push_group'] and i['num'] < 4:
                        i['push_message'] += '\n' + message
                        i['num'] += 1
                        break
                else:
                    temp_list.append(
                        {'push_group': row[4], 'push_message': message, 'num': 1})
        await asyncio.sleep(6 + random.randint(1, 3))
    if await config_check('SignReportSimple'):
        for i in temp_list:
            try:
                report = '以下为签到失败报告：{}'.format(
                    i['push_message']) if i['push_message'] != '' else ''
                await bot.call_api(
                    api='send_group_msg', group_id=i['push_group'],
                    message='今日自动签到已完成！\n本群共签到成功{}人，共签到失败{}人。{}'.format(i['success'], i['failed'], report))
            except Exception:
                logger.exception('签到报告发送失败：{}'.format(i['push_message']))
            await asyncio.sleep(4 + random.randint(1, 3))
    else:
        for i in temp_list:
            try:
                await bot.call_api(
                    api='send_group_msg', group_id=i['push_group'], message=i['push_message'])
            except Exception:
                logger.exception('签到报告发送失败：{}'.format(i['push_message']))
            await asyncio.sleep(4 + random.randint(1, 3))


# 每日零点五十进行米游币获取
@daily_mihoyo_bbs_sign_schedule.scheduled_job('cron', hour='0', minute='50')
async def sign_at_night():
    await daily_mihoyo_bbs_sign()


async def daily_mihoyo_bbs_sign():
    bot = get_bot()
    conn = sqlite3.connect('ID_DATA.db')
    c = conn.cursor()
    cursor = c.execute(
        'SELECT *  FROM NewCookiesTable WHERE StatusC != ?', ('off',))
    c_data = cursor.fetchall()
    logger.info(c_data)
    for row in c_data:
        logger.info('正在执行{}'.format(row[0]))
        if row[8]:
            await asyncio.sleep(5 + random.randint(1, 3))
            im = await mihoyo_coin(str(row[2]), str(row[8]))
            logger.info(im)
            try:
                await bot.call_api(api='send_private_msg',
                                   user_id=row[2], message=im)
            except Exception:
                logger.exception(f'{im} Error')
    logger.info('已结束。')

@get_help.handle()
async def send_help_pic(bot: Bot, event: MessageEvent):
    try:
        help_path = os.path.join(INDEX_PATH,'help.png')
        f = open(help_path, 'rb')
        ls_f = b64encode(f.read()).decode()
        img_mes = 'base64://' + ls_f
        f.close()
        await get_help.send(MessageSegment.image(img_mes))
    except Exception:
        logger.exception('获取帮助失败。')

@get_guide_pic.handle()
async def send_guide_pic(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip().replace(' ', '')[:-2]
        with open(os.path.join(INDEX_PATH,'char_alias.json'),'r',encoding='utf8')as fp:
            char_data = json.load(fp)
        name = message
        for i in char_data:
            if message in i:
                name = i
            else:
                for k in char_data[i]:
                    if message in k:
                        name = i
        #name = str(event.get_message()).strip().replace(' ', '')[:-2]
        url = 'https://img.genshin.minigg.cn/guide/{}.jpg'.format(name)
        await get_guide_pic.send(MessageSegment.image(url))
    except Exception:
        logger.exception('获取建议失败。')

@get_char_adv.handle()
async def send_char_adv(bot: Bot, event: MessageEvent):
    try:
        name = str(event.get_message()).strip().replace(' ', '')[:-3]
        im = await char_adv(name)
        await get_char_adv.send(im)
    except Exception:
        logger.exception('获取建议失败。')


@get_weapon_adv.handle()
async def send_weapon_adv(bot: Bot, event: MessageEvent):
    try:
        name = str(event.get_message()).strip().replace(' ', '')[:-3]
        im = await weapon_adv(name)
        await get_weapon_adv.send(im)
    except Exception:
        logger.exception('获取建议失败。')


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


@get_lots.handle()
async def send_lots(bot: Bot, event: MessageEvent):
    try:
        qid = int(event.sender.user_id)
        raw_data = await get_a_lots(qid)
        im = base64.b64decode(raw_data).decode('utf-8')
        await get_lots.send(im)
    except ActionFailed as e:
        await get_lots.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送御神签失败')
    except Exception as e:
        await get_lots.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('获取御神签错误')


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


@get_event.handle()
async def send_events(bot: Bot, event: MessageEvent):
    try:
        img_mes = await get_event_pic()
        await get_event.send(MessageSegment.image(img_mes))
    except ActionFailed as e:
        await get_lots.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送活动列表失败')
    except Exception as e:
        await get_event.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('获取活动列表错误')


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


# 开启 自动签到 和 推送树脂提醒 功能
@open_switch.handle()
async def open_switch_func(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip().replace(
            ' ', '').replace('开启', '')
        m = ''.join(re.findall('[\u4e00-\u9fa5]', message))

        qid = int(event.sender.user_id)
        at = re.search(r'\[CQ:at,qq=(\d*)]', message)

        if m == '自动签到':
            try:
                if at and qid in superusers:
                    qid = at.group(1)
                elif at and at.group(1) != qid:
                    await open_switch.send('你没有权限。', at_sender=True)
                    return
                else:
                    pass
                gid = event.get_session_id().split('_')[1] if len(
                    event.get_session_id().split('_')) == 3 else 'on'
                uid = await select_db(qid, mode='uid')
                im = await open_push(int(uid[0]), qid, str(gid), 'StatusB')
                await open_switch.send(im, at_sender=True)
            except Exception:
                await open_switch.send('未绑定uid信息！', at_sender=True)
        elif m == '推送':
            try:
                if at and qid in superusers:
                    qid = at.group(1)
                elif at and at.group(1) != qid:
                    await open_switch.send('你没有权限。', at_sender=True)
                    return
                else:
                    pass
                gid = event.get_session_id().split('_')[1] if len(
                    event.get_session_id().split('_')) == 3 else 'on'
                uid = await select_db(qid, mode='uid')
                im = await open_push(int(uid[0]), qid, str(gid), 'StatusA')
                await open_switch.send(im, at_sender=True)
            except Exception:
                await open_switch.send('未绑定uid信息！', at_sender=True)
        elif m == '自动米游币':
            try:
                if at and qid in superusers:
                    qid = at.group(1)
                elif at and at.group(1) != qid:
                    await close_switch.send('你没有权限。', at_sender=True)
                    return
                else:
                    pass
                gid = event.get_session_id().split('_')[1] if len(
                    event.get_session_id().split('_')) == 3 else 'on'
                uid = await select_db(qid, mode='uid')
                im = await open_push(int(uid[0]), qid, str(gid), 'StatusC')
                await open_switch.send(im, at_sender=True)
            except Exception:
                await open_switch.send('未绑定uid信息！', at_sender=True)
        elif m == '简洁签到报告':
            try:
                if qid in superusers:
                    _ = await config_check('SignReportSimple', 'OPEN')
                    await open_switch.send('成功!', at_sender=True)
                else:
                    return
            except ActionFailed as e:
                await open_switch.send('机器人发送消息失败：{}'.format(e.info['wording']))
                logger.exception('发送设置成功信息失败')
            except Exception as e:
                await open_switch.send('发生错误 {},请检查后台输出。'.format(e))
                logger.exception('设置简洁签到报告失败')
    except ActionFailed as e:
        await open_switch.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送开启自动签到信息失败')
    except Exception as e:
        await open_switch.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('开启自动签到失败')


# 关闭 自动签到 和 推送树脂提醒 功能
@close_switch.handle()
async def close_switch_func(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip().replace(
            ' ', '').replace('关闭', '')
        m = ''.join(re.findall('[\u4e00-\u9fa5]', message))

        qid = int(event.sender.user_id)
        at = re.search(r'\[CQ:at,qq=(\d*)]', message)

        if m == '自动签到':
            try:
                if at and qid in superusers:
                    qid = at.group(1)
                elif at and at.group(1) != qid:
                    await close_switch.send('你没有权限。', at_sender=True)
                    return
                else:
                    pass
                uid = await select_db(qid, mode='uid')
                im = await open_push(int(uid[0]), qid, 'off', 'StatusB')
                await close_switch.send(im, at_sender=True)
            except Exception:
                await close_switch.send('未绑定uid信息！', at_sender=True)
        elif m == '推送':
            try:
                if at and qid in superusers:
                    qid = at.group(1)
                elif at and at.group(1) != qid:
                    await close_switch.send('你没有权限。', at_sender=True)
                    return
                else:
                    pass
                uid = await select_db(qid, mode='uid')
                im = await open_push(int(uid[0]), qid, 'off', 'StatusA')
                await close_switch.send(im, at_sender=True)
            except Exception:
                await close_switch.send('未绑定uid信息！', at_sender=True)
        elif m == '自动米游币':
            try:
                if at and qid in superusers:
                    qid = at.group(1)
                elif at and at.group(1) != qid:
                    await close_switch.send('你没有权限。', at_sender=True)
                    return
                else:
                    pass
                uid = await select_db(qid, mode='uid')
                im = await open_push(int(uid[0]), qid, 'off', 'StatusC')
                await close_switch.send(im, at_sender=True)
            except Exception:
                await close_switch.send('未绑定uid信息！', at_sender=True)
        elif m == '简洁签到报告':
            try:
                if qid in superusers:
                    _ = await config_check('SignReportSimple', 'CLOSED')
                    await close_switch.send('成功!', at_sender=True)
                else:
                    return
            except ActionFailed as e:
                await close_switch.send('机器人发送消息失败：{}'.format(e.info['wording']))
                logger.exception('发送设置成功信息失败')
            except Exception as e:
                await close_switch.send('发生错误 {},请检查后台输出。'.format(e))
                logger.exception('设置简洁签到报告失败')
    except ActionFailed as e:
        await close_switch.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送开启自动签到信息失败')
    except Exception as e:
        await close_switch.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('关闭自动签到失败')


# 图片版信息
@get_genshin_info.handle()
async def send_genshin_info(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip().replace(
            ' ', '')
        qid = int(event.sender.user_id)
        uid = await select_db(qid, mode='uid')
        image = re.search(r'\[CQ:image,file=(.*),url=(.*)]', message)
        uid = uid[0]
        im = await draw_info_pic(uid, image)
        await get_genshin_info.send(MessageSegment.image(im), at_sender=True)
    except ActionFailed as e:
        await get_genshin_info.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送每月统计信息失败')
    except Exception:
        await get_genshin_info.send('未找到绑定信息', at_sender=True)
        logger.exception('获取/发送每月统计失败')


# 群聊内 每月统计 功能
@monthly_data.handle()
async def send_monthly_data(bot: Bot, event: MessageEvent):
    try:
        qid = int(event.sender.user_id)
        uid = await select_db(qid, mode='uid')
        uid = uid[0]
        im = await award(uid)
        await monthly_data.send(im, at_sender=True)
    except ActionFailed as e:
        await monthly_data.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送每月统计信息失败')
    except Exception:
        await monthly_data.send('未找到绑定信息', at_sender=True)
        logger.exception('获取/发送每月统计失败')


# 群聊内 签到 功能
@get_sign.handle()
async def get_sing_func(bot: Bot, event: MessageEvent):
    im = None
    try:
        qid = int(event.sender.user_id)
        uid = await select_db(qid, mode='uid')
        uid = uid[0]
        im = await sign(uid)
    except TypeError:
        im = '没有找到绑定信息。'
    except Exception as e:
        im = '发生错误 {},请检查后台输出。'.format(e)
        logger.exception('签到失败')
    finally:
        try:
            await get_sign.send(im, at_sender=True)
        except ActionFailed as e:
            await get_sign.send('机器人发送消息失败：{}'.format(e.info['wording']))
            logger.exception('发送签到信息失败')


@get_mihoyo_coin.handle()
async def send_mihoyo_coin(bot: Bot, event: MessageEvent):
    im = None
    await get_mihoyo_coin.send('开始操作……', at_sender=True)
    try:
        qid = int(event.sender.user_id)
        im_mes = await mihoyo_coin(qid)
        im = im_mes
    except TypeError or AttributeError:
        im = '没有找到绑定信息。'
        logger.exception('获取米游币失败')
    except Exception as e:
        im = '发生错误 {},请检查后台输出。'.format(e)
        logger.exception('获取米游币失败')
    finally:
        try:
            await get_mihoyo_coin.send(im, at_sender=True)
        except ActionFailed as e:
            await get_mihoyo_coin.send('机器人发送消息失败：{}'.format(e.info['wording']))
            logger.exception('发送签到信息失败')


# 群聊内 校验Cookies 是否正常的功能，不正常自动删掉
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


# 群聊内 查询当前树脂状态以及派遣状态 的命令
@daily_data.handle()
async def send_daily_data(bot: Bot, event: MessageEvent):
    try:
        uid = await select_db(int(event.sender.user_id), mode='uid')
        uid = uid[0]
        mes = await daily('ask', uid)
        im = mes[0]['message']
        await daily_data.send(im, at_sender=False)
    except TypeError:
        im = '没有找到绑定信息。'
        await daily_data.send(im, at_sender=True)
    except ActionFailed as e:
        await daily_data.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送当前状态信息失败')
    except Exception as e:
        await daily_data.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('查询当前状态错误')


# 群聊内 查询uid 的命令
@get_uid_info.handle()
async def send_uid_info(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip().replace(
            ' ', "").replace('uid', "")
        image = re.search(r"\[CQ:image,file=(.*),url=(.*)]", message)
        uid = re.findall(r"\d+", message)[0]  # str
        m = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        if m == '深渊':
            try:
                if len(re.findall(r'\d+', message)) == 2:
                    floor_num = re.findall(r'\d+', message)[1]
                    im = await draw_abyss_pic(uid, event.sender.nickname, floor_num, image)
                    if im.startswith('base64://'):
                        await get_uid_info.send(MessageSegment.image(im), at_sender=False)
                    else:
                        await get_uid_info.send(im, at_sender=False)
                else:
                    im = await draw_abyss0_pic(uid, event.sender.nickname, image)
                    if im.startswith('base64://'):
                        await get_uid_info.send(MessageSegment.image(im), at_sender=False)
                    else:
                        await get_uid_info.send(im, at_sender=False)
            except ActionFailed as e:
                await get_lots.send('机器人发送消息失败：{}'.format(e.info['wording']))
                logger.exception('发送uid深渊信息失败')
            except TypeError:
                await get_uid_info.send('获取失败，可能是Cookies失效或者未打开米游社角色详情开关。')
                logger.exception('深渊数据获取失败（Cookie失效/不公开信息）')
            except Exception as e:
                await get_uid_info.send('获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。'.format(e))
                logger.exception('深渊数据获取失败（数据状态问题）')
        elif m == '上期深渊':
            try:
                if len(re.findall(r'\d+', message)) == 2:
                    floor_num = re.findall(r'\d+', message)[1]
                    im = await draw_abyss_pic(uid, event.sender.nickname, floor_num, image, 2, '2')
                    if im.startswith('base64://'):
                        await get_uid_info.send(MessageSegment.image(im), at_sender=False)
                    else:
                        await get_uid_info.send(im, at_sender=False)
                else:
                    im = await draw_abyss0_pic(uid, event.sender.nickname, image, 2, '2')
                    if im.startswith('base64://'):
                        await get_uid_info.send(MessageSegment.image(im), at_sender=False)
                    else:
                        await get_uid_info.send(im, at_sender=False)
            except TypeError:
                await get_uid_info.send('获取失败，可能是Cookies失效或者未打开米游社角色详情开关。')
                logger.exception('上期深渊数据获取失败（Cookie失效/不公开信息）')
            except Exception as e:
                await get_uid_info.send('获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。'.format(e))
                logger.exception('上期深渊数据获取失败（数据状态问题）')
        else:
            try:
                im = await draw_pic(uid, event.sender.nickname, image, 2)
                if im.startswith('base64://'):
                    await get_uid_info.send(MessageSegment.image(im), at_sender=False)
                else:
                    await get_uid_info.send(im, at_sender=False)
            except ActionFailed as e:
                await get_lots.send('机器人发送消息失败：{}'.format(e.info['wording']))
                logger.exception('发送uid信息失败')
            except TypeError:
                await get_uid_info.send('获取失败，可能是Cookies失效或者未打开米游社角色详情开关。')
                logger.exception('数据获取失败（Cookie失效/不公开信息）')
            except Exception as e:
                await get_uid_info.send('获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。'.format(e))
                logger.exception('数据获取失败（数据状态问题）')
    except Exception as e:
        await get_uid_info.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('uid查询异常')


# 群聊内 绑定uid 的命令，会绑定至当前qq号上
@link_uid.handle()
async def link_uid_to_qq(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip().replace(
            ' ', '').replace('绑定uid', '')
        uid = re.findall(r'\d+', message)[0]  # str
        await connect_db(int(event.sender.user_id), uid)
        await link_uid.send('绑定uid成功！', at_sender=True)
    except ActionFailed as e:
        await link_uid.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送绑定信息失败')
    except Exception as e:
        await link_uid.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('绑定uid异常')


# 群聊内 绑定米游社通行证 的命令，会绑定至当前qq号上，和绑定uid不冲突，两者可以同时绑定
@link_mys.handle()
async def link_mihoyo_bbs_to_qq(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip().replace(
            ' ', '').replace('绑定mys', '')
        mys = re.findall(r'\d+', message)[0]  # str
        await connect_db(int(event.sender.user_id), None, mys)
        await link_mys.send('绑定米游社id成功！', at_sender=True)
    except ActionFailed as e:
        await link_mys.send('机器人发送消息失败：{}'.format(e.info['wording']))
        logger.exception('发送绑定信息失败')
    except Exception as e:
        await link_mys.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('绑定米游社通行证异常')


# 群聊内 绑定过uid/mysid的情况下，可以查询，默认优先调用米游社通行证，多出世界等级一个参数
@search.handle()
async def get_info(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip().replace(
            ' ', '').replace('查询', '')
        image = re.search(r'\[CQ:image,file=(.*),url=(.*)]', message)
        at = re.search(r'\[CQ:at,qq=(\d*)]', message)
        if at:
            qid = at.group(1)
            mi = await bot.call_api('get_group_member_info', **{'group_id': event.group_id, 'user_id': qid})
            nickname = mi['nickname']
            uid = await select_db(qid)
            message = message.replace(at.group(0), '')
        else:
            nickname = event.sender.nickname
            uid = await select_db(int(event.sender.user_id))

        m = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        if uid:
            if m == '深渊':
                try:
                    if len(re.findall(r'\d+', message)) == 1:
                        floor_num = re.findall(r'\d+', message)[0]
                        im = await draw_abyss_pic(uid[0], nickname, floor_num, image, uid[1])
                        if im.startswith('base64://'):
                            await search.send(MessageSegment.image(im), at_sender=False)
                        else:
                            await search.send(im, at_sender=False)
                    else:
                        im = await draw_abyss0_pic(uid[0], nickname, image, uid[1])
                        if im.startswith('base64://'):
                            await search.send(MessageSegment.image(im), at_sender=False)
                        else:
                            await search.send(im, at_sender=False)
                except ActionFailed as e:
                    await search.send('机器人发送消息失败：{}'.format(e.info['wording']))
                    logger.exception('发送uid深渊信息失败')
                except (TypeError, IndexError):
                    await search.send('获取失败，可能是Cookies失效或者未打开米游社角色详情开关。')
                    logger.exception('深渊数据获取失败（Cookie失效/不公开信息）')
                except Exception:
                    await search.send('获取失败，请检查 cookie 及网络状态。')
                    logger.exception('深渊数据获取失败（数据状态问题）')
            elif m == '上期深渊':
                try:
                    if len(re.findall(r'\d+', message)) == 1:
                        floor_num = re.findall(r'\d+', message)[0]
                        im = await draw_abyss_pic(uid[0], nickname, floor_num, image, uid[1], '2')
                        if im.startswith('base64://'):
                            await search.send(MessageSegment.image(im), at_sender=False)
                        else:
                            await search.send(im, at_sender=False)
                    else:
                        im = await draw_abyss0_pic(uid[0], nickname, image, uid[1], '2')
                        if im.startswith('base64://'):
                            await search.send(MessageSegment.image(im), at_sender=False)
                        else:
                            await search.send(im, at_sender=False)
                except ActionFailed as e:
                    await search.send('机器人发送消息失败：{}'.format(e.info['wording']))
                    logger.exception('发送uid上期深渊信息失败')
                except (TypeError, IndexError):
                    await search.send('获取失败，可能是Cookies失效或者未打开米游社角色详情开关。')
                    logger.exception('上期深渊数据获取失败（Cookie失效/不公开信息）')
                except Exception as e:
                    await search.send('获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。'.format(e))
                    logger.exception('上期深渊数据获取失败（数据状态问题）')
            elif m == '词云':
                try:
                    im = await draw_word_cloud(uid[0], image, uid[1])
                    if im.startswith('base64://'):
                        await search.send(MessageSegment.image(im), at_sender=False)
                    else:
                        await search.send(im, at_sender=False)
                except ActionFailed as e:
                    await search.send('机器人发送消息失败：{}'.format(e.info['wording']))
                    logger.exception('发送uid词云信息失败')
                except (TypeError, IndexError):
                    await search.send('获取失败，可能是Cookies失效或者未打开米游社角色详情开关。')
                    logger.exception('词云数据获取失败（Cookie失效/不公开信息）')
                except Exception as e:
                    await search.send('获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。'.format(e))
                    logger.exception('词云数据获取失败（数据状态问题）')
            elif m == '':
                try:
                    im = await draw_pic(uid[0], nickname, image, uid[1])
                    if im.startswith('base64://'):
                        await search.send(MessageSegment.image(im), at_sender=False)
                    else:
                        await search.send(im, at_sender=False)
                except ActionFailed as e:
                    await search.send('机器人发送消息失败：{}'.format(e.info['wording']))
                    logger.exception('发送uid信息失败')
                except (TypeError, IndexError):
                    await search.send('获取失败，可能是Cookies失效或者未打开米游社角色详情开关。')
                    logger.exception('uid数据获取失败（Cookie失效/不公开信息）')
                except Exception as e:
                    await search.send('获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。'.format(e))
                    logger.exception('数据获取失败（数据状态问题）')
            else:
                pass
        else:
            await search.send('未找到绑定记录！')
    except Exception as e:
        await search.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('查询异常')


# 群聊内 查询米游社通行证 的命令
@get_mys_info.handle()
async def send_mihoyo_bbs_info(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip().replace(
            ' ', '').replace('mys', '')
        image = re.search(r'\[CQ:image,file=(.*),url=(.*)]', message)
        uid = re.findall(r'\d+', message)[0]  # str
        m = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        if m == '深渊':
            try:
                if len(re.findall(r'\d+', message)) == 2:
                    floor_num = re.findall(r'\d+', message)[1]
                    im = await draw_abyss_pic(uid, event.sender.nickname, floor_num, image, 3)
                    if im.startswith("base64://"):
                        await get_mys_info.send(MessageSegment.image(im), at_sender=False)
                    else:
                        await get_mys_info.send(im, at_sender=False)
                else:
                    im = await draw_abyss0_pic(uid, event.sender.nickname, image, 3)
                    if im.startswith("base64://"):
                        await get_mys_info.send(MessageSegment.image(im), at_sender=False)
                    else:
                        await get_mys_info.send(im, at_sender=False)
            except ActionFailed as e:
                await get_mys_info.send('机器人发送消息失败：{}'.format(e.info['wording']))
                logger.exception('发送米游社深渊信息失败')
            except (TypeError, IndexError):
                await get_mys_info.send('获取失败，可能是Cookies失效或者未打开米游社角色详情开关。')
                logger.exception('深渊数据获取失败（Cookie失效/不公开信息）')
            except Exception as e:
                await get_mys_info.send('获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。'.format(e))
                logger.exception('深渊数据获取失败（数据状态问题）')
        elif m == '上期深渊':
            try:
                if len(re.findall(r'\d+', message)) == 1:
                    floor_num = re.findall(r'\d+', message)[0]
                    im = await draw_abyss_pic(uid, event.sender.nickname, floor_num, image, 3, '2')
                    if im.startswith('base64://'):
                        await get_mys_info.send(MessageSegment.image(im), at_sender=False)
                    else:
                        await get_mys_info.send(im, at_sender=False)
                else:
                    im = await draw_abyss0_pic(uid, event.sender.nickname, image, 3, '2')
                    if im.startswith('base64://'):
                        await get_mys_info.send(MessageSegment.image(im), at_sender=False)
                    else:
                        await get_mys_info.send(im, at_sender=False)
            except ActionFailed as e:
                await get_mys_info.send('机器人发送消息失败：{}'.format(e.info['wording']))
                logger.exception('发送uid上期深渊信息失败')
            except (TypeError, IndexError):
                await get_mys_info.send('获取失败，可能是Cookies失效或者未打开米游社角色详情开关。')
                logger.exception('上期深渊数据获取失败（Cookie失效/不公开信息）')
            except Exception as e:
                await get_mys_info.send('获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。'.format(e))
                logger.exception('上期深渊数据获取失败（数据状态问题）')
        else:
            try:
                im = await draw_pic(uid, event.sender.nickname, image, 3)
                if im.startswith('base64://'):
                    await get_mys_info.send(MessageSegment.image(im), at_sender=False)
                else:
                    await get_mys_info.send(im, at_sender=False)
            except ActionFailed as e:
                await get_mys_info.send('机器人发送消息失败：{}'.format(e.info['wording']))
                logger.exception('发送米游社信息失败')
            except (TypeError, IndexError):
                await get_mys_info.send('获取失败，可能是Cookies失效或者未打开米游社角色详情开关。')
                logger.exception('米游社数据获取失败（Cookie失效/不公开信息）')
            except Exception as e:
                await get_mys_info.send('获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。'.format(e))
                logger.exception('米游社数据获取失败（数据状态问题）')
    except Exception as e:
        await get_mys_info.send('发生错误 {},请检查后台输出。'.format(e))
        logger.exception('米游社查询异常')


@all_genshinsign_recheck.handle()
async def genshin_resign(bot: Bot):
    await all_genshinsign_recheck.send('已开始执行')
    await sign_at_night()


@all_bbscoin_recheck.handle()
async def bbscoin_resign(bot: Bot, event: MessageEvent):
    await all_bbscoin_recheck.send('已开始执行')
    await daily_mihoyo_bbs_sign()
