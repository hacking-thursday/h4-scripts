# coding:utf-8

import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.Header import Header
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email.Utils import formatdate
from email import Encoders

HOST = "smtp.gmail.com"
PORT = 587


class Gmail():
    def __init__(self, username, password):
        self.smtp = smtplib.SMTP(HOST, PORT)
        self.smtp.starttls()
        self.smtp.login(username, password)

    def send(self, sender, recipient, subject, text=None, html=None, files=None):
        msg = MIMEMultipart("alternative")

        msg['From'] = sender
        msg['To'] = recipient
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = Header(subject, "utf-8")

        # 內文
        if text:
            msg.attach(MIMEText(text, "plain", "utf-8"))
        if html:
            msg.attach(MIMEText(html, "html", "utf-8"))

        # 附加檔案
        for f in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(f, "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)

        # 寄出
        self.smtp.sendmail(sender, recipient, msg.as_string())

    def __del__(self):
        # Should be self.smtp.quit(), but that crashes...
        self.smtp.close()
