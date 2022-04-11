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

# 米游社查询个人信息
get_uid_info = on_startswith("#uid", priority=priority)
get_mys_info = on_startswith("#mys", priority=priority)
search = on_command("查询", priority=priority)


"""
查询uid 的命令
"""

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
                await get_uid_info.send('机器人发送消息失败：{}'.format(e.info['wording']))
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
                await get_uid_info.send('机器人发送消息失败：{}'.format(e.info['wording']))
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


"""
查询米游社通行证 的命令
"""

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


"""
绑定过uid/mysid的情况下，可以查询，默认优先调用米游社通行证，多出世界等级一个参数
"""

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