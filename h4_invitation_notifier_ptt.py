#!/usr/bin/env python
# encoding: utf-8

import common
from lib.Logger import Logger
from lib.Config import Config
from lib.PTT import PTT

logger = Logger('h4_invitation_notifier_ptt').__new__()

config = Config()
ID = config['bbs']['user']
PASSWORD = config['bbs']['pass']
PartyDate = common.thisThursday()

board = 'Linux'
subject = 'HackingThursday 固定聚會 (%s)' % PartyDate
content = common.html2txt(common.get_wikidot_content_body('http://www.hackingthursday.org/invite'))

if __name__ == '__main__':
    ptt = PTT()

    if ptt.login(ID, PASSWORD):
        logger.info('login ptt')

    if ptt.enter(board):
        logger.info('enter %s board' % board)

    if ptt.post(subject, content):
        logger.info('post article')

    if ptt.quit():
        logger.info('quit ptt')
