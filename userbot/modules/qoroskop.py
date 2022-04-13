# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import pyaztro

from userbot.events import register
from userbot.cmdhelp import CmdHelp

CYBER = ""

@register(outgoing=True, disable_errors=True, pattern=r"^\.qoroskop (.*)")
async def cyber(e):
    await e.edit("Məlumatlar hazırlanır..\nBu biraz vaxt apara bilər.")
    if not e.pattern_match.group(1):
        x = CYBER
        if not x:
            await e.edit("Bağışlayın, heçnə tapa bilmədim.")
            return
    else:
        x = e.pattern_match.group(1)
    horoscope = pyaztro.Aztro(sign=x)
    mood = horoscope.mood
    lt = horoscope.lucky_time
    desc = horoscope.description
    col = horoscope.color
    com = horoscope.compatibility
    ln = horoscope.lucky_number

    result = (
        f"**`{x}`** üçün məlumat:\n"
        f"**Mood :** `{mood}`\n"
        f"**Şanslı vaxt :** `{lt}`\n"
        f"**Şanslı rəng :** `{col}`\n"
        f"**Şanslı rəqəm :** `{ln}`\n"
        f"**Uyğunluq :** `{com}`\n"
        f"**Haqqında :** `{desc}`\n"
    )

    await e.edit(result)


Help = CmdHelp('qoroskop')
Help.add_command('qoroskop', None, 'Yazdığınız bürc haqqında məlumat verər.')
Help.add_info('Qeyd: Bürc adları İngilis dilində yazılmalıdır. Bürclərin siyahısı: https://t.me/TheCyberSupport/11400')
Help.add()   
