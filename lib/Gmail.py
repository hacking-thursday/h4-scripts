# coding:utf-8

import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.Header import Header
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email.Utils import formatdate
from email import Encoders
from email.Utils import COMMASPACE
from itertools import chain

HOST = "smtp.gmail.com"
PORT = 587


class Gmail():
    def __init__(self):
        self.smtp = smtplib.SMTP(HOST, PORT, timeout=5)
        self.smtp.starttls()

    def login(self, username, password):
        try:
            self.smtp.login(username, password)
            return True
        except smtplib.SMTPAuthenticationError:
            return False

    def send(self, sender, recipient, subject, text=None, html=None, files=[], cc=[]):
        try:
            msg = MIMEMultipart("alternative")

            if isinstance(recipient, str):
                recipient = recipient.split(',')
            if isinstance(cc, str):
                cc = cc.split(',')

            msg['From'] = sender
            msg['To'] = COMMASPACE.join(recipient)
            if cc:
                msg['Cc'] = COMMASPACE.join(cc)
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
            return self.smtp.sendmail(sender, list(chain(recipient, cc)), msg.as_string())
        except Exception, error:
            print "Unable to send e-mail: '%s'." % str(error)

            return False

    def quit(self):
        try:
            # Should be self.smtp.quit(), but that crashes...
            self.smtp.close()

            return True
        except:
            return False

    def __del__(self):
        self.quit()
