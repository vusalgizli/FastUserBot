# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import hashlib
import re


async def md5(fname: str) -> str:
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def humanbytes(size: int) -> str:
    if size is None or isinstance(size, str):
        return ""

    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " gün, ") if days else "")
        + ((str(hours) + " saat, ") if hours else "")
        + ((str(minutes) + " dəqiqə, ") if minutes else "")
        + ((str(seconds) + " saniyə, ") if seconds else "")
    )
    return tmp[:-2]


def human_to_bytes(size: str) -> int:
    units = {
        "M": 2 ** 20,
        "MB": 2 ** 20,
        "G": 2 ** 30,
        "GB": 2 ** 30,
        "T": 2 ** 40,
        "TB": 2 ** 40,
    }

    size = size.upper()
    if not re.match(r" ", size):
        size = re.sub(r"([KMGT])", r" \1", size)
    number, unit = [string.strip() for string in size.split()]
    return int(float(number) * units[unit])
