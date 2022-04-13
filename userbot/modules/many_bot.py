# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import os
from telethon.tl.functions.contacts import UnblockRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.events import register
from userbot.cmdhelp import CmdHelp

chat = "@manybot"

@register(outgoing=True, pattern="^.manybot ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1):
        text = event.pattern_match.group(1)
        
    else:
        await event.edit("`Bir bot tokeni qeyd edin!!`")
        return

    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("/addbot")
            audio = await conv.get_response()
            await conv.send_message(text)
            audio = await conv.get_response()
            await event.client.forward_messages(event.chat_id, audio)
            await event.delete()
        except YouBlockedUserError:
            await event.client(UnblockRequest("74376339"))
            await conv.send_message("/addbot")
            audio = await conv.get_response()
            await conv.send_message(text)
            audio = await conv.get_response()
            await conv.send_message("/skip")
            await event.client.forward_messages(event.chat_id, audio)
            await event.delete()

add_ = CmdHelp('manybot')
add_.add_command("manybot", "<bot_token>", "@Manybot ilə botunuzu yaradın.").add()
