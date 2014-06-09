# -*- coding: utf-8 -*-

import common
from Gmail import Gmail

USERNAME = ''
PASSWORD = ''

subject = '[活動] 2008-08-21 固定聚會'
content = '1234\n測試內容\n5678'


client = Gmail()


def test_login():
    assert client.login(USERNAME, PASSWORD)


def test_send():
    assert client.send(USERNAME, USERNAME, subject, content) == {}


def test_quit():
    assert client.quit()
