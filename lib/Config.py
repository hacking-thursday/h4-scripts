import os
import ConfigParser

CONFIG_FILE = os.path.join(os.getenv('HOME'), ".h4notifier.ini")


class Config():
    def __init__(self, config_file=CONFIG_FILE):
        #self.cf = ConfigParser.ConfigParser(allow_no_value=True)
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(config_file)

    def __getitem__(self, section):
        # return config list to dict
        # you can use by Config()['section']['option']

        return dict(self.cf.items(section))

    def Get(self, section, option):
        return self.cf.get(section, option)

    def Set(self, section, option, value):
        self.cf.set(section, option, value)
        self.cf.write(open(CONFIG_FILE, 'wb'))
