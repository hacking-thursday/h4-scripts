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


# config variable
# CLIENT_ID = '120190928021712'  # yan_consoel_f_b_client
CLIENT_ID = '164519640405083'  # h4bot

# static variable
GRAPH_URL = 'https://graph.facebook.com'


class Facebook():
    def __init__(self, access_token=None, email=None, password=None):
        cj = cookielib.CookieJar()

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('Referer', 'http://m.facebook.com/'),
                            ('Content-Type', 'application/x-www-form-urlencoded'),
                            ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)')]

        self.opener = opener

        usock = self.opener.open('http://m.facebook.com')

        # 嘗試確定快取 Token 可用
        if access_token:
            self.token = access_token

            self.uid = self.getUID()

            if self.uid:
                print 'use token'
                return

        # 重新獲取 Token
        if self._login(email, password):
            self.token = self._getToken()

            self.uid = self.getUID()

            if self.uid:
                print 'login to facebook'
                return
            else:
                raise Exception("get uid error")
        else:
            raise Exception("login to Facebook error")

    def _login(self, email, passwd):
        url = 'https://m.facebook.com/login.php'

        data = "email=%s&pass=%s" % (email, passwd)

        usock = self.opener.open(url, data)
        line = usock.read()

        # print line

        if "Logout" in line:
            # print 'logged in'

            return True
        else:
            # print 'failed login'

            #print usock.read()

            return False

    def _getToken(self):
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

    def getUID(self):
        query = '/me'
        data = 'fields=%s' % ('id')
        url = GRAPH_URL + query + '?access_token=' + self.token + '&' + data

        uid = ''
        try:
            connection = urllib2.urlopen(url)
            response = connection.read()
            uid = simplejson.loads(response)['id']
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

    def getEvent(self, eventid):
        query = '/%s' % (eventid)
        data = 'fields=id,name,description,start_time,updated_time,location'
        url = GRAPH_URL + query + '?access_token=' + self.token + '&' + data
        # print url

        connection = urllib2.urlopen(url)
        response = connection.read()

        return simplejson.loads(response)

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
