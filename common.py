#!/usr/bin/env python
# coding:utf8
#
# Author: Chun-Yu Lee (Mat) <matlinuxer2@gmail.com>
# Copyright: Chun-Yu Lee (Mat) <matlinuxer2@gmail.com>
# License: MIT
#

from __future__ import print_function

import ConfigParser
import datetime
import os
import re
import subprocess
import sys
import tempfile

from BeautifulSoup import BeautifulSoup


root_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root_path, '3rd'))
sys.path.append(os.path.join(root_path, '3rd', 'gdata-python-client', 'src'))

import html2text  # pip version decode error, using 3rd-party instead


# idx == 0 => 這一週的星期四
# idx == 1 => 下一週的星期四
# idx == 2 => 下下一週的星期四
# idx == -1 => 上一週的星期四
# idx == -2 => 上上一週的星期四
# ...以此類推
def getThursday(idx, fmt="default"):
    delta_days = 4 - datetime.date.today().isoweekday() + idx * 7
    the_thursday = datetime.date.today() + datetime.timedelta(days=delta_days)
    if fmt == "default":
        res = the_thursday.isoformat()
    elif fmt == "fb":
        res = the_thursday.strftime('X%m/X%d/X%Y').replace('X0', 'X').replace('X', '')
    else:
        res = the_thursday.isoformat()

    return res


# 回傳 0 => 這一週
# 回傳 1 => 下一週
# 回傳 2 => 下下一週
# 回傳 -1 => 上一週
# 回傳 -2 => 上上一週
# 回傳 False => 非星期四
def chkThursday(date_str):
    base_day = datetime.datetime.strptime(getThursday(0), "%Y-%m-%d").date()
    this_day = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

    delta_days = (this_day - base_day).days
    if delta_days % 7 == 0:
        res = delta_days / 7
    else:
        res = False
    return res


##################
## Contents
##################
mail_content_header = '''
這個是昨天的聚會手記，感謝大家的心得分享～

'''

mail_content_footer = '''
----
主網站: http://www.hackingthursday.org/
Google論譠: http://groups.google.com/group/hackingthursday/
Facebook群組: http://www.facebook.com/groups/hackingday/
'''


def string2file(string, path):
    f = open(path, 'w')
    f.write(string)
    f.close()


def html2txt(the_html):
    result = html2text.html2text(the_html.decode('utf-8'), '').encode('utf-8')
    return result


def get_wikidot_content_body(URL):
    htmlfile = tempfile.mktemp()

    os.system("wget -O " + htmlfile + " " + URL)
    the_html = file2string(htmlfile)
    os.system("rm " + htmlfile)

    soup = BeautifulSoup(the_html)
    div = soup.findAll('div', attrs={'id': 'page-content'})
    res_txt = ""
    for d in div:
        res_txt += d.prettify()

    result = res_txt

    return result


def convert_spreadsheet_to_userdata(sprd_data):
    result = []

    for k in sprd_data.keys():
        row = sprd_data[k]

        alias = row['筆名'].split('||')
        url_name = row['url_name']
        rel_name = row['Name'].lower().strip()
        email = row['E-Mail']
        notify = row['notify']

        result.append({
            "alias": alias,
            "url_name": url_name,
            "rel_name": rel_name,
            "email": email,
            "notify": notify,
        })

    return result


def search_userdata(sprd_data, keyword):
    result = {}
    for k in sprd_data.keys():
        row = sprd_data[k]
        for value in row.values():
            if value.find(keyword) >= 0:
                result[k] = row

    return result


def show_userdata(sprd_data_row):
    field00 = sprd_data_row['url_name']
    field01 = sprd_data_row['Name']
    field02 = sprd_data_row['Full Name']
    field03 = sprd_data_row['E-Mail']
    field04 = sprd_data_row['Mobile']
    field05 = sprd_data_row['筆名']
    field06 = sprd_data_row['notify']
    field07 = sprd_data_row['備註']

    print("ID".rjust(10), ":", field00)
    print("Nick".rjust(10), ":", field01)
    print("姓名".rjust(12), ":", field02)
    print("E-mail".rjust(10), ":", field03)
    print("手機".rjust(12), ":", field04)
    print("筆名".rjust(12), ":", field05.replace('||', ', '))
    print("notify".rjust(10), ":", field06)
    print("備註".rjust(12), ":", field07)


def find_keyword_and_insert_content(content, find_kw_beg, find_kw_end, ins_str):
    ins_pos_beg = content.find(find_kw_beg) + find_kw_beg.__len__()
    if find_kw_beg is None:
        ins_pos_end = ins_pos_beg
    else:
        ins_pos_end = content.find(find_kw_end)

    if ins_pos_beg >= 0 and ins_pos_end >= ins_pos_beg:
        new_content = content[0:ins_pos_beg] + ins_str + content[ins_pos_end:]
    else:
        new_content = content

    return new_content


def get_diff_output_between_two_string(orig, after):
    tmp_old = tempfile.mktemp()
    tmp_new = tempfile.mktemp()
    string2file(orig, tmp_old)
    string2file(after, tmp_new)
    cmd = "diff -Naur %s %s" % (tmp_old, tmp_new)
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
    os.unlink(tmp_old)
    os.unlink(tmp_new)

    return out


def page_split_by_keyword(text, keyword):
        pos = text.rfind(keyword)

        if pos >= 0:
            head = text[:pos]
            body = text[pos:]
        else:
            head = text
            body = ""

        return head, body


def send_notify_mail(author, author_data_obj, sender, root_url):
    ad_obj = author_data_obj
    author_data = ad_obj.find_author_by_name(author)
    rel_name = author_data['rel_name']
    url_name = author_data['url_name']
    email = author_data['email']

    Sender = sender  # 值日生的 email
    Reciver = email
    Subject = "H4個人頁面更新通知"
    Link = "%s/user:%s" % (root_url, url_name)

    Html = """
<html>
    <head>
        <title>%s</title>
    </head>
    <body>
    <a href="%s">%s</a>
    <pre>
Hi %s 您好:

關於您在 H4 的個人手記有新的
內容嘍~(網址如上) 歡迎您有空
再來 H4 逛逛~!

備註:
這是 H4 值日生們新推出的小功
能，bot 會將大家的筆記，依個
別作排序跟整理在 wiki 上。

%s

備註2:
個人頁面 "Table of Contents"
以上的部份是可以編輯的。歡迎
您編輯個人相關資訊及連結!!
( Table of Contents 以下的部
份則是會由 bot 定期產生並覆
蓋 )

若您有任何問題或是建議，都歡
迎 feedback 給我們，謝謝!!
    </pre>
    </body>
</html>
""" % (Subject, Link, Link, rel_name, root_url + "h4note")

    Txt = html2txt(Html)

    receivers = Reciver.split(',')
    for item in receivers:
        receiver = item.strip()
        gmail.send(Sender, receiver, Subject, Txt, Html)
