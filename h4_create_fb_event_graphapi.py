# coding: utf-8

import common
from Logger import Logger
from Config import Config
import urllib
import urllib2
import json

logger = Logger('fb').__new__()


class FacebookGraph():
    # get access token :
    #     https://www.facebook.com/dialog/oauth?client_id=164519640405083&redirect_uri=http://www.facebook.com/connect/login_success.html&response_type=token
    # grant permission :
    #     https://www.facebook.com/dialog/oauth?client_id=164519640405083&redirect_uri=http://www.facebook.com/connect/login_success.html&scope=user_photos,ads_management,user_notes,user_relationships,user_religion_politics,user_education_history,user_activities,user_online_presence,user_status,user_photo_video_tags,user_location,user_checkins,user_likes,read_mailbox,xmpp_login,read_friendlists,read_requests,user_events,user_groups,user_website,user_birthday,user_relationship_details,user_videos,email,read_stream,user_interests,user_about_me,user_hometown,read_insights,user_work_history,create_event

    def __init__(self):
        self.GRAPH_URL = "https://graph.facebook.com/"

        self.ACCESS_TOKEN = Config()['facebook']['access_token']
        self.id = Config()['facebook']['group_id']  # '126789270714326'

    def create_event(self, title, description, start_time, end_time):
        _query = '/events'
        url = self.GRAPH_URL + self.id + _query

        data = urllib.urlencode({'name': title,
                        'description': description,
                        'start_time': start_time,
                        'end_time': end_time,
                        'access_token': self.ACCESS_TOKEN})

        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        the_page = response.read()

        try:
            logger.info('http://www.facebook.com/events/%s' % json.loads(the_page)['id'])
        except:
            logger.error('fb event create failed.')


if __name__ == '__main__':
    this_thursday = common.thisThursday()
    title = 'HackingThursday固定聚會(%s)' % this_thursday
    description = "地點：伯朗咖啡 (建國店)\n地址：台北市大安區建國南路一段 166 號 3 樓\n(捷運忠孝新生站三號出口，沿忠孝東路走至建國南路右轉)\n\nWhat you can do in H4 :\n1. Code your code.\n2. Talk about OS, Programming, Hacking skills, Gossiping ...\n3. Meet new friends ~\n4. Hack and share anything !\n\nSee details :\nhttp://www.hackingthursday.org/\n\nWeekly Share :\nhttp://sync.in/h4"
    start_time = '%sT07:30:00-0400' % this_thursday
    end_time = '%sT10:00:00-0400' % this_thursday

    fb = FacebookGraph()
    fb.create_event(title, description, start_time, end_time)
