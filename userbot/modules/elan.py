# Copyright (C) 2021-2022 FastUserBot
# This file is a part of < https://www.github.com/FastUserBot/FastUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FastUserBot/FastUserBot/blob/master/LICENSE/>.

# CODER tg/@FUSUF github/@Quiec #
# PLEASE DON'T DELETE THIS LINES (IF YOU KANG) #

from telethon import events
from userbot.cmdhelp import CmdHelp
import asyncio
from userbot.events import register


@register(outgoing=True, pattern="^.elan ?(.*)")
@register(outgoing=True, pattern="^.duyuru ?(.*)")
async def elan(event):
    mesaj = event.pattern_match.group(1)
    if len(mesaj) < 1:
        await event.edit("`Elan üçün bir mesaj vermelisiz. Məsələn: ``.elan Salam Dünya`")
        return

    if event.is_private:
        await event.edit("`Bu əmr sadəcə qruplarda işləyir.`")
        return

    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await event.edit("`Ciddisən? Admin olmadığın bir qrupda elan göndərməyivə icazə verməyəcəm!`")
        return

    await event.edit("`Bütün istifadəçilərivizə elan göndərilir...`")
    all_participants = await event.client.get_participants(event.chat_id, aggressive=True)
    a = 0

    for user in all_participants:
        a += 1
        uid = user.id
        if user.username:
            link = "@" + user.username
        else:
            link = "[" + user.first_name + "](" + str(user.id) + ")"
        try:
            await event.client.send_message(uid, mesaj + "\n\n@FastSupp ilə göndərildi.")
            son = f"**Son elan göndərilən istifadəçi:** {link}"
        except:
            son = f"**Son elan göndərilən istifadəçi:** **Göndərilə bilmədi!**"
    
        await event.edit(f"`Bütün istifadəçilərivizə elan göndərilir...`\n{son}\n\n**Status:** `{a}/{len(all_participants)}`")
        await asyncio.sleep(0.5)

    await event.edit("`Bütün istifadəçilərinizə elan göndərildi!`")

    
Help = CmdHelp('elan')
Help.add_command('elan', '<admin və ya sahibi olduğunuz qrupda yazın>', 'Admini və ya sahibi olduğunuz qrupda yazdığınız mesajı istifadəçilərə göndərər.')
Help.add_info('@FastSupp')
Help.add()    
