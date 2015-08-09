# -*- coding: utf-8 -*-

import os
from h4_scripts.Config import Config
from h4_scripts.Facebook import Facebook

username = os.environ['FACEBOOK_USERNAME'] if os.environ.get('FACEBOOK_USERNAME') else Config()['facebook']['username']
password = os.environ['FACEBOOK_PASSWORD'] if os.environ.get('FACEBOOK_PASSWORD') else Config()['facebook']['password']


token = ''
fb = Facebook()


def test_login():
    assert fb.login(username, password)


def test_get_token():
    token = fb.get_token()
    assert isinstance(token, str)
