# coding: utf-8

import common
from Logger import Logger
from Config import Config
from Facebook import Facebook


logger = Logger('h4_create_fb_event').__new__()


if __name__ == '__main__':
    this_thursday = common.thisThursday()
    title = 'HackingThursday固定聚會(%s)' % this_thursday
    description = "地點：伯朗咖啡 (建國店)\n地址：台北市大安區建國南路一段 166 號\n(捷運忠孝新生站三號出口，沿忠孝東路走至建國南路右轉)\n\nWhat you can do in H4 :\n1. Code your code.\n2. Talk about OS, Programming, Hacking skills, Gossiping ...\n3. Meet new friends ~\n4. Hack and share anything !\n\nSee details :\nhttp://www.hackingthursday.org/\n\nWeekly Share :\nhttp://sync.in/h4"
    start_time = '%sT07:30:00-0400' % this_thursday
    end_time = '%sT10:00:00-0400' % this_thursday

    try:
        fb = Facebook(Config()['facebook']['access_token'], Config()['facebook']['username'], Config()['facebook']['password'])
        if fb.token:
            Config().Set('facebook', 'access_token', fb.token)

        event_id = fb.createEvent(Config()['facebook']['group_id'], title, description, start_time, end_time)

        if event_id:
            logger.info('http://www.facebook.com/events/' + event_id)
        else:
            logger.error('event create error')
    except:
        logger.error('error quit')
