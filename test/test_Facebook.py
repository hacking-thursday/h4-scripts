# -*- coding: utf-8 -*-

import common
from Config import Config
from Facebook import Facebook

username = Config()['facebook']['username']
password = Config()['facebook']['password']


token = ''
fb = Facebook()


def test_login():
    assert fb.login(username, password)


def test_get_token():
    token = fb.get_token()
    assert isinstance(token, str)
