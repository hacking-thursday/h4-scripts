# -*- coding: utf-8 -*-

import os
from h4_scripts.Config import Config
from h4_scripts.Gmail import Gmail

DRY_RUN = True if os.environ.get('DRY_RUN') == 'True' else False

username = os.environ['GMAIL_USERNAME'] if os.environ.get('GMAIL_USERNAME') else Config()['gmail']['username']
password = os.environ['GMAIL_PASSWORD'] if os.environ.get('GMAIL_PASSWORD') else Config()['gmail']['password']

subject = os.environ['TEST_SUBJECT'] if os.environ.get('TEST_SUBJECT') else Config()['test']['subject']
content = os.environ['TEST_HTML_CONTENT'] if os.environ.get('TEST_HTML_CONTENT') else Config()['test']['html_content']

client = Gmail()


def test_login():
    assert client.login(username, password)


def test_send():
    assert client.send(username, username, subject, html=content, dry_run=DRY_RUN)


def test_quit():
    assert client.quit()
