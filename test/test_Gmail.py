# -*- coding: utf-8 -*-

from h4_scripts.lib.Config import Config
from h4_scripts.lib.Gmail import Gmail

username = Config()['gmail']['username']
password = Config()['gmail']['password']

subject = Config()['test']['subject']
content = Config()['test']['html_content']


client = Gmail()


def test_login():
    assert client.login(username, password)


# def test_send():
#     assert client.send(username, username, subject, html=content) == {}


def test_quit():
    assert client.quit()
