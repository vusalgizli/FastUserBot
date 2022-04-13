# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FatsUserBot/FastUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FastUserBot/FastUserBot/blob/master/LICENSE/>.

FROM fastuserbot/fastuserbot:latest
RUN git clone https://github.com/fastuserbot/fastuserbot /root/fastuserbot
WORKDIR /root/fastuserbot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]
