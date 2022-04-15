#Yenə Sən?🤨

from telethon import events
from telethon.events import *
from . import tgbot, FAST_VERSION, DEFAULT_NAME
from platform import python_version
from telethon import version

ALIVE_LOGO = "https://telegra.ph/file/263cc6bbc34d4eaeef71b.jpg"

HELP_LOGO = "https://telegra.ph/file/263cc6bbc34d4eaeef71b.jpg"

alive_text = (
        f"**🇦🇿 𝐅𝐀𝐒𝐓 𝐔𝐒𝐄𝐑𝐁𝐎𝐓 𝐀𝐊𝐓𝐈̇𝐕𝐃𝐈̇𝐑 🇦🇿** \n"
        f"┏━━━━━━━━━━━━━━━━━━━━\n"
        f"┣[ 🤵🏻 **Sahibim:** `{DEFAULT_NAME}`\n"
        f"┣[ 🏷️ **Python:** `{python_version()}`\n"                               
        f"┣[ ⚒️ **Telethon:** `{version.__version__}`\n"
        f"┣[ 📌 **Branch:** `Master`\n"
        f"┗━━━━━━━━━━━━━━━━━━━━\n"
        f"**Ətraflı məlumat və kômək üçün /help yazın.**"
        )

help_text = (
        f"**🇦🇿 𝙵𝙰𝚂𝚃 𝚄𝚂𝙴𝚁𝙱𝙾𝚃 🇦🇿** \n"
        f"┏━━━━━━━━━━━━━━━━━━━━\n"
        f"┣[ `♻️ /start` - **Start mesajını göndərər.**\n"
        f"┣[ `♻️ /id` - **Bir qrup və ya istifadəçi ID almaq üçün.**\n"                               
        f"┣[ `♻️ /tr` - **Tərcümə edər.**\n"
        f"┣[ `♻️ /help` - **Bu mesajı atar.**\n"
        f"┣[ `♻️ /purge` - **Qeyd etdiyiniz mesajdan sonraki mesajları təmizləyər.**\n"
        f"┣[ `♻️ /del` - **Cavab verdiyiniz mesajı silər.**\n"
        f"┣[ `♻️ /ban` - **Bir istifadəçini ban etmək üçün.**\n"
        f"┣[ `♻️ /unban` - **Bir istifadəçinin banını açar.**\n"
        f"┣[ `♻️ /promote` - **Bir istifadəçini admin etmək üçün.**\n"
        f"┣[ `♻️ /demote` - **Bir istifadəçinin adminlik hüququnu almaq üçün.**\n"
        f"┣[ `♻️ /pin` - **Cavab verdiyiniz mesajı sabitləyər.**\n"
        f"┣[ `♻️ /lyrics` - **Adını yazdığınız musiqinin sözlərini axtarar.**\n"
        f"┗━━━━━━━━━━━━━━━━━━━━\n"
        )

@tgbot.on(events.NewMessage(pattern="^/start"))
async def start_fast_bot(event):
    await tgbot.send_file(event.chat_id, ALIVE_LOGO, caption=alive_text)


@tgbot.on(events.NewMessage(pattern="^/help"))
async def help(event):
    await tgbot.send_file(event.chat_id, HELP_LOGO, caption=help_text)
