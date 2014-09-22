#!/usr/bin/env python
# coding:utf8
#
# Author: Chun-Yu Lee (Mat) <matlinuxer2@gmail.com>
# Copyright: Chun-Yu Lee (Mat) <matlinuxer2@gmail.com>
# License: MIT
#

from __future__ import print_function

import datetime

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Header import Header

import os
import ConfigParser

from BeautifulSoup import BeautifulSoup

import tempfile
import subprocess

import re
import sys

root_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root_path, '3rd'))
sys.path.append(os.path.join(root_path, '3rd', 'gdata-python-client', 'src'))

import html2text  # pip version decode error, using 3rd-party instead
import lib.GoogleSpreadsheetAPI


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


#
# send_gmail("matlinuxer2@gmail.com", "matlinuxer2@gmail.com", "Hello from python!", "<hr/><h1>hello from python</h1><hr/>", "USERNAME", "PASSWORD")
#
def send_gmail(sender, recipient, subject, text, html, username, passwd):
    msg = MIMEMultipart("alternative")

    msg['Subject'] = Header(subject, "utf-8")
    msg['From'] = sender
    msg['To'] = recipient

    msg.attach(MIMEText(text, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(username, passwd)
    mailServer.sendmail(sender, recipient, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()


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


def fetch_googledoc_spreadsheet(email, password, spreadsheet_name, worksheet_name):
    res_ary = []
    col_mapping = {}
    result_ary = {}

    # 取得列表內容
    spr = lib.GoogleSpreadsheetAPI.Spreadsheet(email, password, spreadsheet_name)
    work = lib.GoogleSpreadsheetAPI.Spreadsheet.Worksheet(spr, worksheet_name)
    feed = work.getCells()

    for i, entry in enumerate(feed.entry):
        #print (i, entry.title.text, entry.content.text)
        pattern = r"(\w)(\d+)"
        matches = re.findall(pattern, entry.title.text)
        #print matches
        col_idx = matches[0][0]
        row_idx = matches[0][1]

        res_ary.append((row_idx, col_idx, entry.content.text))

    # 取得欄位名稱對應
    for item in res_ary:
        row_idx = item[0]
        col_idx = item[1]
        value = item[2]

        if row_idx == "1":
            col_mapping[col_idx] = value.strip()

    # 處理並產生回傳陣列
    for item in res_ary:
        row_idx = item[0]
        col_idx = item[1]
        value = item[2]

        if row_idx != '1':
            if not row_idx in result_ary:
                result_ary[row_idx] = {}
                for col_name in col_mapping.values():
                    result_ary[row_idx][col_name] = ''

            col_name = col_mapping[col_idx]

            # 修正手機的格式
            if col_name == "Mobile" and value.__len__() == 9:
                value = "0" + value

            result_ary[row_idx][col_name] = value

    return result_ary


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


def php_parse_wikidot_heading(path):
    cmd_path = os.path.join(root_path, 'parse_wikidot_heading.php')
    cmd = "php %s --file='%s'" % (cmd_path, path)
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
    result = out.strip().split('\n')

    return result
