# -*- coding: utf-8 -*-

import os
from h4_scripts.lib.Config import Config
from h4_scripts.lib.PTT import PTT

DRY_RUN = True if os.environ.get('DRY_RUN') == 'True' else False

id = Config()['bbs']['user']
password = Config()['bbs']['pass']

board = 'Test'  # 討論版名稱
subject = Config()['test']['subject']
content = Config()['test']['content']


client = PTT()


def test_login():
    assert client.login(id, password)


def test_enter():
    assert client.enter(board)


def test_post():
    assert client.post(subject, content, dry_run=DRY_RUN)


def test_quit():
    assert client.quit()
