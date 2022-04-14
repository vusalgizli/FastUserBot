# Copyright (C) 2021-2022 FastUserBot
# This file is a part of < # <https://www.github.com/FastUserBot/FastUserBot/blob/master/LICENSE/>.
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FastUserBot/FastUserBot/blob/master/LICENSE/>.

FROM fastuserbot/fastspaceaz:latest
RUN git clone https://github.com/fastuserbot/fastuserbot /root/fastuserbot
WORKDIR /root/fastuserbot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]
