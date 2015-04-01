# -*- coding: utf-8 -*-

import os
from h4_scripts.lib.Config import Config
from h4_scripts.lib.Gmail import Gmail

DRY_RUN = True if os.environ.get('DRY_RUN') == 'True' else False

username = Config()['gmail']['username']
password = Config()['gmail']['password']

subject = Config()['test']['subject']
content = Config()['test']['html_content']

client = Gmail()


def test_login():
    assert client.login(username, password)


def test_send():
    assert client.send(username, username, subject, html=content, dry_run=DRY_RUN)


def test_quit():
    assert client.quit()
