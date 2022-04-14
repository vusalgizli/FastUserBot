#Qəhibəlik Eləmə Gijdillax😃👌

from telethon import events
from telethon.events import *
from . import tgbot, SAHIB_ID
import asyncio
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
)

#================================================#

PP_TOO_SMOL = "`Şəkil çox balacadır.`"
PP_ERROR = "`Bilinməyən xəta baş verdi.`"
NO_ADMIN = "`Bunu edə bilməyim üçün məni admin etməlisiniz!`"
NO_PERM = (
    "`Bunu edə bilməyim üçün kifayət qədər icazəm yoxdur!`"
)
NO_SQL = "`Bot qeyri-SQL rejimində işləyir!`"
CHAT_PP_CHANGED = "`Şəkil uğurla dəyişdirildi!`"
CHAT_PP_ERROR = (
    "`Şəklin yenilənməsi ilə bağlı bəzi problem aşkarlandı,`"
    "`mən admin deyiləm və ya,`"
    "`lazım olan admin hüquqlarına sahib deyiləm.`"
)
INVALID_MEDIA = "`Yanlış format.`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

#================================================#

# Admin hüquqlarını yoxlamağa kömək edir.
async def admindirmi(user_id: int, message):
    admin = False
    async for user in tgbot.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or SAHIB_ID:
            admin = True
            break
    return admin      


@tgbot.on(events.NewMessage(pattern="^/purge"))
async def purge(event):
    chat = event.chat_id
    msgs = []

    if not await admindirmi(user_id=event.sender_id, message=event):
        await event.reply("`Bunu etmək üçün admin olmalısınız.`")
        return

    msg = await event.get_reply_message()
    if not msg:
        await event.reply("`Təmizləməyə haradan başlayacağınızı seçmək üçün mesaja cavab verin.`")
        return

    try:
        msg_id = msg.id
        count = 0
        to_delete = event.message.id - 1
        await tgbot.delete_messages(chat, event.message.id)
        msgs.append(event.reply_to_msg_id)
        for m_id in range(to_delete, msg_id - 1, -1):
            msgs.append(m_id)
            count += 1
            if len(msgs) == 100:
                await tgbot.delete_messages(chat, msgs)
                msgs = []

        await tgbot.delete_messages(chat, msgs)
        del_res = await tgbot.send_message(
            event.chat_id, f"Təmizləndi `{count}` mesaj."
        )

        await asyncio.sleep(4)
        await del_res.delete()

    except MessageDeleteForbiddenError:
        text = "Xəta baş verdi!\n"
        text += "Mesajlar çox köhnə ola bilər və ya admin deyiləm!"
        del_res = await respond(text, parse_mode="md")
        await asyncio.sleep(5)
        await del_res.delete()


@tgbot.on(events.NewMessage(pattern="^/del$"))
async def mesaj_sil(event):
    if not await admindirmi(user_id=event.sender_id, message=event):
        await event.reply(NO_ADMIN)
        return
    chat = event.chat_id
    msg = await event.get_reply_message()
    if not msg:
        await event.reply("`Silməmi istəyidiniz mesaja cavab verin.`")
        return
    to_delete = event.message
    chat = await event.get_input_chat()
    rm = [msg, to_delete]
    await tgbot.delete_messages(chat, rm)


@tgbot.on(events.NewMessage(pattern="^/ban(?: |$)(.*)"))
async def ban(event):
    noob = event.sender_id
    userids = []
    async for user in tgbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    ):
        userids.append(user.id)
    if noob not in userids:
        await event.reply(NO_ADMIN)
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await event.reply("`Bunu edə bilmək üçün admin və ya qrup sahibi olmalısınız.`")
        return

    user, reason = await get_user_from_event(event)
    if user:
        pass
    else:
        return
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        await event.reply(NO_ADMIN)
        return
    try:
        reply = await event.get_reply_message()
        if reply:
            pass
    except BadRequestError:
        await event.reply(
            "`Mənim mesaj göndərmə hüququm yoxdur! Ancaq yenə də qadağan edildi!`"
        )
        return
    if reason:
        await event.reply(f"Ban prosesi uğurla edildi!\nİstifadəçi ID: `{str(user.id)}` \nSəbəb: {reason}")
    else:
        await event.reply(f"Ban prosesi uğurla edildi!\nİstifadəçi ID: `{str(user.id)}` !")

@tgbot.on(events.NewMessage(pattern="^/unban(?: |$)(.*)"))
async def unban(event):
    userids = []
    noob = event.sender_id
    async for user in tgbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    ):
        userids.append(user.id)
    if noob not in userids:
        await event.reply("`Bunu edə bilmək üçün admin və ya qrup sahibi olmalısınız.`")
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await event.reply(NO_ADMIN)
        return
    user = await get_user_from_event(event)
    user = user[0]
    if user:
        pass
    else:
        return
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await event.reply("`İstifadəçi yenidən qatıla bilər.`")
    except BadRequestError:
        await event.reply(NO_ADMIN)
        return

@tgbot.on(events.NewMessage(pattern="^/promote(?: |$)(.*)"))
async def promote(event):
    userids = []
    noob = event.sender_id
    async for user in tgbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    ):
        userids.append(user.id)
    if noob not in userids:
        await event.reply("`Bunu edə bilmək üçün admin və ya qrup sahibi olmalısınız.`")
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await event.reply(NO_ADMIN)
        return

    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=False,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "Admin" 
    if user:
        pass
    else:
        return
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
        await event.reply("`Uğurla admin edildi!`")
    except BadRequestError:
        await event.reply(NO_ADMIN)
        return

@tgbot.on(events.NewMessage(pattern="^/demote(?: |$)(.*)"))
async def demote(event):
    userids = []
    noob = event.sender_id
    async for user in tgbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    ):
        userids.append(user.id)
    if noob not in userids:
        await event.reply("`Bunu etmək üçün admin olmalısınız.`")
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await event.reply(NO_ADMIN)
        return

    rank = "Admin" 
    user = await get_user_from_event(event)
    user = user[0]
    if user:
        pass
    else:
        return

    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        await event.reply(NO_ADMIN)
        return
    await event.reply("`Adminlik uğurla alındı!`")


@tgbot.on(events.NewMessage(pattern="^/pin(?: |$)(.*)"))
async def pin(event):
    userids = []
    noob = event.sender_id
    async for user in tgbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    ):
        userids.append(user.id)
    if noob not in userids:
        await event.reply("`Bunu edə bilmək üçün admin və ya qrup sahibi olmalısınız.`")
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await event.reply(NO_ADMIN)
        return

    to_pin = event.reply_to_msg_id

    if not to_pin:
        await event.reply("`Sabitləməyimi istədiyiniz mesaja cavab verin.`")
        return

    options = event.pattern_match.group(1)
    is_silent = True
    if options.lower() == "loud":
        is_silent = False
    try:
        await event.client(UpdatePinnedMessageRequest(event.to_id, to_pin, is_silent))
    except BadRequestError:
        await event.reply(NO_ADMIN)
        return
    await event.reply("`Mesaj uğurla sabitləndi!`")
    user = await get_user_from_id(msg.sender_id, msg)



async def get_user_from_event(event):
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.reply("`İstifadəçinin istifadəçi adını, id-sini yazın, və ya mesajına cavab yazın!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None

    return user_obj
