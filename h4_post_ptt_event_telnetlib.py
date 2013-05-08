#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
import telnetlib
from Logger import Logger
from Config import Config

logger = Logger('bbs').__new__()

ID        = Config()['bbs']['user']
PASSWD    = Config()['bbs']['pass']
PartyDate = common.thisThursday()

Subject   = "HackingThursday 固定聚會 (" + PartyDate + ")"
Content   = common.html2txt(common.get_wikidot_content_body("http://www.hackingthursday.org/invite"))


def big5(str):
    return str.decode('utf-8', 'ignore').encode('big5', 'ignore')

tn = telnetlib.Telnet("ptt.cc")
tn.set_debuglevel(2)
tn.read_until("guest")
tn.write("%s\r%s\r" % (ID, PASSWD))

isMain = False
while not isMain:
    line = tn.read_very_eager()

    if big5("請勿頻繁登入以免造成系統過度負荷") in line:
        tn.write("\r")
    elif "[Y/n]" in line:
        tn.write("Y\r")
    elif big5("請按任意鍵繼續") in line:
        tn.write("\r")
    elif big5("分組討論區") in line:
        logger.info('bbs login')
        isMain = True

#tn.read_until(big5("分組討論區"))
tn.write("s")
#tn.write("Test\r")
tn.write("Linux\r")

tn.read_until(big5("請按任意鍵繼續"))
tn.write("\r")

logger.debug('enter board')

tn.read_until(big5("文章選讀"))
tn.write("")
tn.write("\r")
tn.write(big5("[活動] %s\r") % big5(Subject))  # Subject
# Content
for line in Content.split('\n'):
    tn.write("%s\r" % big5((line.rstrip())))
tn.write("")
tn.read_until(big5("確定要儲存檔案嗎"))
logger.debug('save sure?')
tn.write("S")
tn.write("\r")

tn.read_until(big5("任意鍵繼續"))
tn.write("\r")

logger.info('article post')

tn.read_until(big5("文章選讀"))
tn.write("eee")
tn.write("ee")
tn.write("g")
tn.write("\r")
tn.write("y")
tn.write("\r")
tn.write("\r\r")

logger.info('quit bbs')

sess_op = tn.read_all()
print sess_op
#logger.info(sess_op)
