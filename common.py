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
from email.Header import Header

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

def nextThursday( this_thursday_str ):
    this_thursday = datetime.datetime.strptime( this_thursday_str, "%Y-%m-%d" )
    next_thursday = this_thursday + datetime.timedelta( days=7 )
    result = next_thursday.date().isoformat()
    return result

def prevThursday( this_thursday_str ):
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

   msg['Subject'] = Header( subject, "utf-8" )
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

mail_content_header='''
這個是昨天的聚會手記，感謝大家的心得分享～

'''

mail_content_footer='''
相關連結:
http://www.hackingthursday.org/
http://groups.google.com/group/hackingthursday/
http://pad.hackingthursday.org/
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


def get_wikidot_content_body( URL ):
    xmlfile  = tempfile.mktemp()
    htmlfile = tempfile.mktemp()

    os.system( "wget -O "+htmlfile+" "+URL )
    the_html = file2string( htmlfile )
    os.system( "rm "+ htmlfile )

    the_xml = html2xml( the_html )
    string2file( the_xml, xmlfile )
    doc = libxml2.parseFile( xmlfile )

    ctxt = doc.xpathNewContext()
    ctxt.xpathRegisterNs('xhtml', 'http://www.w3.org/1999/xhtml')
    rows = ctxt.xpathEval('//xhtml:div[@id="page-content"]')
    ctxt.xpathFreeContext()

    f = StringIO.StringIO()
    buf = libxml2.createOutputBuffer(f, 'UTF-8')
    rows[0].docSetRootElement( doc )
    doc.saveFileTo(buf, 'UTF-8')
    
    os.system( "rm " + xmlfile )
    result = f.getvalue()

    return result


def get_etherpad_content_body( URL ):
    htmlfile = tempfile.mktemp()

    ret = os.system( "wget -O "+htmlfile+" "+URL )
    if ret == 0:
	    the_html = file2string( htmlfile )
    else:
	    the_html = None
    os.system( "rm "+ htmlfile )

    result = the_html

    return result

