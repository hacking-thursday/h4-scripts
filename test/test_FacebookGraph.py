# -*- coding: utf-8 -*-

import common
from Config import Config
from Facebook import Facebook, Graph

username = Config()['facebook']['username']
password = Config()['facebook']['password']


fb = Facebook()
fb.login(username, password)
token = fb.get_token()
graph = Graph(token)


def test_get_uid():
    assert isinstance(graph.getUID(), int)
