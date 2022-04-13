# Copyright (C) 2021-2022 FastUserBot
# This file is a part of < https://www.github.com/FastUserBot/FastUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FastUserBot/FastUserBot/blob/master/LICENSE/>.

import asyncio
from telethon import events
from userbot import SUDO_ID, SUDO_VERSION, FAST_VERSION
from userbot.cmdhelp import CmdHelp
from userbot.events import register

@register(sudo=True, pattern="^.calive$")
async def sudoers(s):
    await s.client.send_message(s.chat_id,f"`𝙵𝙰𝚂𝚃 USERBOT\nSudo aktivdir...\n𝙵𝙰𝚂𝚃 Version: {FAST_VERSION}\nSudo Version: {SUDO_VERSION}`")
    
Help = CmdHelp('calive')
Help.add_command('calive', None, 'Sudo aktiv olub olmadığını yoxlamaq üçün.')
Help.add()
