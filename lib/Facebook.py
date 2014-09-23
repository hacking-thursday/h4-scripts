# coding:utf8

# get access token :
#     https://www.facebook.com/dialog/oauth?client_id=164519640405083&redirect_uri=http://www.facebook.com/connect/login_success.html&response_type=token
# grant permission :
#     https://www.facebook.com/dialog/oauth?client_id=164519640405083&redirect_uri=http://www.facebook.com/connect/login_success.html&scope=user_photos,ads_management,user_notes,user_relationships,user_religion_politics,user_education_history,user_activities,user_online_presence,user_status,user_photo_video_tags,user_location,user_checkins,user_likes,read_mailbox,xmpp_login,read_friendlists,read_requests,user_events,user_groups,user_website,user_birthday,user_relationship_details,user_videos,email,read_stream,user_interests,user_about_me,user_hometown,read_insights,user_work_history,create_event

import re
import urllib
import urllib2
import cookielib
import simplejson
import datetime
import dateutil.parser


# config variable
# CLIENT_ID = '120190928021712'  # yan_consoel_f_b_client
CLIENT_ID = '164519640405083'  # h4bot

# static variable
GRAPH_URL = 'https://graph.facebook.com'


class Facebook():
    def __init__(self):
        cj = cookielib.CookieJar()

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('Host', 'www.facebook.com'),
                             ('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'),
                             ('Referer', 'https://www.facebook.com/')]

        self.opener = opener

        usock = self.opener.open('http://www.facebook.com')

    def login(self, email, password):
        url = 'https://www.facebook.com/login.php?login_attempt=1'

        data = "locale=en_US&lsd=%s&lgnrnd=215019_4mpx&lgnjs=1400475025&email=%s&pass=%s" % ('AVoy-05c', email, password)

        usock = self.opener.open(url, data)
        line = usock.read()

        # print line

        if "Redirecting" in line or "Logout" in line:
            # print 'login to facebook'

            return True
        else:
            # print 'login failed'

            # print usock.read()

            return False

    def get_token(self):
        url = 'https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=http://www.facebook.com/connect/login_success.html&response_type=token' % CLIENT_ID
        usock = self.opener.open(url)

        line = usock.read()

        url = usock.url

        p = re.compile('access_token=([a-zA-Z0-9]+)&')
        token = p.findall(url)[0]

        # if token:
        #     print 'Access token : ',
        #     print token

        return token

    def logout(self):
        url = 'https://www.facebook.com/logout.php'

        usock = self.opener.open(url)

        line = usock.read()

    def get_facebook_id(self, url_name):
        try:
            facebook_id = self.get_group_id(url_name)

            if facebook_id:
                return facebook_id
        except:
            pass

        try:
            facebook_id = self.get_user_page_id(url_name)

            if facebook_id:
                return facebook_id
        except:
            pass

    def get_user_page_id(self, page_name):
        url = 'https://www.facebook.com/%s/' % page_name
        usock = self.opener.open(url)

        line = usock.read()

        p = re.compile('profile_owner&quot;:&quot;(\d+)&quot;,&quot;')
        found = p.findall(line)
        if found:
            id = found[0]

            print 'Facebook ID : ',
            print id

            return id

    def get_group_id(self, group_name):
        url = 'https://www.facebook.com/groups/%s/' % group_name
        usock = self.opener.open(url)

        line = usock.read()

        p = re.compile('"selectedKey":"group_(\d+)"')
        found = p.findall(line)
        if found:
            id = found[0]

            print 'Facebook Group ID : ',
            print id

            return id


class Graph():
    def __init__(self, access_token):
        self.token = access_token

    def getUID(self):
        query = '/me'
        data = 'fields=%s' % ('id')
        url = GRAPH_URL + query + '?access_token=' + self.token + '&' + data

        uid = None
        try:
            connection = urllib2.urlopen(url)
            response = connection.read()
            uid = int(simplejson.loads(response)['id'])
        finally:
            return uid

    def getNotifications(self):
        query = '/me/notifications'
        url = GRAPH_URL + query + '?access_token=' + self.token

        connection = urllib2.urlopen(url)
        response = connection.read()

        return simplejson.loads(response)

    def getPublishes(self, facebookid, limit=20):
        query = '/%s/feed' % (facebookid)
        data = 'fields=from,message,created_time,updated_time,link,description,id,comments,picture,name,actions,caption,type&limit=%s' % (limit)
        url = GRAPH_URL + query + '?access_token=' + self.token + '&' + data

        connection = urllib2.urlopen(url)
        response = connection.read()

        return simplejson.loads(response)

    # def getEvent(self, eventid):
    #     query = '/%s' % (eventid)
    #     data = 'fields=id,name,description,start_time,updated_time,location'
    #     url = GRAPH_URL + query + '?access_token=' + self.token + '&' + data
    #     # print url
    #
    #     connection = urllib2.urlopen(url)
    #     response = connection.read()
    #
    #     return simplejson.loads(response)

    def getEvent(self, event_id):
        query = '/v2.1/%s' % event_id
        url = GRAPH_URL + query + '?access_token=' + self.token

        connection = urllib2.urlopen(url)
        response = connection.read()

        event = {}
        json_data = simplejson.loads(response)
        if 'start_time' in json_data:
            event['start_datetime'] = dateutil.parser.parse(json_data['start_time']).strftime("%Y-%m-%d %H:%M:00")
        if 'end_time' in json_data:
            event['end_datetime'] = dateutil.parser.parse(json_data['end_time']).strftime("%Y-%m-%d %H:%M:00")
        if 'location' in json_data:
            event['place_name'] = json_data['location']
        if 'venue' in json_data:
            if 'name' in json_data['venue']:
                event['address'] = json_data['venue']['name']
            if 'street' in json_data['venue']:
                event['address'] = json_data['venue']['street']
            if 'latitude' in json_data['venue'] and 'longitude' in json_data['venue']:
                event['lat'] = json_data['venue']['latitude']
                event['lng'] = json_data['venue']['longitude']

        return event

    def createEvent(self, facebookid, title, description, start_time, end_time):
        query = '/events'
        url = GRAPH_URL + '/' + facebookid + query

        data = urllib.urlencode({'access_token': self.token,
                                 'name': title,
                                 'description': description,
                                 'start_time': start_time,  # 2013-09-13T07:30:00-0400  (19:30)
                                 'end_time': end_time})  # 2013-09-13T22:00:00-0400  (22:00)

        event_id = ''
        try:
            req = urllib2.Request(url, data)
            connection = urllib2.urlopen(req)
            response = connection.read()
            event_id = simplejson.loads(response)['id']
        finally:
            return event_id

    def getGroups(self):
        query = '/me/groups'
        url = GRAPH_URL + query + '?access_token=' + self.token

        connection = urllib2.urlopen(url)
        response = connection.read()
        group_data = simplejson.loads(response)
        groups = [{'id': group['id'], 'name': group['name']} for group in group_data['data']]

        while 'paging' in group_data and 'next' in group_data['paging']:
            connection = urllib2.urlopen(group_data['paging']['next'])
            response = connection.read()
            group_data = simplejson.loads(response)
            groups = groups + [{'id': group['id'], 'name': group['name']} for group in group_data['data']]

        return groups

    def getRecentEvents(self, facebook_id):
        query = '/v2.1/%s/events' % facebook_id
        url = GRAPH_URL + query + '?access_token=' + self.token

        connection = urllib2.urlopen(url)
        response = connection.read()

        events = []
        if 'data' in simplejson.loads(response):
            for event in simplejson.loads(response)['data']:
                if dateutil.parser.parse(event['start_time']).strftime("%Y-%m-%d %H:%M:00") > datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00"):
                    _ = {}
                    _['name'] = event['name']
                    _['start_datetime'] = dateutil.parser.parse(event['start_time']).strftime("%Y-%m-%d %H:%M:00")
                    if 'end_time' in event:
                        _['end_datetime'] = dateutil.parser.parse(event['end_time']).strftime("%Y-%m-%d %H:%M:00")
                    _['url'] = 'https://www.facebook.com/events/%s' % event['id']

                    events.append(_)

        return events

    def getPastEvents(self, facebook_id):
        query = '/v2.1/%s/events' % facebook_id
        url = GRAPH_URL + query + '?access_token=' + self.token

        connection = urllib2.urlopen(url)
        response = connection.read()

        events = []
        if 'data' in simplejson.loads(response):
            for event in simplejson.loads(response)['data']:
                if dateutil.parser.parse(event['start_time']).strftime("%Y-%m-%d %H:%M:00") < datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00"):
                    _ = {}
                    _['name'] = event['name']
                    _['start_datetime'] = dateutil.parser.parse(event['start_time']).strftime("%Y-%m-%d %H:%M:00")
                    if 'end_time' in event:
                        _['end_datetime'] = dateutil.parser.parse(event['end_time']).strftime("%Y-%m-%d %H:%M:00")
                    _['url'] = 'https://www.facebook.com/events/%s' % event['id']

                    events.append(_)

        return events
