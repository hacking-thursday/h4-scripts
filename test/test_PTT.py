# -*- coding: utf-8 -*-

import os
from h4_scripts.Config import Config
from h4_scripts.PTT import PTT

DRY_RUN = True if os.environ.get('DRY_RUN') == 'True' else False

id = os.environ['BBS_USER'] if os.environ.get('BBS_USER') else Config()['bbs']['user']
password = os.environ['BBS_PASS'] if os.environ.get('BBS_PASS') else Config()['bbs']['pass']

board = 'Test'  # 討論版名稱
subject = os.environ['TEST_SUBJECT'] if os.environ.get('TEST_SUBJECT') else Config()['test']['subject']
content = os.environ['TEST_HTML_CONTENT'] if os.environ.get('TEST_HTML_CONTENT') else Config()['test']['content']


client = PTT()


def test_login():
    assert client.login(id, password)


def test_enter():
    assert client.enter(board)


def test_post():
    assert client.post(subject, content, dry_run=DRY_RUN)


def test_quit():
    assert client.quit()
