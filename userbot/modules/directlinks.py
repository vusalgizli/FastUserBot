# Copyright (C) 2021-2022 FastUserBot
# This file is a part of < https://www.github.com/FastUserBot/FastUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FastUserBot/FastUserBot/blob/master/LICENSE/>.

from os import popen
import re
import ast
import urllib.parse
import json
from random import choice
import requests
from bs4 import BeautifulSoup
from humanize import naturalsize

from userbot import CMD_HELP
from userbot.events import register


@register(fast=True, pattern=r"^\.direct(?: |$)([\s\S]*)")
async def directlinks(request):
    """ FastUserBot """
    await request.edit("`Hazırlanır biraz gözləyin...`")
    textx = await request.get_reply_message()
    mesaj = request.pattern_match.group(1)
    if mesaj:
        pass
    elif textx:
        mesaj = textx.text
    else:
        await request.edit("`İstifadəsi: .direct <link>`")
        return
    fast = ''
    links = re.findall(r'\bhttps?://.*\.\S+', mesaj)
    if not links:
        fast = "`Bağışlayın, heç nə tapa bilmədim!`"
        await request.edit(fast)
    for link in links:
        if 'drive.google.com' in link:
            fast += gdrive(link)
        elif 'zippyshare.com' in link:
            fast += zippy_share(link)
        elif 'mega.' in link:
            fast += mega_dl(link)
        elif 'yadi.sk' in link:
            fast += yandex_disk(link)
        elif 'cloud.mail.ru' in link:
            fast += cm_ru(link)
        elif 'mediafire.com' in link:
            fast += mediafire(link)
        elif 'sourceforge.net' in link:
            fast += sourceforge(link)
        elif 'osdn.net' in link:
            fast += osdn(link)
        elif 'github.com' in link:
            fast += github(link)
        elif 'androidfilehost.com' in link:
            fast += androidfilehost(link)
        else:
            fast += re.findall(r"\bhttps?://(.*?[^/]+)",
                                link)[0] + ' dəstəklənmir!'
    await request.edit(cyber)


def gdrive(url: str) -> str:
    """ GDrive üçün """
    drive = 'https://drive.google.com'
    try:
        link = re.findall(r'\bhttps?://drive\.google\.com\S+', url)[0]
    except IndexError:
        fast = "`Google Drive linki tapılmadı!`\n"
        return fast
    file_id = ''
    fast = ''
    if link.find("view") != -1:
        file_id = link.split('/')[-2]
    elif link.find("open?id=") != -1:
        file_id = link.split("open?id=")[1].strip()
    elif link.find("uc?id=") != -1:
        file_id = link.split("uc?id=")[1].strip()
    url = f'{drive}/uc?export=download&id={file_id}'
    download = requests.get(url, stream=True, allow_redirects=False)
    cookies = download.cookies
    try:
        # In case of small file size, Google downloads directly
        dl_url = download.headers["location"]
        if 'accounts.google.com' in dl_url:  # non-public file
            fast += '`Link açıq deyil!`\n'
            return reply
        name = 'Birbaşa yükləmə linki'
    except KeyError:
        # In case of download warning page
        page = BeautifulSoup(download.content, 'lxml')
        export = drive + page.find('a', {'id': 'uc-download-link'}).get('href')
        name = page.find('span', {'class': 'uc-name-size'}).text
        response = requests.get(export,
                                stream=True,
                                allow_redirects=False,
                                cookies=cookies)
        dl_url = response.headers['location']
        if 'accounts.google.com' in dl_url:
            reply += 'Link açıq deyil!'
            return reply
    reply += f'[{name}]({dl_url})\n'
    return reply


def zippy_share(url: str) -> str:
    """ ZippyShare birbasa yukleme linki
    credits: https://github.com/LameLemon/ziggy"""
    fast = ''
    dl_url = ''
    try:
        link = re.findall(r'\bhttps?://.*zippyshare\.com\S+', url)[0]
    except IndexError:
        fast = "`ZippyShare linki aşkar edilmədi!`\n"
        return reply
    session = requests.Session()
    base_url = re.search('http.+.com', link).group()
    response = session.get(link)
    page_soup = BeautifulSoup(response.content, "lxml")
    scripts = page_soup.find_all("script", {"type": "text/javascript"})
    for script in scripts:
        if "getElementById('dlbutton')" in script.text:
            url_raw = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);',
                                script.text).group('url')
            math = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);',
                             script.text).group('math')
            dl_url = url_raw.replace(math, '"' + str(ast.literal_eval(math)) + '"')
            break
    dl_url = base_url + ast.literal_eval(dl_url)
    name = urllib.parse.unquote(dl_url.split('/')[-1])
    reply += f'[{name}]({dl_url})\n'
    return reply


def yandex_disk(url: str) -> str:
    """ Yandex.Disk ucun link qısaldıcı
    credits: https://github.com/wldhx/yadisk-direct"""
    reply = ''
    try:
        link = re.findall(r'\bhttps?://.*yadi\.sk\S+', url)[0]
    except IndexError:
        fast = "`Yandex.Disk linki aşkar edilmədi!`\n"
        return fast
    api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
    try:
        dl_url = requests.get(api.format(link)).json()['href']
        name = dl_url.split('filename=')[1].split('&disposition')[0]
        fast += f'[{name}]({dl_url})\n'
    except KeyError:
        fast += '`Xəta: Fayl tapılmadı / Endirmə həddinə çatdı.`\n'
        return fast
    return fast


def mega_dl(url: str) -> str:
    """ MEGA.nz ucun
    credits: https://github.com/tonikelope/megadown"""
    fast = ''
    try:
        link = re.findall(r'\bhttps?://.*mega.*\.nz\S+', url)[0]
    except IndexError:
        fast = "`MEGA.nz linki aşkar edilmədi!`\n"
        return fast
    command = f'bin/megadown -q -m {link}'
    result = popen(command).read()
    try:
        data = json.loads(result)
        print(data)
    except json.JSONDecodeError:
        reply += "`Xəta: Bağlantı çıxarıla bilmir`\n"
        return fast
    dl_url = data['url']
    name = data['file_name']
    size = naturalsize(int(data['file_size']))
    fast += f'[{name} ({size})]({dl_url})\n'
    return fast


def cm_ru(url: str) -> str:
    """ cloud.mail.ru direct links generator
    Using https://github.com/JrMasterModelBuilder/cmrudl.py"""
    reply = ''
    try:
        link = re.findall(r'\bhttps?://.*cloud\.mail\.ru\S+', url)[0]
    except IndexError:
        reply = "`cloud.mail.ru linki aşkar edilmədi!`\n"
        return reply
    command = f'bin/cmrudl -s {link}'
    result = popen(command).read()
    result = result.splitlines()[-1]
    try:
        data = json.loads(result)
    except json.decoder.JSONDecodeError:
        reply += "`Xəta: Bağlantı çıxarıla bilmir`\n"
        return reply
    dl_url = data['download']
    name = data['file_name']
    size = naturalsize(int(data['file_size']))
    reply += f'[{name} ({size})]({dl_url})\n'
    return reply


def mediafire(url: str) -> str:
    """ MediaFire direct links generator """
    try:
        link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
    except IndexError:
        fast = "`MediaFire linki aşkar edilmədi!`\n"
        return fast
    fast = ''
    page = BeautifulSoup(requests.get(link).content, 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    dl_url = info.get('href')
    size = re.findall(r'\(.*\)', info.text)[0]
    name = page.find('div', {'class': 'filename'}).text
    fast += f'[{name} {size}]({dl_url})\n'
    return fast


def sourceforge(url: str) -> str:
    """ SourceForge direct links generator """
    try:
        link = re.findall(r'\bhttps?://.*sourceforge\.net\S+', url)[0]
    except IndexError:
        fast = "`SourceForge linki aşkar edilmədi!`\n"
        return fast
    file_path = re.findall(r'files(.*)/download', link)[0]
    fast = f" __{file_path.split('/')[-1]}__ üçün\n"
    project = re.findall(r'projects?/(.*?)/files', link)[0]
    mirrors = f'https://sourceforge.net/settings/mirror_choices?' \
        f'projectname={project}&filename={file_path}'
    page = BeautifulSoup(requests.get(mirrors).content, 'html.parser')
    info = page.find('ul', {'id': 'mirrorList'}).findAll('li')
    for mirror in info[1:]:
        name = re.findall(r'\((.*)\)', mirror.text.strip())[0]
        dl_url = f'https://{mirror["id"]}.dl.sourceforge.net/project/{project}/{file_path}'
        fast += f'[{name}]({dl_url}) '
    return fast


def osdn(url: str) -> str:
    """ OSDN """
    osdn_link = 'https://osdn.net'
    try:
        link = re.findall(r'\bhttps?://.*osdn\.net\S+', url)[0]
    except IndexError:
        fast = "`OSDN linki aşkar edilmədi!`\n"
        return fast
    page = BeautifulSoup(
        requests.get(link, allow_redirects=True).content, 'lxml')
    info = page.find('a', {'class': 'mirror_link'})
    link = urllib.parse.unquote(osdn_link + info['href'])
    fast = f" __{link.split('/')[-1]}__ üçün\n"
    mirrors = page.find('form', {'id': 'mirror-select-form'}).findAll('tr')
    for data in mirrors[1:]:
        mirror = data.find('input')['value']
        name = re.findall(r'\((.*)\)', data.findAll('td')[-1].text.strip())[0]
        dl_url = re.sub(r'm=(.*)&f', f'm={mirror}&f', link)
        fast += f'[{name}]({dl_url}) '
    return fast


def github(url: str) -> str:
    """ GitHub direct links generator """
    try:
        link = re.findall(r'\bhttps?://.*github\.com.*releases\S+', url)[0]
    except IndexError:
        fast = "`Heç bir GitHub Buraxılış əlaqəsi tapılmadı.`\n"
        return fast
    fast = ''
    dl_url = ''
    download = requests.get(url, stream=True, allow_redirects=False)
    try:
        dl_url = download.headers["location"]
    except KeyError:
        fast += "`Xəta: Linki açmaq olmur`\n"
    name = link.split('/')[-1]
    fast += f'[{name}]({dl_url}) '
    return fast


def androidfilehost(url: str) -> str:
    """ AFH direct links generator """
    try:
        link = re.findall(r'\bhttps?://.*androidfilehost.*fid.*\S+', url)[0]
    except IndexError:
        reply = "`AFH aşkar edilmədi`\n"
        return reply
    fid = re.findall(r'\?fid=(.*)', link)[0]
    session = requests.Session()
    user_agent = useragent()
    headers = {'user-agent': user_agent}
    res = session.get(link, headers=headers, allow_redirects=True)
    headers = {
        'origin': 'https://androidfilehost.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': user_agent,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-mod-sbb-ctype': 'xhr',
        'accept': '*/*',
        'referer': f'https://androidfilehost.com/?fid={fid}',
        'authority': 'androidfilehost.com',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'submit': 'submit',
        'action': 'getdownloadmirrors',
        'fid': f'{fid}'
    }
    mirrors = None
    reply = ''
    error = "`Xəta: Can't find Mirrors for the link`\n"
    try:
        req = session.post(
            'https://androidfilehost.com/libs/otf/mirrors.otf.php',
            headers=headers,
            data=data,
            cookies=res.cookies)
        mirrors = req.json()['MIRRORS']
    except (json.decoder.JSONDecodeError, TypeError):
        reply += error
    if not mirrors:
        reply += error
        return reply
    for item in mirrors:
        name = item['name']
        dl_url = item['url']
        reply += f'[{name}]({dl_url}) '
    return reply


def useragent():
    """
    useragent təsadüfi qurucu
    """
    useragents = BeautifulSoup(
        requests.get(
            'https://developers.whatismybrowser.com/'
            'useragents/explore/operating_system_name/android/').content,
        'lxml').findAll('td', {'class': 'useragent'})
    user_agent = choice(useragents)
    return user_agent.text
