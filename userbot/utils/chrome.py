# Copyright (C) 2021-2022 FastUserBot
# This file is a part of < https://github.com/FastUserBot/FastUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://github.com/FastUserBot/FastUserBot/blob/master/LICENSE/>.

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from userbot import CHROME_DRIVER, GOOGLE_CHROME_BIN, TEMP_DOWNLOAD_DIRECTORY


async def chrome(chrome_options=None):
    if chrome_options is None:
        chrome_options = await options()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.mkdir(TEMP_DOWNLOAD_DIRECTORY)
    prefs = {"download.default_directory": TEMP_DOWNLOAD_DIRECTORY}
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(executable_path=CHROME_DRIVER, options=chrome_options)


async def options():
    chrome_options = Options()
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    return chrome_options
