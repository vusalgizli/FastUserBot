# Copyright (C) 2021-2022 FastUserBot
# This file is a part of < https://github.com/FastUserbBot/FastUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://github.com/FastUserbBot/FastUserBot/blob/master/LICENSE/>.

from userbot.cmdhelp import CmdHelp
from userbot import cmdhelp
from userbot import CMD_HELP, FAST_EMOJI
from userbot.events import register

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("__fast")

# ████████████████████████████████ #

@register(fast=True, pattern="^.fast(?: |$)(.*)")
async def fast(event):
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit(LANG["NEED_PLUGIN"])
    else:
        string = ""
        sayfa = [sorted(list(CMD_HELP))[i:i + 5] for i in range(0, len(sorted(list(CMD_HELP))), 5)]
        
        for i in sayfa:
            string += f'{FAST_EMOJI} '
            for sira, a in enumerate(i):
                string += "`" + str(a)
                if sira == i.index(i[-1]):
                    string += "`"
                else:
                    string += "`, "
            string += "\n"
        await event.edit(LANG["NEED_MODULE"] + '\n\n' + string)
