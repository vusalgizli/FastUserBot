# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

from pydub import AudioSegment
from json import dumps
from userbot.events import register
from .shazam_helper.communication import recognize_song_from_signature
from .shazam_helper.algorithm import SignatureGenerator
from requests import get
from os import remove
import urllib.parse
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern=r"^\.shazam(?: |$)(.*)")
async def shazam(event):
    if not event.is_reply:
        return await event.edit('`Zəhmət olmasa bir səs faylına cavab verin!`')
    else:
        await event.edit('`⬇️ Səs faylı yüklənir...`')
        reply_message = await event.get_reply_message()
        dosya = await reply_message.download_media()

        await event.edit('`🛠 Səs dosyası fingerprint formatına çevirilir...`')
        audio = AudioSegment.from_file(dosya)
        audio = audio.set_sample_width(2)
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
            
        signature_generator = SignatureGenerator()
        signature_generator.feed_input(audio.get_array_of_samples())
            
        signature_generator.MAX_TIME_SECONDS = 12
        if audio.duration_seconds > 12 * 3:
            signature_generator.samples_processed += 16000 * (int(audio.duration_seconds / 2) - 6)
            
        results = '{"error": "Not found"}'
        sarki = None
        await event.edit('`🎧 🎤 Shazamlanır...`')
        while True:
            signature = signature_generator.get_next_signature()
            if not signature:
                sarki = results
                break
            results = recognize_song_from_signature(signature)
            if results['matches']:
                sarki = results
                break
            else:
                await event.edit(f'`İlk {(signature_generator.samples_processed / 16000)} saniyədə heç nə tapılmadı...\nBiraz daha yoxlayıram.`')
        
        if 'track' not in sarki:
            return await event.edit('`Ehh Shazam verdiyiniz səsi anlamadı 😔. Biraz daha açıq səs göndərə bilərsən?`')
        await event.edit('`✅ Musiqini tapdım... Məlumatlar toplanır...`')
        Caption = f'**Musiqi:** [{sarki["track"]["title"]}]({sarki["track"]["url"]})\n'
        if 'artists' in sarki['track']:
            Caption += f'**Sənətçi(lər):** [{sarki["track"]["subtitle"]}](https://www.shazam.com/artist/{sarki["track"]["artists"][0]["id"]})\n'
        else:
            Caption += f'**Sənətçi(lər):** `{sarki["track"]["subtitle"]}`\n'

        if 'genres'in sarki['track']:
            Caption += f'**Janr:** `{sarki["track"]["genres"]["primary"]}`\n'

        if sarki["track"]["sections"][0]["type"] == "SONG":
            for metadata in sarki["track"]["sections"][0]["metadata"]:
                Caption += f'**{"İl" if metadata["title"] == "Sorti" else metadata["title"]}:** `{metadata["text"]}`\n'

        Caption += '\n**Musiqi Platformaları:** '
        for provider in sarki['track']['hub']['providers']:
            if provider['actions'][0]['uri'].startswith('spotify:track'):
                Url = provider['actions'][0]['uri'].replace(
                    'spotify:track:', 'http://open.spotify.com/track/'
                )
            elif provider['actions'][0]['uri'].startswith('intent:#Intent;action=android.media.action.MEDIA_PLAY_FROM_SEARCH'):
                Url = f'https://open.spotify.com/search/' + urllib.parse.quote(sarki["track"]["subtitle"] + ' - ' + sarki["track"]["title"])
            elif provider['actions'][0]['uri'].startswith('deezer'):
                Url = provider['actions'][0]['uri'].replace(
                    'deezer-query://', 'https://'
                )
            else:
                Url = provider['actions'][0]['uri']
            Caption += f'[{provider["type"].capitalize()}]({Url}) '
        for section in sarki['track']['sections']:
            if section['type'] == 'VIDEO':
                if 'youtubeurl' in section:
                    Youtube = get(section['youtubeurl']).json()
                else:
                    return

                Caption += f'\n**Klip Videosu:** [Youtube]({Youtube["actions"][0]["uri"]})'

        if 'images' in sarki["track"] and len(sarki["track"]["images"]) >= 1:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                sarki["track"]["images"]["coverarthq"] if 'coverarthq' in sarki["track"]["images"] else sarki["track"]["images"]["background"],
                caption=Caption,
                reply_to=reply_message
                )
        else:
            await event.edit(Caption)  
        remove(dosya)



@register(outgoing=True, pattern=r"^\.shazam2(?: |$)(.*)")
async def _(event):
    if not event.reply_to_msg_id:
        return await event.edit("`Zəhmət olmasa musiqi faylına cavab verin.`")
    reply_message = await event.get_reply_message()
    chat = "@auddbot"
    try:
        async with event.client.conversation(chat) as conv:
            try:
                await event.edit("`Musiqi skan edilir...`")
                start_msg = await conv.send_message("/start")
                await conv.get_response()
                send_audio = await conv.send_message(reply_message)
                check = await conv.get_response()
                if not check.text.startswith("Audio received"):
                    return await event.edit(
                        "`Mahnı tanınarkən xəta baş verdi.\n5-10 saniyə uzunluğunda bir səs mesajı istifadə etməyə çalışın.`"
                    )
                await event.edit("`Bir az gözləyin...`")
                result = await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.edit("**Hmm deyəsən @auddbot bloklamısan.\nBloku aç sonra yenidən yoxla.**")
                return
            namem = f"**Mahnı adı:** `{result.text.splitlines()[0]}`\
        \n\n**Detallar:** `{result.text.splitlines()[2]}`"
            await event.edit(namem)
            await event.client.delete_messages(
                conv.chat_id, [start_msg.id, send_audio.id, check.id, result.id]
            )
    except TimeoutError:
        return await event.edit(
            "**Xəta: @auddbot cavab vermir, daha sonra yenidən cəhd edin**"
        )     
        
        
Help = CmdHelp('shazam')
Help.add_command('shazam', '<cavab>', 'Cavab verdiyiniz səs faylını Shazamda axtarar.')
Help.add_command('shazam2', '<cavab>', 'Cavab verdiyiniz səs faylını @auddbot-da axtarar.')
Help.add_info('@TheCyberUserBot')
Help.add()
