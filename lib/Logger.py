import os
import sys
root_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root_path, '3rd'))

import logging
# from cloghandler import ConcurrentRotatingFileHandler

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
