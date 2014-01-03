import os
import ConfigParser

CONFIG_FILE = os.path.join(os.getenv('HOME'), ".h4notifier.ini")


class Config():

    def __init__(self):
        #self.cf = ConfigParser.ConfigParser(allow_no_value=True)
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(CONFIG_FILE)

    def __getitem__(self, key):
        # return config list to dict
        # you can use by Config()['Key']

        return dict(self.cf.items(key))

    def Set(self, section, key, value):
        self.cf.set(section, key, value)
        self.cf.write(open(CONFIG_FILE, 'wb'))
