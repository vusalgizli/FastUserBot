# Copyright (C) 2021-2022 FastUserBot
# This file is a part of < https://www.github.com/FastUserBot/FastUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FastUserBot/FastUserBot/blob/master/LICENSE/>.

from asyncio import sleep
from requests import get
from telethon.events import ChatAction
from telethon.tl.types import ChannelParticipantsAdmins, Message
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, ANTI_SPAMBOT, ANTI_SPAMBOT_SHOUT, bot


@bot.on(ChatAction)
async def anti_spambot(welcm):
    try:
        if not ANTI_SPAMBOT:
            return
        if welcm.user_joined or welcm.user_added:
            adder = None
            ignore = False
            users = None

            if welcm.user_added:
                ignore = False
                try:
                    adder = welcm.action_message.from_id
                except AttributeError:
                    return

            async for admin in bot.iter_participants(
                    welcm.chat_id, filter=ChannelParticipantsAdmins):
                if admin.id == adder:
                    ignore = True
                    break

            if ignore:
                return

            elif welcm.user_joined:
                users_list = hasattr(welcm.action_message.action, "users")
                if users_list:
                    users = welcm.action_message.action.users
                else:
                    users = [welcm.action_message.from_id]

            await sleep(5)
            spambot = False

            if not users:
                return

            for user_id in users:
                async for message in bot.iter_messages(welcm.chat_id,
                                                       from_user=user_id):

                    correct_type = isinstance(message, Message)
                    if not message or not correct_type:
                        break

                    join_time = welcm.action_message.date
                    message_date = message.date

                    if message_date < join_time:
                        # E??er mesaj kullan??c?? kat??lma tarihinden daha ??nce ise yoksay??l??r.
                        continue

                    check_user = await welcm.client.get_entity(user_id)

                    # Hata ay??klama. ??lerideki durumlar i??in b??rak??ld??. ###
                    print(
                        f"Qat??lan istifad????i: {check_user.first_name} [ID: {check_user.id}]"
                    )
                    print(f"Qrup: {welcm.chat.title}")
                    print(f"Zaman: {join_time}")
                    print(
                        f"G??nd??rdiyi mesaj: {message.text}\n\n[Zaman: {message_date}]"
                    )
                    ##############################################

                    try:
                        cas_url = f"https://combot.org/api/cas/check?user_id={check_user.id}"
                        r = get(cas_url, timeout=3)
                        data = r.json()
                    except BaseException:
                        print(
                            "CAS kontrolu u??ursuzdur, k??hn?? anti_spambot kontroluna qay??d??l??r."
                        )
                        data = None
                        pass

                    if data and data['ok']:
                        reason = f"[Combot Anti Spam t??r??find??n banland??.](https://combot.org/cas/query?u={check_user.id})"
                        spambot = True
                    elif "t.cn/" in message.text:
                        reason = "`t.cn` URL'leri a??karland??."
                        spambot = True
                    elif "t.me/joinchat" in message.text:
                        reason = "Qrup v?? ya kanal reklam?? mesaj??."
                        spambot = True
                    elif message.fwd_from:
                        reason = "Y??nl??ndiril??n mesaj"
                        spambot = True
                    elif "?start=" in message.text:
                        reason = "Telegram botu `start` linki"
                        spambot = True
                    elif "bit.ly/" in message.text:
                        reason = "`bit.ly` URL-i a??kar edildi."
                        spambot = True
                    else:
                        if check_user.first_name in ("Bitmex", "Promotion",
                                                     "Information", "Dex",
                                                     "Announcements", "Info",
                                                     "Broadcast", "Broadcasts"
                                                     "M??lumatland??rma", "M??lumatland??rmalar"):
                            if check_user.last_name == "Bot":
                                reason = "Bilin??n SpamBot"
                                spambot = True

                    if spambot:
                        print(f"Spam mesaj??: {message.text}")
                        await message.delete()
                        break

                    continue 

            if spambot:
                chat = await welcm.get_chat()
                admin = chat.admin_rights
                creator = chat.creator
                if not admin and not creator:
                    if ANTI_SPAMBOT_SHOUT:
                        await welcm.reply(
                            "@admins\n"
                            "`ANTI SPAMBOT A??KARLANDI!\n"
                            "BU ??ST??FAD?????? M??N??M SPAMBOT ALQOR??TMAM ??L?? UY??UNLA??IR!`"
                            f"S??B??B: {reason}")
                        kicked = False
                        reported = True
                else:
                    try:

                        await welcm.reply(
                            "`Spambot a??karland??!!`\n"
                            f"`S??B??B:` {reason}\n"
                            "Qrupdan at??l??r, bu ID sonraki prosesl??r ??????n qeyd edilir.\n"
                            f"`??ST??FAD??????:` [{check_user.first_name}](tg://user?id={check_user.id})"
                        )

                        await welcm.client.kick_participant(
                            welcm.chat_id, check_user.id)
                        kicked = True
                        reported = False

                    except BaseException:
                        if ANTI_SPAMBOT_SHOUT:
                            await welcm.reply(
                                "@admins\n"
                                "`ANT?? SPAMBOT A??KAR ED??LD??!\n"
                                "BU ??ST??FAD?????? M??N??M SPAMBOT ALQOR??TMAM ??L?? UY??UNDUR!`"
                                f"S??B??B: {reason}")
                            kicked = False
                            reported = True

                if BOTLOG:
                    if kicked or reported:
                        await welcm.client.send_message(
                            BOTLOG_CHATID, "#ANTI_SPAMBOT B??LD??R????\n"
                            f"??stifad????i: [{check_user.first_name}](tg://user?id={check_user.id})\n"
                            f"??stifad????i IDsi: `{check_user.id}`\n"
                            f"Qrup: {welcm.chat.title}\n"
                            f"Qrup IDsi: `{welcm.chat_id}`\n"
                            f"S??b??b: {reason}\n"
                            f"Mesaj:\n\n{message.text}")
    except ValueError:
        pass


CMD_HELP.update({
    'anti_spambot':
    "??stifad??si: Bu modul config.env fayl??nda ya da env d??y??ri il?? aktiv edilibs??,\
        \n??g??r spam ed??nl??r UserBot'un anti-spam alqoritmas?? il?? uy??unla????rsa, \
        \nbu modul qrupdaki spammerl??ri qrupdan atar. (ya da adminl??r?? bildir??r.)"
})
