# Copyright (C) 2021-2022 FastUserBot

import importlib
from importlib import import_module
from sqlite3 import connect
import time
import os
from pathlib import Path
import sys
import requests
import asyncio

from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.channels import GetMessagesRequest
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID, CMD_HELP, LANGUAGE, FAST_VERSION, PATTERNS, BOTLOG_CHATID, BOTLOG, StartTime
from .modules import ALL_MODULES
import userbot.modules.sql_helper.mesaj_sql as MSJ_SQL
import userbot.modules.sql_helper.galeri_sql as GALERI_SQL
from pySmartDL import SmartDL
from random import randint
from telethon.tl import functions

from random import choice
import chromedriver_autoinstaller
from json import loads, JSONDecodeError
import re
from asyncio import get_event_loop
import userbot.cmdhelp

from userbot import DEFAULT_NAME, SAHIB_ID, SON_GORULME
from time import time
import userbot.events
from userbot.events import start_fast_assistant

FAST_NAME = f"[{DEFAULT_NAME}](tg://user?id={SAHIB_ID})"
QRUP = BOTLOG_CHATID

def fast_time(seconds, short=True):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + (" gün, " if not short else "g, ")) if days else "") + \
        ((str(hours) + (" saat, " if not short else "s, ")) if hours else "") + \
        ((str(minutes) + (" dəqiqə, " if not short else "d, ")) if minutes else "") + \
        ((str(seconds) + (" saniyə, " if not short else "s, ")) if seconds else "")
    return tmp[:-2] + " əvvəl"

notafk = round(time() - SON_GORULME)
noe = fast_time(notafk)
noe2 = fast_time(notafk, False)
NO_AFK_TIME = noe2

ALIVE_STR = [
    "`🇫​🇦​🇸​🇹​ 🇺​🇸​🇪​🇷​🇧​🇴​🇹​` {mention}-un `👤əmrlərini icra etməyə hazırdır👤`",
    "`🇦🇿 Salam` {mention} `narahat olma 🇫​🇦​🇸​🇹​ 🇺​🇸​🇪​🇷​🇧​🇴​🇹​ əla işləyir...`",
    "✨ `🇫​🇦​🇸​🇹​ 🇺​🇸​🇪​🇷​🇧​🇴​🇹​` **{mention}**-in `əmirlərini icra edir🌐`",
    "✨ {mention} `əlimdən gələnin ən yaxşısını edəcəm✨`",
]

LOGO_STR = [
    "https://telegra.ph/file/263cc6bbc34d4eaeef71b.jpg",
]


KICKME_STR = [
    "Bye bye mən gedirəm! 🦦",
    "Qrupu tərk edirəm! 😒",
    "Qrupdan çıxıram..\nBir daha dönməmək şərti ilə!",
    "Qrupdan ayrılıram... 🦦",
]

NON_AFK = [
    f"`ℹArtıq AFK deyiləm yaza bilərsinizℹ`",
    f"{FAST_NAME} `☢artıq AFK deyil☢`",
    f"{FAST_NAME} `♦buradadır♦`",
    f"{FAST_NAME} `🥰Gəldim🥰`",
    f"{FAST_NAME} `❤️artıq sizinlədir❤️",
]

DIZCILIK_STR = [
    "😎Stickeri fırladıram😎",
    "⚡Sticker paketə əlavə edilir⚡",
    "♥Bu sticker artıq mənimdir!♥",
    "📩⛓Bunu stickerlərimə əlavə etməliyəm..",
    "⛓Sticker həps edilir...",
    "Stikerini oğurladım\nhahaha.",
    "▪▫Mən bir sticker oğrusuyam stickerin məndədi▫▪ ;D!",
    "🖇Nə gözəl stickerdi bu!🖇"
    "🔰Stiker paketə əlavə edilir🔰",
    "🔰Stikeri öz paketimə əlavə edirəm🔰",
]

AFKSTR = [
    "💫İndi vacib işimlərim var, gələndə yazacam🖤\nSahibim `{last_seen_long}` ℹ aktiv idi ℹ",
    "🥲Birazdan gələcəm amma gəlməsəm...\nDarıxma😕.\nSahibim `{last_seen_long}` ℹ aktiv idi ℹ",
    "😡Ay xaam yeri get..\nistirahət elirəm:)\nbiraz daha gözlə.\nSahibim `{last_seen_long}` ℹ aktiv idi ℹ",
    "İndi burada deyiləm..\nYəqin ki, başqa bir yerdəyəm..\nSahibim `{last_seen_long}` ℹ aktiv idi ℹ",
    "Sahibim hal-hazırda AFK dı!\nSahibim `{last_seen_long}` ℹ aktiv idi ℹ",
    "🎈həyatdakı ən yaxşı şeyləri gözləməyə dəyər…\nGələcəm.🎈\nSahibim `{last_seen_long}` ℹ aktiv idi ℹ",
    "Bəli❓\nGələcəm.\nSahibim `{last_seen_long}` ℹ aktiv idi ℹ",
    "▪▫Sahibim gəlir gözlə▫▪.\nSahibim `{last_seen_long}` ℹ aktiv idi ℹ",
    "Hal-hazırda sahibim burada deyil❗\nXahiş edirəm biraz sonra əlaqə saxlayın.\nSahibim `{last_seen_long}` ℹ aktiv idiℹ ",
    "💠Salam, uzaq mesajıma xoş gəldiniz💠, sizə necə kömək edə bilərəm?\nSahibim `{last_seen_long}` ℹ aktiv idi ℹ",
    "Mən sahibimin xüsusi botuyam!, sizdə bot istəyirsizsə: ⚜ @FastUserBot ⚜ qur.\nSahibim `{last_seen_long}` ℹ aktiv idi ℹ",
    "Hal hazırda burdan çoox uzaqdayam.\nQışqırsan bəlkə eşitdim.\nSahibim `{last_seen_long}` ℹ aktiv idi ℹ",
    "Bu tərəfə gedirəm 🔜.\nSahibim `{last_seen_long}` ℹ aktiv idi ℹ",
    "Mesajınızı Sahibim ə göndərirəm...\nbiraz daha gözlə.\nSahibim `{last_seen_long}` ℹ aktiv idi ℹ",
    "✖Sahibim burda deyil mənə yazmağı kəs artıq.✖nqayıtdığında sizinlə əlaqə saxlayacaqdır.\nSahibim `{last_seen_long}` ℹ aktiv idi ℹ",
]

UNAPPROVED_MSG = ("`Salam,` {mention} `\nBu bir avtomatik mesajdır.\nNarahat olma.\n\n`"
                  "`Sahibim sənə PM yazma icazəsi verməyib. `"
                  "`Zəhmət olmasa sahibimin aktiv olmasını gözləyin, o bəzən PM yazmağa icazə verər.\n\n`"
                  "`Bildiyim qədəri ilə o beynini itirib insanlara PM icazəsi vermir.`")

DB = connect("learning-data-root.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()
INVALID_PH = '\nXƏTA: Yazılan telefon nömrəsi yanlışdır' \
             '\n  Tips: Ölkə kodunu istifadə edərək yenidən yaz' \
             '\n       Telefon nömrənizi kontrol edin.'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("learning-data-root.check").close()

def extractCommands(file):
    FileRead = open(file, 'r').read()
    
    if '/' in file:
        file = file.split('/')[-1]

    Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", FileRead)
    Komutlar = []

    if re.search(r'CmdHelp\(.*\)', FileRead):
        pass
    else:
        dosyaAdi = file.replace('.py', '')
        CmdHelp = userbot.cmdhelp.CmdHelp(dosyaAdi, False)

       
        for Command in Pattern:
            Command = Command[1]
            if Command == '' or len(Command) <= 1:
                continue
            Komut = re.findall("(^.*[a-zA-Z0-9şğüöçı]\w)", Command)
            if (len(Komut) >= 1) and (not Komut[0] == ''):
                Komut = Komut[0]
                if Komut[0] == '^':
                    KomutStr = Komut[1:]
                    if KomutStr[0] == '.':
                        KomutStr = KomutStr[1:]
                    Komutlar.append(KomutStr)
                else:
                    if Command[0] == '^':
                        KomutStr = Command[1:]
                        if KomutStr[0] == '.':
                            KomutStr = KomutStr[1:]
                        else:
                            KomutStr = Command
                        Komutlar.append(KomutStr)

           
            Fastpy = re.search('\"\"\"FASTPY(.*)\"\"\"', FileRead, re.DOTALL)
            if not Fastpy is None:
                Fastpy = Fastpy.group(0)
                for Satir in Fastpy.splitlines():
                    if (not '"""' in Satir) and (':' in Satir):
                        Satir = Satir.split(':')
                        Isim = Satir[0]
                        Deger = Satir[1][1:]
                                
                        if Isim == 'INFO':
                            CmdHelp.add_info(Deger)
                        elif Isim == 'WARN':
                            CmdHelp.add_warning(Deger)
                        else:
                            CmdHelp.set_file_info(Isim, Deger)
            for Komut in Komutlar:
                # if re.search('\[(\w*)\]', Komut):
                    # Komut = re.sub('(?<=\[.)[A-Za-z0-9_]*\]', '', Komut).replace('[', '')
                CmdHelp.add_command(Komut, None, 'Bu plugin xaricdən yüklənib, hər hansı bir açıqlama qeyd olunmayıb.')
            CmdHelp.add()

try:
    bot.start()
    idim = bot.get_me().id
    fastbl = requests.get('https://raw.githubusercontent.com/FastUserBot/FastUserBot/main/fastbl.json').json()
    if idim in fastbl:
        bot.send_message("me", "**FAST USERBOT adminləri tərəfindən botdan istifadə haqqınız alındı.**\n**Səbəb:** `None`")
        bot.disconnect()

    
    try:
        chromedriver_autoinstaller.install()
    except:
        pass
    
    
    GALERI = {}

    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {"alive": f"{str(choice(ALIVE_STR))}", "afk": f"`{str(choice(AFKSTR))}`", "kickme": f"{str(choice(KICKME_STR))}", "pm": UNAPPROVED_MSG, "dızcı": str(choice(DIZCILIK_STR)), "ban": "{mention}`, Banlandı!`", "mute": "{mention}`, səssizə alındı!`", "approve": "{mention}`, artıq mənə mesaj göndərə bilərsən!`", "disapprove": "{mention}`, artıq mənə mesaj göndərə bilməzsən!`", "block": "{mention}`, səni əngəllədim!`", "nonafk": f"{str(choice(NON_AFK))}", "salive": "https://telegra.ph/file/c3e75eccaeb7f56dfae89.mp4"}

    PLUGIN_MESAJLAR_TURLER = ["alive", "afk", "kickme", "pm", "dızcı", "ban", "mute", "approve", "disapprove", "block", "nonafk", "salive"]
    for mesaj in PLUGIN_MESAJLAR_TURLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if dmsj is False:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            if dmsj.startswith("MEDYA_"):
                medya = int(dmsj.split("MEDYA_")[1])
                medya = bot.get_messages(PLUGIN_CHANNEL_ID, ids=medya)

                PLUGIN_MESAJLAR[mesaj] = medya
            else:
                PLUGIN_MESAJLAR[mesaj] = dmsj
    if not PLUGIN_CHANNEL_ID is None:
        LOGS.info("Plugins installing...")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
        except:
            KanalId = "me"

        for plugin in bot.iter_messages(KanalId, filter=InputMessagesFilterDocument):
            if plugin.file.name and (len(plugin.file.name.split('.')) > 1) \
                and plugin.file.name.split('.')[-1] == 'py':
                Split = plugin.file.name.split('.')

                if not os.path.exists("./userbot/modules/" + plugin.file.name):
                    dosya = bot.download_media(plugin, "./userbot/modules/")
                else:
                    LOGS.info("Bu plugin onsuzda yüklüdür " + plugin.file.name)
                    extractCommands('./userbot/modules/' + plugin.file.name)
                    dosya = plugin.file.name
                    continue 
                
                try:
                    spec = importlib.util.spec_from_file_location("userbot.modules." + Split[0], dosya)
                    mod = importlib.util.module_from_spec(spec)

                    spec.loader.exec_module(mod)
                except Exception as e:
                    LOGS.info(f"Yükləmədə problem! Plugin xətalıdır.\n\nXəta: {e}")

                    try:
                        plugin.delete()
                    except:
                        pass

                    if os.path.exists("./userbot/modules/" + plugin.file.name):
                        os.remove("./userbot/modules/" + plugin.file.name)
                    continue
                extractCommands('./userbot/modules/' + plugin.file.name)
    else:
        bot.send_message("me", f"`Xahiş edirəm pluginlərin qalıcı olması üçün PLUGIN_CHANNEL_ID'i ayarlayın.`")
except PhoneNumberInvalidError:
    print(INVALID_PH)
    sys.exit(1)
    
async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["saniyə", "dəqiqə", "saat", "gün"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ", ".join(time_list)

    return up_time


async def startupcyber():
    try:
        if QRUP != 0:
            await bot.send_message(
                QRUP,
                f"**Salam! Mən 𝓕𝓐𝓢𝓣 𝓤𝓢𝓔𝓡 𝓑𝓞𝓣**\n**Botumuzu qurduğunuz üçün təşəkkür edirəm!**\n**Botunuz aktivdir.**\n\n**𝓕𝓐𝓢𝓣 Version:** **{FAST_VERSION}**\n**Plugin sayı: {len(CMD_HELP)}**\n**Sahib: {FAST_NAME}**\n**Plugin kanalı:** @FastPlugins\n**FAST ADMIN Heyəti:** @FastMMC\n\n**Yardıma ehtiyyacınız olarsa @FastSupp qrupuna yazın :)**",
            )
    except Exception as e:
        LOGS.info(str(e))


async def FotoDegistir (foto):
    FOTOURL = GALERI_SQL.TUM_GALERI[foto].foto
    r = requests.get(FOTOURL)

    with open(str(foto) + ".jpg", 'wb') as f:
        f.write(r.content)    
    file = await bot.upload_file(str(foto) + ".jpg")
    try:
        await bot(functions.photos.UploadProfilePhotoRequest(
            file
        ))
        return True
    except:
        return False

aktiv_et = "ON"

async def asistan_aktiv_et():
    if aktiv_et == "ON":
        import glob

        path = "userbot/modules/assistant/*.py"
        fayl = glob.glob(path)
        for name in fayl:
            with open(name) as f:
                path1 = Path(f.name)
                shortname = path1.stem
                start_fast_assistant(shortname.replace(".py", ""))
    else:
        print("Asistan qurularkən xəta baş verdi.")


for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)
    

loop = asyncio.get_event_loop()
LOGS.info("FAST is working now.")
LOGS.info("Köməyə ehtiyacınız olarsa, @FastSupp qrupuna yazın.")
LOGS.info(f"FAST Version: {FAST_VERSION}")
bot.loop.create_task(startupcyber())
bot.loop.create_task(asistan_aktiv_et())
bot.run_until_disconnected()
