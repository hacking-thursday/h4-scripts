# -*- coding: utf-8 -*-

import common
from Config import Config
from Gmail import Gmail

username = Config()['gmail']['username']
password = Config()['gmail']['password']

subject = Config()['test']['subject']
content = Config()['test']['html_content']


client = Gmail()


def test_login():
    assert client.login(username, password)


def test_send():
    assert client.send(username, username, subject, html=content) == {}


def test_quit():
    assert client.quit()
