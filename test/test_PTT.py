# -*- coding: utf-8 -*-

import common
from PTT import PTT

ID = ''
PASSWORD = ''

board = 'Test'
subject = '[活動] 2008-08-21 固定聚會'
content = '1234\n測試內容\n5678'


client = PTT()


def test_login():
    assert client.login(ID, PASSWORD)


def test_enter():
    assert client.enter(board)


def test_post():
    assert client.post(subject, content)


def test_quit():
    assert client.quit()
