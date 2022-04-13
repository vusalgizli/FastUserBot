# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern=".stick ?(.*)")
async def stick(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Zəhmət olmasa bir şəkilə cavab verin`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`Sadəcə və sadəcə şəkilləri ver.`")
        return
    chat = "@BuildStickerBot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("Botlardan olan mesajları qəbul edə bilmirəm!")
        return
    asc = await event.edit("`Stickerə çevrirəm...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=164977173)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit("@BuildStickerBot'u `blokdan çıxardın və bir daha yenidən yoxlayın`")
            return
        if response.text.startswith("Forward"):
            await event.edit(
                "Gizlilik ayarlarınızı gözdən keçirdin."
            )
        else:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
                caption=f"@TheCyberUserBot ilə stickerə çevrildi",
            )
            await event.client.send_read_acknowledge(conv.chat_id)

@register(outgoing=True, pattern=".tweet ?(.*)")
async def tweet(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Bir yazıya cavab verin`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.message:
        await event.edit("`Yalnız yazıya tweet effekti əlavə bilirəm`")
        return
    chat = "@TwitterStatusBot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("Ups botlar tweet effekti istifadə edə bilməz.")
        return
    asc = await event.edit("`Tweeting..`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1276223938)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit("`Bir problem baş verdi...`")
            return
        if response.text.startswith("Forward"):
            await event.edit(
                "Gizlilik ayarlarınızı düzəldin."
            )
        else:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
                caption=f"Tweet by @TheCyberUserBot",
            )
            await event.client.send_read_acknowledge(conv.chat_id)

@register(outgoing=True, pattern=".png ?(.*)")
async def png(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Xahiş edirəm, bir şəkilə yada stikcerə cavab verin.`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`Xahiş edirəm, bir şəkilə yada stikcerə cavab verin.`")
        return
    chat = "@newstickeroptimizerbot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("Oups botlar PNG converter istifadə edə bilməz.")
        return
    asc = await event.edit("PNG-yə `çevrilir`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=436288868)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit("@newstickeroptimizerbot'u `blokdan çıxardın və yenidən yoxlayın`")
            return
        if response.text.startswith("Forward"):
            await event.edit(
                "Gizlilik ayarlarınızı kontrol edin."
            )
        else:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
                caption=f"@TheCyberUserBot ilə PNG-yə çevrildi",
            )
            await event.client.send_read_acknowledge(conv.chat_id)

CmdHelp('stick').add_command(
    'stick', None, 'Cavab verdiyiniz şəkli Sticker olaraq atar.'
).add_command(
    'png', None, 'Cavab verdiyiniz stickeri və ya şəkili PNG formatına çevirər.'
).add_command(
    'tweet', None, 'Cavab verdiyiniz mətni tweet-ə çevirər.'
).add()
