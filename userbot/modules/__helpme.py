# Copyright (C) 2021-2022 FastUserBot
# This file is a part of < https://github.com/FastUserbBot/FastUserBot/ >
# PLease read the GNU General Public License v3.0 in
# <https://github.com/FastUserbBot/FastUserBot/blob/master/LICENSE/>.

# Thanks @Spechide.

from userbot import BOT_USERNAME
from userbot.events import register

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("__helpme")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.yard[iı]m|^.help")
async def help(event):
    tgbotusername = BOT_USERNAME
    if tgbotusername is not None:
        results = await event.client.inline_query(
            tgbotusername,
            "@FastUserRobot"
        )
        await results[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        )
        await event.delete()
    else:
        await event.edit(LANG["NO_BOT"])
