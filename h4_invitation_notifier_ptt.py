# -*- coding: utf-8 -*-

import common
from Config import Config
from lib.PTT import PTT

ID = Config()['bbs']['user']
PASSWORD = Config()['bbs']['pass']
PartyDate = common.thisThursday()

board = 'Linux'
subject = 'HackingThursday 固定聚會 (' + PartyDate + ')'
content = common.html2txt(common.get_wikidot_content_body('http://www.hackingthursday.org/invite'))

if __name__ == '__main__':
    ptt = PTT(ID, PASSWORD)
    ptt.enter(board)
    ptt.post(subject, content)
    ptt.quit()
