# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import re
import asyncio
from userbot import CMD_HELP, ASYNC_POOL, GALERI_SURE
from userbot.events import register
from userbot.main import FotoDegistir
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("galeri")

# ████████████████████████████████ #

URL_REGEX = re.compile(
    # https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

@register(outgoing=True, pattern="^.qalareya ?(.*)")
@register(outgoing=True, pattern="^.galeri ?(.*)")
async def qalareya(event):
    try:
        import userbot.modules.sql_helper.galeri_sql as sql
    except:
        await event.edit("`SQL dışı mod'da qaleri işləməz!`")
    secenek = event.pattern_match.group(1)
    secen = secenek.split(" ")
    if secen[0] == "elave":
        if len(secen) > 1:
            URL = re.search(URL_REGEX, secen[1])
            if URL != None:
                sql.ekle_foto(secen[1])
                sql.getir_foto()
                await event.edit(LANG['ADDED_LIST'])
            else:
                await event.edit(LANG['INVALID_URL'])
        else:
            await event.edit(LANG['EXAMPLE'])
    elif secen[0] == "list":
        yfoto = ""
        sql.getir_foto()
        fotolar = sql.TUM_GALERI
        for foto in fotolar:
            yfoto += f"\n▶️ ({foto.g_id}) [Fotoğraf]({foto.foto})"
        await event.edit(f"**{LANG['LIST']}**\n" + yfoto)
    elif secen[0] == "sil":
        if secen[1].isdigit():
            silme = sql.sil_foto(secen[1])
            if silme == True:
                await event.edit(LANG['REMOVED'])
            else:
                await event.edit(f"{LANG['REMOVED_ERROR']}: {silme}")
        else:
            await event.edit(f"**{LANG['NEED_NUMBER']}** `.qalareya sil 2`")
    elif secen[0] == "başla":
        if "qalareya" in ASYNC_POOL:
            await event.edit(LANG['WORKING'])
            return
        ASYNC_POOL.append("qalareya")
        sql.getir_foto()
        await event.edit(LANG['STARTED'])
        if len(sql.TUM_GALERI) >= 1:
            while "qalareya" in ASYNC_POOL:
                fotolar = sql.TUM_GALERI
                i = 0
                while i < len(fotolar):
                    if "qalareya" not in ASYNC_POOL:
                        break
                    if i == len(fotolar):
                        i = 0
                    await FotoDegistir(i)
                    await asyncio.sleep(GALERI_SURE)
                    i += 1
        else:
            await event.edit(LANG['NEED_PHOTO'])
            return
    elif secen[0] == "bagla":
        if "qalareya" in ASYNC_POOL:
            ASYNC_POOL.remove("qalareya")
            await event.edit(LANG['STOPPED'])
        else:
            event.edit(LANG['ALREADY_STOP'])
        return
    else:
        await event.edit(LANG['INVALID'])
        

CmdHelp('qalareya').add_command(
    'qalareya elave', '<url>', 'Qaleri sırasına foto əlavə edər', 'qalareya elave https://i.hizliresim.com/cyber.jpg'
).add_command(
    'qalareya list', None, 'Qaleri sırasını göstərir.'
).add_command(
    'qalareya sil', '<sayı>', 'Qaleri sırasından bir fotonu silər.', 'qalareya sil 4'
).add()
