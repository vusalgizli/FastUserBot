# Copyright (C) 2021-2022 FastUserBot
# AY UÇAN QUŞLAR

import os
import requests
from userbot import bot, BLACKLIST_CHAT
from userbot.events import register
from userbot.cmdhelp import CmdHelp

# ---------------------------------- #

from userbot.language import get_value
LANG = get_value("fastlangs")

# ---------------------------------- #


# ------------------------------------------------------ #
#FAST_AI_DE = sb(os.environ.get("FAST_AI_DE", "False"))#
FAST_AI_KEY = "82cb8992-fe1e-4924-8299-7f55dd6e40c3"    
# ------------------------------------------------------ #

@register(fast=True, pattern=r"^\.scan(?: |$)(.*)")
@register(fast=True, pattern=r"^\.detect(?: |$)(.*)")
async def detect(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await event.edit(LANG["PROHIBITED_COMMAND"])
    reply = await event.get_reply_message()
    if not reply:
        return await event.edit("`Xahiş edirəm bir mediaya cavab verin!`")
    fast = await event.edit("`Fayl endirilir...`")
    media = await event.client.download_media(reply)
    fast2 = await event.edit("`Media skan edilir...`")
    r = requests.post(
        "https://api.deepai.org/api/nsfw-detector",
        files={
            "image": open(media, "rb"),
        },
        headers={"api-key": FAST_AI_KEY},
    )
    os.remove(media)
    if "status" in r.json():
        return await event.edit(r.json()["status"])
    r_json = r.json()["output"]
    pic_id = r.json()["id"]
    percentage = r_json["nsfw_score"] * 100
    detections = r_json["detections"]
    link = f"https://api.deepai.org/job-view-file/{pic_id}/inputs/image.jpg"
    netice = f"<b>Medianın 18+ olma faizi hesablandı:</b>\n<a href='{link}'>>>></a> <code>{percentage:.3f}%</code>\n\n"
    if detections:
        for parts in detections:
            name = parts["name"]
            confidence = int(float(parts["confidence"]) * 100)
            netice += f"<b>• {name}:</b>\n   <code>{confidence} %</code>\n"
    await bot.send_message(
        event.chat_id,
        netice,
        link_preview=False,
        parse_mode="HTML",
    )


Help = CmdHelp('deepai')
Help.add_command('detect', '<Bir mediaya cavab>', 'Cavab verdiyiniz medianın 18+ məzmun olub olmadığını aşkar etmək üçün.')
Help.add_info('@FastUserBot')
Help.add() 
