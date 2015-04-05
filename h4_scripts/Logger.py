import os
import sys
import logging

LOGFILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'h4.log')


class Logger():
    def __init__(self, app):
        self.log = logging.getLogger(app)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # rotateHandler = ConcurrentRotatingFileHandler(LOGFILE, "a", 512 * 1024, 5)
        # rotateHandler.setFormatter(formatter)

        hdlr = logging.FileHandler(LOGFILE)
        hdlr.setFormatter(formatter)

        # self.log.addHandler(rotateHandler)
        self.log.addHandler(hdlr)

        self.log.setLevel(logging.DEBUG)

    def __new__(self):
        return self.log
