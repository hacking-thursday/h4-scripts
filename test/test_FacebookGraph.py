# -*- coding: utf-8 -*-

import os
from h4_scripts.Config import Config
from h4_scripts.Facebook import Facebook, Graph

username = os.environ['FACEBOOK_USERNAME'] if os.environ.get('FACEBOOK_USERNAME') else Config()['facebook']['username']
password = os.environ['FACEBOOK_PASSWORD'] if os.environ.get('FACEBOOK_PASSWORD') else Config()['facebook']['password']

fb = Facebook()
fb.login(username, password)
token = fb.get_token()
graph = Graph(token)


def test_get_uid():
    assert isinstance(graph.getUID(), int)


def test_get_groups():
    assert isinstance(graph.getGroups(), list)


def test_get_group_event():
    assert isinstance(graph.getRecentEvents('468945293170945'), list)
