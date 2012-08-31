# -*- coding: utf-8 -*-

import urllib2
import cookielib
import re
import urllib
import common
from Config import Config
from Logger import Logger


USERNAME = Config()['facebook']['username']
PASSWORD = Config()['facebook']['password']
DEBUG = int(Config()['other']['debug'])

logger = Logger('facebook_unofficial_api').__new__()


class Facebook():
    def __init__(self):
        cj = cookielib.CookieJar()

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('Referer', 'http://login.facebook.com/login.php'),
                            ('Content-Type', 'application/x-www-form-urlencoded'),
                            ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)')]
        self.opener = opener

        usock = self.opener.open('http://www.facebook.com')

        #if DEBUG:
        #    line = usock.read()
        #    print line

    def _getlsd(self):
        url = 'http://www.facebook.com/login.php?login_attempt=1'

        usock = self.opener.open(url)

        line = usock.read()
        lsd = re.findall('name="lsd" value="(\w+)" auto', line)[0]

        return lsd

    def login(self):
        url = 'https://login.facebook.com/login.php?login_attempt=1'
        data = "locale=en_US&non_com_login=&email=%s&pass=%s&lsd=%s" % (USERNAME, PASSWORD, self._getlsd())  # 'AVpNwXkC')

        usock = self.opener.open('http://www.facebook.com')
        usock = self.opener.open(url, data)
        line = usock.read()

        #print line

        if "Log Out" in line:
            #print "Logged in."

            return True
        else:
            #print "failed login"
            #print usock.read()

            return False

    def getUID(self):
        url = 'http://www.facebook.com/'

        usock = self.opener.open(url)

        line = usock.read()
        uid = re.findall('envFlush\({"user":"(\d+)",', line)[0]

        return uid

    def _getfb_dtsg(self):
        url = 'http://www.facebook.com/events/create/?gid=161774120511261'

        usock = self.opener.open(url)

        line = usock.read()
        dtsg = re.findall('lag":2,"fb_dtsg":"(\w+)","ajax', line)[0]

        return dtsg

    def create_event(self):
        url = 'http://www.facebook.com/ajax/plans/create/save.php'
        data = urllib.urlencode({'fb_dtsg': self._getfb_dtsg(),  # 'AQCfQbPn',
                                 'title': 'HackingThursday固定聚會(%s)' % (common.thisThursday()),
                                 'details': '通告網址: http://www.hackingthursday.org/invite',
                                 'location_id': '154788921241520',  # MarketPlace
                                 #'when_dateIntlDisplay': '9/4/2012',
                                 #'when_date': '9/4/2012',
                                 'when_dateIntlDisplay': common.thisThursday_fb_format(),
                                 'when_date': common.thisThursday_fb_format(),
                                 'when_time': '70200',
                                 'when_time_display_time': '7:30 pm',
                                 'when_timezone': 'Asia/Taipei',
                                 #'end_when_dateIntlDisplay': '9/4/2012',
                                 #'end_when_date': '9/4/2012',
                                 'end_when_dateIntlDisplay': common.thisThursday_fb_format(),  # '8/30/2012',
                                 'end_when_date': common.thisThursday_fb_format(),  # '8/30/2012',
                                 'end_when_time': '79200',
                                 'end_when_time_display_time': '10:00 pm',
                                 'pre_end_when_timestamp': '0',
                                 'guest_invite': 'on',
                                 'guest_list': 'on',
                                 'object_id': '161774120511261',  # Hacking Thursday Group
                                 #'object_id': '126789270714326',  # iteamjob Group
                                 'invite_group_members': 'on',
                                 #'__user': '1801815672',
                                 '__a': '1'})
        if DEBUG:
            print data

        usock = self.opener.open(url, data)

        line = usock.read()

        if DEBUG:
            print line

        match = re.search(r'events\\\\\\\/(\d+)\\\\\\\/\?context=create', line)

        if match:
            return match.group(1)
        else:
            return False
