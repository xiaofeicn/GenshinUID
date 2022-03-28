import asyncio, os, sys, re

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

search = on_command("查询", permission=GROUP, priority=priority)
get_sign = on_command("签到", priority=priority)
get_mihoyo_coin = on_command("开始获取米游币", priority=priority)
check = on_command("校验全部Cookies", permission=SUPERUSER, priority=priority)
monthly_data = on_command("每月统计", priority=priority)
daily_data = on_command("当前状态", priority=priority)
open_switch = on_startswith("开启", priority=priority)
close_switch = on_startswith("关闭", priority=priority)
all_genshinsign_recheck = on_command("全部重签", permission=SUPERUSER, priority=priority)
all_bbscoin_recheck = on_command("全部重获取", permission=SUPERUSER, priority=priority)

"""
签到 功能
"""


@get_sign.handle()
async def get_sing_func(bot: Bot, event: MessageEvent):
    try:
        qid = int(event.sender.user_id)
        uid = await select_db(qid, mode="uid")
        uid = uid[0]
        im = await sign(uid)
    except TypeError:
        im = "没有找到绑定信息。"
    except Exception as e:
        im = "发生错误 {},请检查后台输出。".format(e)
        logger.exception("签到失败")
    finally:
        try:
            await get_sign.send(im, at_sender=True)
        except ActionFailed as e:
            await get_sign.send("机器人发送消息失败：{}".format(e.info['wording']))
            logger.exception("发送签到信息失败")


"""
每月统计 功能
"""


@monthly_data.handle()
async def send_monthly_data(bot: Bot, event: MessageEvent):
    try:
        qid = int(event.sender.user_id)
        uid = await select_db(qid, mode="uid")
        uid = uid[0]
        im = await award(uid)
        await monthly_data.send(im, at_sender=True)
    except ActionFailed as e:
        await monthly_data.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送每月统计信息失败")
    except Exception:
        await monthly_data.send('未找到绑定信息', at_sender=True)
        logger.exception("获取/发送每月统计失败")


"""
查询当前树脂状态以及派遣状态 功能
"""


@daily_data.handle()
async def send_daily_data(bot: Bot, event: MessageEvent):
    try:
        uid = await select_db(int(event.sender.user_id), mode="uid")
        uid = uid[0]
        mes = await daily("ask", uid)
        im = mes[0]['message']
        await daily_data.send(im, at_sender=True)
    except TypeError:
        im = "没有找到绑定信息。"
        await daily_data.send(im, at_sender=True)
    except ActionFailed as e:
        await daily_data.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送当前状态信息失败")
    except Exception as e:
        await daily_data.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("查询当前状态错误")


"""
开启 自动签到 和 推送树脂提醒 功能
"""


@open_switch.handle()
async def open_switch_func(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip().replace(
            ' ', "").replace('开启', "")
        m = ''.join(re.findall('[\u4e00-\u9fa5]', message))

        qid = int(event.sender.user_id)
        at = re.search(r"\[CQ:at,qq=(\d*)]", message)

        if m == "自动签到":
            try:
                if at and qid in superusers:
                    qid = at.group(1)
                elif at and at.group(1) != qid:
                    await close_switch.send("你没有权限。", at_sender=True)
                    return
                else:
                    pass
                gid = event.get_session_id().split("_")[1] if len(
                    event.get_session_id().split("_")) == 3 else "on"
                uid = await select_db(qid, mode="uid")
                im = await open_push(int(uid[0]), qid, str(gid), "StatusB")
                await open_switch.send(im, at_sender=True)
            except Exception:
                await open_switch.send("未绑定uid信息！", at_sender=True)
        elif m == "推送":
            try:
                if at and qid in superusers:
                    qid = at.group(1)
                elif at and at.group(1) != qid:
                    await close_switch.send("你没有权限。", at_sender=True)
                    return
                else:
                    pass
                gid = event.get_session_id().split("_")[1] if len(
                    event.get_session_id().split("_")) == 3 else "on"
                uid = await select_db(qid, mode="uid")
                im = await open_push(int(uid[0]), qid, str(gid), "StatusA")
                await open_switch.send(im, at_sender=True)
            except Exception:
                await open_switch.send("未绑定uid信息！", at_sender=True)
        elif m == "简洁签到报告":
            try:
                if qid in superusers:
                    _ = await config_check("SignReportSimple", "OPEN")
                    await open_switch.send("成功!", at_sender=True)
                else:
                    return
            except ActionFailed as e:
                await open_switch.send("机器人发送消息失败：{}".format(e.info['wording']))
                logger.exception("发送设置成功信息失败")
            except Exception as e:
                await open_switch.send("发生错误 {},请检查后台输出。".format(e))
                logger.exception("设置简洁签到报告失败")
    except ActionFailed as e:
        await open_switch.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送开启自动签到信息失败")
    except Exception as e:
        await open_switch.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("开启自动签到失败")


"""
关闭 自动签到 和 推送树脂提醒 功能
"""


@close_switch.handle()
async def close_switch_func(bot: Bot, event: MessageEvent):
    try:
        message = str(event.get_message()).strip().replace(
            ' ', "").replace('关闭', "")
        m = ''.join(re.findall('[\u4e00-\u9fa5]', message))

        qid = int(event.sender.user_id)
        at = re.search(r"\[CQ:at,qq=(\d*)]", message)

        if m == "自动签到":
            try:
                if at and qid in superusers:
                    qid = at.group(1)
                elif at and at.group(1) != qid:
                    await close_switch.send("你没有权限。", at_sender=True)
                    return
                else:
                    pass
                uid = await select_db(qid, mode="uid")
                im = await open_push(int(uid[0]), qid, "off", "StatusB")
                await close_switch.send(im, at_sender=True)
            except Exception:
                await close_switch.send("未绑定uid信息！", at_sender=True)
        elif m == "推送":
            try:
                if at and qid in superusers:
                    qid = at.group(1)
                elif at and at.group(1) != qid:
                    await close_switch.send("你没有权限。", at_sender=True)
                    return
                else:
                    pass
                uid = await select_db(qid, mode="uid")
                im = await open_push(int(uid[0]), qid, "off", "StatusA")
                await close_switch.send(im, at_sender=True)
            except Exception:
                await close_switch.send("未绑定uid信息！", at_sender=True)
        elif m == "简洁签到报告":
            try:
                if qid in superusers:
                    _ = await config_check("SignReportSimple", "CLOSED")
                    await close_switch.send("成功!", at_sender=True)
                else:
                    return
            except ActionFailed as e:
                await close_switch.send("机器人发送消息失败：{}".format(e.info['wording']))
                logger.exception("发送设置成功信息失败")
            except Exception as e:
                await open_switch.send("发生错误 {},请检查后台输出。".format(e))
                logger.exception("设置简洁签到报告失败")
    except ActionFailed as e:
        await close_switch.send("机器人发送消息失败：{}".format(e.info['wording']))
        logger.exception("发送开启自动签到信息失败")
    except Exception as e:
        await close_switch.send("发生错误 {},请检查后台输出。".format(e))
        logger.exception("关闭自动签到失败")


"""
全部签到
"""


@all_genshinsign_recheck.handle()
async def genshin_resign(bot: Bot):
    await all_genshinsign_recheck.send("已开始执行")
    from GenshinUID.mihoyo_bot_feature.bot_cron import sign_at_night
    await sign_at_night()

@all_bbscoin_recheck.handle()
async def bbscoin_resign(bot:Bot, event: MessageEvent):
    await all_bbscoin_recheck.send("已开始执行")
    from GenshinUID.mihoyo_bot_feature.bot_cron import daily_mihoyo_bbs_sign
    await daily_mihoyo_bbs_sign()