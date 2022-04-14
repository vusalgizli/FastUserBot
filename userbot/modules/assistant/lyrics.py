# Get 
# Osdur
# Ala

from telethon import events
from telethon.events import *
from . import tgbot, FAST_VERSION, DEFAULT_NAME
import requests 
import os

API = "https://apis.xditya.me/lyrics?song="

@tgbot.on(events.NewMessage(pattern="^/lyrics(?: |$)(.*)"))
async def lyrics(event):
    musiqi_adi = event.pattern_match.group(1)
    musiqi_sozleri = sozler(musiqi_adi)
    try: 
        await event.reply(f"{musiqi_sozleri}")
    except Exception as e:
        await event.reply(f"Bağışlayın, {musiqi_adi} mahnısının sözlərini tapa bilmədim.")

def axtar(mahni_adi):
        r = requests.get(API + mahni_adi)
        find = r.json()
        return find

def sozler(mahni_adi):
        fin = axtar(mahni_adi)
        text = f'**🎶 {mahni_adi} adlı mahnının sözləri:**\n\n\n\n'
        text += f'`{fin["lyrics"]}`'
        text += '\n\n\n**Rəsmi ❗ @FastSupp.**'
        return text
