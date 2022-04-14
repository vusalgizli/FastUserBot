# Copyright (C) 2021-2022 FastUserBot
# This file is a part of < https://github.com/FastUserBot/FastUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FastUserBot/FastUserBot/blob/master/LICENSE/>.

def e_(fayl_adi, name, slep, siyahi):
	f = open(f"./fastuserbot{fayl_adi}.py", "x")
	f.write(f"""from userbot.events import register
from userbot.cmdhelp import CmdHelp
from time import sleep
from telethon import events

a={siyahi}

@register(outgoing=True, pattern="^.{name}$")
async def _(fast):
	for i in a:
		await fast.edit(' '+str(i))
		sleep({slep})

Help = CmdHelp("fastuserbot{fayl_adi}")
Help.add_command("{name}", None, "Bu Plugin @FastSupp ilə hazırlanmışdır...")
Help.add()
								""")
	return f.close()

def a_(fayl_adi, name, siyahi, slep):
	f = open(f"./fastuserbot{fayl_adi}.py", "x")
	f.write(f"""from userbot.events import register
from userbot.cmdhelp import CmdHelp
from time import sleep
from telethon import events

a={siyahi}

@register(outgoing=True, pattern="^.{name}$")
async def _(fast):
	text= " "
	for i in a:
		text+=i+"\\n"
		await fast.edit(text)
		sleep({slep})

Help = CmdHelp("fastuserbot{fayl_adi}")
Help.add_command("{name}", None, "Bu Plugin @FastSupp ilə hazırlanmışdır...")
Help.add()
								""")
	return f.close()

def r_(fayl_adi, name, siyahi):
	f = open(f"./fastuserbot{fayl_adi}.py", "x")
	f.write(f"""from userbot.events import register
from userbot.cmdhelp import CmdHelp
from telethon import events
from random import choice

a={siyahi}

@register(outgoing=True, pattern="^.{name}$")
async def _(fast):
	random_ = choice(a)
	await fast.client.send_file(fast.chat_id, random_)
	await fast.delete()

Help = CmdHelp("fastuserbot{fayl_adi}")
Help.add_command("{name}", None, "Bu Plugin @FastSupp ilə hazırlanmışdır...")
Help.add()

		""")

def m_(fayl_adi, name, siyahi):
	f = open(f"./fastuserbot{fayl_adi}.py", "x")
	f.write("""from telethon import events
import asyncio
from userbot.events import register
from userbot.cmdhelp import CmdHelp
import random
import os

IFACI = [{siyahi}]

@register(outgoing=True, pattern="^.{name}$")
async def fastmusic(fast):
    
    
    await fast.edit("`Sizin üçün təsadüfi bir "+IFACI+" musiqisi axtarıram...`")

    try:
        results = await fast.client.inline_query('creatormusicazbot', '+IFACI+')
    except:
            await fast.edit("`Bağışlayın, botdan cavab ala bilmədim!`")
            return

    netice = False
    while netice is False:
            rast = random.choice(results)
            if rast.description == IFACI:
                await fast.edit("`Musiqi yüklənir!\nBiraz gözləyin...`")
                yukle = await rast.download_media()
                await fast.edit("`Yüklənmə tamamlandı!\nFayl göndərilir...`")
                await fast.client.send_file(fast.chat_id, yukle, caption="@FastSupp sizin üçün `"+rast.description+" - "+rast.title+"` musiqisini seçdi\n\nXoş dinləmələr :)")
                await event.delete()
                os.remove(yukle)
                netice = True

Help = CmdHelp("fastuserbot{fayl_adi}")
Help.add_command("{name}", None, "Bu Plugin @FastSupp Tərəfindən Hazırlanmışdır..")
Help.add()

		""".format(
siyahi=siyahi,
name=name,
fayl_adi=fayl_adi
			))
