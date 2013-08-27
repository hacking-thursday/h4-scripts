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
        opener.addheaders = [('Referer', 'http://m.facebook.com/'),
                            ('Content-Type', 'application/x-www-form-urlencoded'),
                            ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)')]
        self.opener = opener

        usock = self.opener.open('http://m.facebook.com')

    def login(self):
        url = 'https://m.facebook.com/login.php'

        data = "email=%s&pass=%s" % (USERNAME, PASSWORD)

        usock = self.opener.open(url, data)
        line = usock.read()

        # print line

        if "Logout" in line:
            logger.info('logged in')

            return True
        else:
            logger.info('failed login')

            #print usock.read()

            return False

    def getAccessToken(self):
        usock = self.opener.open('https://developers.facebook.com/tools/access_token/')

        line = usock.read()

        token = re.findall('<code>(\w+)</code>', line)[0]

        return token
