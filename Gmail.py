# coding:utf-8

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.Header import Header
from email.mime.text import MIMEText

SERVER_HOST = "smtp.gmail.com"
SERVER_PORT = 587


class Gmail():
    def __init__(self, username, password):
        self.smtp = smtplib.SMTP(SERVER_HOST, SERVER_PORT)
        self.smtp.starttls()
        self.smtp.login(username, password)

    def send(self, sender, recipient, subject, text=None, html=None):
        msg = MIMEMultipart("alternative")

        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = Header(subject, "utf-8")

        if text:
            msg.attach(MIMEText(text, "plain", "utf-8"))
        if html:
            msg.attach(MIMEText(html, "html", "utf-8"))

        self.smtp.sendmail(sender, recipient, msg.as_string())

    def __del__(self):
        # Should be self.smtp.quit(), but that crashes...
        self.smtp.close()
