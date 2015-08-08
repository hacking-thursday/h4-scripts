# 設定 API 資訊
    $ cp config/dot.h4notifier.ini $HOME/.h4notifier.ini
    $ vi $HOME/.h4notifier.ini

# 安裝系統套件

## Ubuntu
    # apt-get install python-virtualenv python-pip mercurial tidy php5-cli php-pear

## Python

## 建立獨立環境
    $ virtualenv --no-site-package env --python=python2.7
    $ . ./env/bin/activate

## 安裝 Python 函式庫
    $ pip install -r requirements.txt

# 安裝第三方函式庫
    $ make setup

# 安裝 h4-script 進系統或 virtualenv
    $ make install
