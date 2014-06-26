# -*- coding: utf-8 -*-

import common
from Config import Config
from PTT import PTT

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


# def test_post():
#     assert client.post(subject, content)


def test_quit():
    assert client.quit()
