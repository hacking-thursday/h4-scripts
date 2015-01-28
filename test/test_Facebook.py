# -*- coding: utf-8 -*-

from h4_scripts.lib.Config import Config
from h4_scripts.lib.Facebook import Facebook

username = Config()['facebook']['username']
password = Config()['facebook']['password']


token = ''
fb = Facebook()


def test_login():
    assert fb.login(username, password)


def test_get_token():
    token = fb.get_token()
    assert isinstance(token, str)
