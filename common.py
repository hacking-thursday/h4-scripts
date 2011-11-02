#!/usr/bin/env python
# coding:utf8
#
# Author: Chun-Yu Lee (Mat) <matlinuxer2@gmail.com>
# Copyright: Chun-Yu Lee (Mat) <matlinuxer2@gmail.com>
# License: MIT 
#

import datetime

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import os
import ConfigParser

import libxml2
import StringIO

import tempfile
import html2text

def thisThursday():
    delta_days = 4 - datetime.date.today().isoweekday()
    this_thursday = datetime.date.today() + datetime.timedelta( days=delta_days )
    return this_thursday.isoformat()

def nextThursday():
    this_thursday_str = thisThursday()
    this_thursday = datetime.datetime.strptime( this_thursday_str, "%Y-%m-%d" )
    next_thursday = this_thursday + datetime.timedelta( days=7 )
    result = next_thursday.date().isoformat()
    return result

def prevThursday():
    this_thursday_str = thisThursday()
    this_thursday = datetime.datetime.strptime( this_thursday_str, "%Y-%m-%d" )
    prev_thursday = this_thursday + datetime.timedelta( days=-7 )
    result = prev_thursday.date().isoformat()
    return result

def isThursday( date_str ):
    this_day = datetime.datetime.strptime( date_str, "%Y-%m-%d").date()
    result = ( this_day.isoweekday() == 4 )
    return result


#
# send_gmail("matlinuxer2@gmail.com", "matlinuxer2@gmail.com", "Hello from python!", "<hr/><h1>hello from python</h1><hr/>", "USERNAME", "PASSWORD")
#
def send_gmail( sender, recipient, subject, text, html, username, passwd ):
   msg = MIMEMultipart("alternative")

   msg['Subject'] = subject
   msg['From'] = sender
   msg['To'] = recipient 

   msg.attach( MIMEText(text,"plain", "utf-8") )
   msg.attach( MIMEText(html,"html", "utf-8") )

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login( username, passwd )
   mailServer.sendmail( sender, recipient, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()



##################
## Settings 
##################

if os.name == "posix":
    settings_file = os.path.join( os.getenv('HOME'), ".h4notifier.ini" )
else:
    settings_file = None

volatile_settings = {
    'username': 'USERNAME',
    'password' : 'PASSWORD',
    'who' : 'who@gmail.com',
    'email_address' : 'hackingthursday@googlegroups.com',
    'wikidot_api_user' : 'WIKIDOT_API_USER',
    'wikidot_api_key' : 'WIKIDOT_API_KEY',
    'facebook_user' : 'FB_USER',
    'facebook_password' : 'FB_PASS',
    'facebook_api_key' : 'FB_API_KEY',
    'facebook_secret' : 'FB_SECRET',
    'facebook_gid' : '############',
}


def read_settings_from_file():
    if os.access( settings_file, os.R_OK ):
        config = ConfigParser.RawConfigParser()
        config.read( settings_file )

        try:
	    # Section: gmail
            volatile_settings['username'] = config.get('gmail', 'username') 
            volatile_settings['password'] = config.get('gmail', 'password') 

	    # Section: hackingthursday
            volatile_settings['who'] = config.get('hackingthursday', 'who') 
            volatile_settings['email_address'] = config.get('hackingthursday', 'email_address') 

	    # Section: wikidot
            volatile_settings['wikidot_api_user'] = config.get('wikidot', 'wikidot_api_user') 
            volatile_settings['wikidot_api_key'] = config.get('wikidot', 'wikidot_api_key') 

	    # Section: facebook
            volatile_settings['facebook_password'] = config.get('facebook', 'facebook_password') 
            volatile_settings['facebook_user'] = config.get('facebook', 'facebook_user') 
            volatile_settings['facebook_api_key'] = config.get('facebook', 'facebook_api_key') 
            volatile_settings['facebook_secret'] = config.get('facebook', 'facebook_secret') 
            volatile_settings['facebook_gid'] = config.get('facebook', 'facebook_gid') 

        except:
            pass



##################
## Contents
##################

mail_content = '''
這次聚會和上週一樣是在 MarketPlace。

詳細資訊如下:

場地: MarketPlace 
時間: 週四晚上 19:30 至 22:00
地址: 台北市重慶南路一段1號2樓 ( 忠孝西路與重慶南路交口的 7-11 樓上, 近台北車站 )
 Map: http://goo.gl/8jmBY

店家有提供無線上網，電源，營業時間至 22:00 。
低消為1杯飲料，飲料約 100-140 元，輕食加飲料約 190-250 元。
>>店家有129元價位的簡餐(含飲料)，但限時17:00-18:00點餐，時間彈性的人可以提前前往用餐<<

如果您在前來的過程中，有任何問題，歡迎隨時聯絡我們。
或是填下列問卷，協助我們了解你的聯絡方式: http://goo.gl/FCV8f
'''

mail_content_header='''
這個是昨天的聚會手記，感謝大家的心得分享～

'''

mail_content_footer='''
相關連結:
http://www.hackingthursday.org/
http://groups.google.com/group/hackingthursday/
http://pad.hackingthursday.org/
'''

mail_content_other_link='''
H4 wiki, 若有新玩意 or 想問的問題可以先行貼上去囉
http://pad.hackingthursday.org
'''

mail_content_signature='''
這是一個給喜歡玩軟體、寫程式的人的小小聚會。
內容不外乎手把手，弄點東西，閒聊八卦。

這個聚會是開放的，你想參加的話，不用回信告知我們，
直接前來即可。也歡迎你邀朋友一起來  :-)

A small gathering for people who like software and programming.
Nothing but hand by hand, play something, and chat.
Welcome to here to have a dinner and talk together.

This gathering is open. Just come if you like it.
Welcome to bring your friends, too.
'''


def file2string( path ):
    result = ""
    f = open( path )
    for line in f:
        result += line

    f.close()

    return result

def string2file( string, path ):
    f = open( path, 'w')
    f.write( string )
    f.close()
    

def html2xml( the_html ):
    result = ""
    htmlfile = tempfile.mktemp()
    xmlfile  = tempfile.mktemp()
    string2file( the_html, htmlfile )
    os.system("tidy -q -asxhtml -numeric -utf8 < "+htmlfile+" > "+xmlfile )
    result = file2string( xmlfile )
    os.system( "rm " + htmlfile )
    os.system( "rm " + xmlfile )

    return result


def html2txt( the_html ):
    result = html2text.html2text( the_html.decode('utf-8'), '' ).encode('utf-8')
    return result
