import logging
from cloghandler import ConcurrentRotatingFileHandler

LOGFILE = 'h4notifier.log'


class Logger():
    def __init__(self, app):
        self.log = logging.getLogger(app)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        rotateHandler = ConcurrentRotatingFileHandler(LOGFILE, "a", 512 * 1024, 5)
        rotateHandler.setFormatter(formatter)

        self.log.addHandler(rotateHandler)
        self.log.setLevel(logging.DEBUG)

    def __new__(self):
        return self.log
