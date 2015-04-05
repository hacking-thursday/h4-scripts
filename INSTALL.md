# 設定 API 資訊
    $ cp dot.h4notifier.ini $HOME/.h4notifier.ini
    $ vi $HOME/.h4notifier.ini

# 安裝系統工具

## Ubuntu
    # apt-get install python-pip mercurial tidy php5-cli php-pear
    $ make setup

# 安裝 Python 函式庫
    $ virtualenv --no-site-package virtenv --python=python2.7
    $ virtenv/bin/activate
    $ pip install -r requirements.txt
