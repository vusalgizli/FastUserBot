#FastUserBot Üçün Təyin Olunub!
#👌
#🥱
#😃
#🖕

from telethon import Button, custom
from userbot import *
from . import *

async def setit(fast, ad, deyer):
    try:
        fast.set(ad, deyer)
    except BaseException:
        return await fast.edit("`Xəta baş verdi.`")


def geri_butonu(ad):
    button = [Button.inline("« Geri", data=f"{ad}")]
    return button
