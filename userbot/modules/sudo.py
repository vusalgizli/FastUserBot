# Copyright (C) 2021-2022 FastUserBot
# This file is a part of < https://www.github.com/FastUserBot/FastUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FastUserBot/FastUserBot/blob/master/LICENSE/>.
# 
# Qəhibə #
#Naxuy
#Dalbayov 

import os
import re
from userbot.cmdhelp import CmdHelp
from userbot.events import register
from userbot import (
    HEROKU_APPNAME,
    HEROKU_APIKEY,
    SUDO_VERSION,
    SUDO_ID,
    bot,
)
import heroku3
from telethon.tl.functions.users import GetFullUserRequest

Heroku = heroku3.from_key(HEROKU_APIKEY)
heroku_api = "https://api.heroku.com"
fastsudo = os.environ.get("SUDO_ID", None)
sudosiyahisi = os.environ.get("SUDO_ID", None)

@register(outgoing=True,
          pattern=r"^.addsudo")
async def sudoelave(event):
    await event.edit("F A S T \nİstifadəçi sudo olaraq qeyd edilir...")
    fast = "SUDO_ID"
    if HEROKU_APPNAME is not None:
        app = Heroku.app(HEROKU_APPNAME)
    else:
        await event.edit("`F A S T:" "\nXahiş edirəm` **HEROKU_APPNAME** dəyərini əlavə edin.")
        return
    heroku_var = app.config()
    if event is None:
        return
    try:
        fastt = await get_user(event)
    except Exception:
        await event.edit("Xahiş edirəm bir istifadəçiyə cavab verin.")
    if fastsudo:
        yenisudo = f"{fastsudo} {fastt}"
    else:
        yenisudo = f"{fastt}"
    await event.edit("İstifadəçi sudo olaraq qeyd edildi!\nF A S T yenidən başladılır...")
    heroku_var[fast] = yenisudo
    

    
@register(outgoing=True,
          pattern=r"^.sudosil")
async def sudosil(event):
  Heroku = heroku3.from_key(HEROKU_APIKEY)
  app = Heroku.app(HEROKU_APPNAME)
  heroku_var = app.config()
  if not event.is_reply:
    return await event.edit("Xahiş edirəm bir istifadəçinin mesajını cavablandırın.")
  if event.is_reply:
    id = (await event.get_reply_message()).sender_id
    ad = (await bot.get_entity(id)).first_name
    op = re.search(str(id), str(sudosiyahisi))
    if op:
      i = ""
      sakoxz = sudosiyahisi.split(" ")
      sakoxz.remove(str(id))
      i += str(sakoxz)
      x = i.replace("[", "")
      xx = x.replace("]", "")
      xxx = xx.replace(",", "")
      hazir = xxx.replace("'", "")
      heroku_var["SUDO_ID"] = hazir
      await event.edit(f"`{ad}` adlı istifadəçinin icazəsi alındı.\nF A S T yenidən başladılır...")
    else:
      await event.edit(f"Bağışlayın, `{ad}` istifadəçi sudo olaraq qeyd olunmayıb!")
    if heroku_var["SUDO_ID"] == None:
       await event.edit(f"`Sudo siyahısı boşdur!`") 
    

async def get_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.forward.sender_id)
            )
        else:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.sender_id)
            )
    fastt = replied_user.user.id
    return fastt
    
    
Help = CmdHelp('sudo')
Help.add_command('addsudo', None, 'Cavab verdiyiniz istifadəçini botunuzda admin edər.')
Help.add_command('sudosil', None, 'Cavab verdiyiniz istifadəçinin botunuzda olan adminliyini alar.')
Help.add()
