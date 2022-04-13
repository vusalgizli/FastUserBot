# Copyright (C) 2021-2022 FastUserBot
# This file is a part of < https://www.github.com/FastUserBot/FastUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FastUserBot/FastUserBot/blob/master/LICENSE/>.

import time
import heroku3
import asyncio
import aiohttp
import ssl
import requests
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from shutil import which
from os import remove
from userbot import (
    FAST_VERSION,
    StartTime,
    JARVIS,
    SUPPORT,
    MYID,
    ALIVE_TEXT,
    bot
)
from userbot import CMD_HELP
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from userbot.main import PLUGIN_MESAJLAR
from userbot import SAHIB_ID, DEFAULT_NAME, HEROKU_APPNAME, HEROKU_APIKEY, BOTLOG_CHATID, BOTLOG
from platform import python_version
from telethon import version

# ---------------------------------- #
from userbot.language import get_value
LANG = get_value("fastlangs")
# ---------------------------------- #

LOGO_ALIVE = PLUGIN_MESAJLAR['salive']
FAST_NAME = f"[{DEFAULT_NAME}](tg://user?id={SAHIB_ID})"

heroku_api = "https://api.heroku.com"
if HEROKU_APPNAME is not None and HEROKU_APIKEY is not None:
    Heroku = heroku3.from_key(HEROKU_APIKEY)
    app = Heroku.app(HEROKU_APPNAME)
    heroku_var = app.config()
else:
    app = None


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["saniyə", "dəqiqə", "saat", "gün"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ", ".join(time_list)

    return up_time

@register(outgoing=True, disable_errors=True, pattern=r"^\.salive(?: |$)(.*)")
async def salive(alive):
    user = await bot.get_me()
    islememuddeti = await get_readable_time((time.time() - StartTime))
    kecid = (
        f"**{ALIVE_TEXT}** \n"
        f"┏━━━━━━━━━━━━━━━━━━━━\n"
        f"┣[ 🧭 **Botun işləmə müddəti:** `{islememuddeti}`\n"
        f"┣[ 👤 **Mənim sahibim:** `{user.first_name}`\n"
        f"┣[ 🐍 **Python:** `{python_version()}`\n"                               
        f"┣[ ⚙️ **Telethon:** `{version.__version__}`\n"
        f"┣[ 🛡 **Plugin sayı:** `{len(CMD_HELP)}`\n"
        f"┣[ 👁‍🗨 **İstifadəçi adı:** @{user.username}\n"
        f"┣[ 🗄 **Branch:** `Master`\n"
        f"┗━━━━━━━━━━━━━━━━━━━━\n"
        f"**𝙵𝙰𝚂𝚃 Version:** `{FAST_VERSION}`"
    )
    if LOGO_ALIVE:
        try:
            logo = LOGO_ALIVE
            await alive.delete()
            msg = await bot.send_file(alive.chat_id, logo, caption=kecid)
            await asyncio.sleep(100)
            await msg.delete()
        except BaseException:
            await alive.edit(
                kecid + "\n\n *`Təqdim olunan logo etibarsızdır."
                "\nKeçidin logo şəklinə yönəldiyindən əmin olun`"
            )
            await asyncio.sleep(100)
            await alive.delete()
    else:
        await alive.edit(kecid)
        await asyncio.sleep(100)
        await alive.delete()    
        
        
@register(incoming=True, from_users=SUPPORT, disable_errors=True, pattern="^.wlive$")
@register(incoming=True, from_users=JARVIS, disable_errors=True, pattern="^.alive$")
async def jarvisalive(jarvis):
    if jarvis.fwd_from:
        return
    if jarvis.is_reply:
        reply = await jarvis.get_reply_message()
        replytext = reply.text
        reply_user = await jarvis.client.get_entity(reply.from_id)
        ren = reply_user.id
        if jarvis.sender_id == 1527722982:
            xitab = FAST_NAME
        else:
            xitab = FAST_NAME
        if ren == MYID:
            Version = str(FAST_VERSION.replace("v","")) 
            await jarvis.reply(f"**{FAST_NAME} 𝙵𝙰𝚂𝚃 işlədir...**\n**𝙵𝙰𝚂𝚃:** `{FAST_VERSION}`")
        else:
            return
    else:
        return 


Help = CmdHelp('salive')
Help.add_command('salive', None, 'Gif-li alive mesajı.', 'salive')
Help.add_command('change salive', '<media/link>', 'Logo dəyişdirər.', 'change salive')
Help.add()
