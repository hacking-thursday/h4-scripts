#!/usr/bin/env python
# encoding: utf-8

import common
from Logger import Logger
from lib.Config import Config
from lib.Facebook import Facebook, Graph

logger = Logger('h4_create_fb_event').__new__()

config = Config()
username = config['facebook']['username']
password = config['facebook']['password']
facebook_group_id = config['facebook']['group_id']

this_thursday = common.thisThursday()
title = 'HackingThursday固定聚會(%s)' % this_thursday
description = "地點：伯朗咖啡 (建國店)\n地址：台北市大安區建國南路一段 166 號\n(捷運忠孝新生站三號出口，沿忠孝東路走至建國南路右轉)\n\nWhat you can do in H4 :\n1. Code your code.\n2. Talk about OS, Programming, Hacking skills, Gossiping ...\n3. Meet new friends ~\n4. Hack and share anything !\n\nSee details :\nhttp://www.hackingthursday.org/\n\nWeekly Share :\nhttp://sync.in/h4"
start_time = '%sT07:30:00-0400' % this_thursday
end_time = '%sT10:00:00-0400' % this_thursday


def check_token():
    graph = Graph(config['facebook']['access_token'])

    if graph.getUID():
        logger.info('valid token')
        return config['facebook']['access_token']
    else:
        logger.info('invalid token, try get new one')
        fb = Facebook()
        if fb.login(username, password):
            logger.info('login success')
            token = fb.get_token()
            if token:
                logger.info('get new token')
                config.Set('facebook', 'access_token', token)
                return token
            else:
                logger.error('get token failed')
        else:
            logger.info('login failed')

    return False

if __name__ == '__main__':
    token = check_token()
    if token:
        graph = Graph(token)

        event_id = graph.createEvent(facebook_group_id, title, description, start_time, end_time)

        if event_id:
            logger.info('http://www.facebook.com/events/' + event_id)
        else:
            logger.error('event create error')
