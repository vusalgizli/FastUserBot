# Copyright (C) 2021-2022 FastUserBot
# This file is a part of < https://github.com/FastUserBot/FastUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://github.com/FastUserBot/FastUserBot/blob/master/LICENSE/>.

from pydrive.auth import GoogleAuth


def main():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("secret.json")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("secret.json")


if __name__ == '__main__':
    main()
