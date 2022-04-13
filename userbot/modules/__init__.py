# Copyright (C) 2021-2022 FastUserBot
# This file is a part of < https://github.com/FastUserbBot/FastUserBot/ >
# PLease read the GNU General Public License v3.0 in
# <https://github.com/FastUserbBot/FastUserBot/blob/master/LICENSE/>.

from userbot import LOGS

def __list_all_modules():
    from os.path import dirname, basename, isfile
    import glob

    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [
        basename(f)[:-3] for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]
    return all_modules


ALL_MODULES = sorted(__list_all_modules())
LOGS.info("Yüklənəcək modullar: %s", str(ALL_MODULES))
__all__ = ALL_MODULES + ["ALL_MODULES"]
