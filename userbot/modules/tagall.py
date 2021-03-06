# Copyright (C) 2021-2022 FastUserBot
# This file is a part of < https://www.github.com/FastUserBot/FastUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FastUserBot/FastUserBot/blob/master/LICENSE/>.

from telethon.tl.types import ChannelParticipantsAdmins

from userbot.events import register as fast
from userbot.cmdhelp import CmdHelp
from userbot import bot


@fast(outgoing=True, pattern="^.tagall ?(.*)$")
async def _(event):
    if event.fwd_from:
        return
    mentions = event.pattern_match.group(1)
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, 100):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    await event.reply(mentions)
    await event.delete()


@fast(outgoing=True, pattern="^.admin ?(.*)$")
async def _(event):
    if event.fwd_from:
        return
    mentions = "Adminlər: "
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()

CmdHelp('tags').add_command(
    'tagall', '<səbəb>', 'Bir mesajda 100 istifadəçini etiketləyər (Maksimum 100)'
).add_command(
    'admin', '<səbəb>', 'Qrupdaki adminləri bir mesajda etiketləyər.'
).add_command(
    'tag', '<səbəb>', 'Qrupdaki istifadəçiləri bir-bir etiketləyər. (Maksimum 500)'
).add_command(
    'alladmin', '<səbəb>', 'Qrupdaki adminləri bir mesajda etiketləyər.'
).add_command(
    'stop', None, 'Tag etməni dayandırar.'
).add_command(
    'taglimit', '<rəqəm>', 'Tag limiti ayarlayın'
).add()
