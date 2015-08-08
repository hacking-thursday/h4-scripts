# -*- coding: utf-8 -*-

from h4_scripts.Config import Config
from h4_scripts.Facebook import Facebook, Graph

username = Config()['facebook']['username']
password = Config()['facebook']['password']

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
