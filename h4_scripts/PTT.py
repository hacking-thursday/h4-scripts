# -*- coding: utf-8 -*-

import telnetlib


def big5(str):
    return str.decode('utf-8', 'ignore').encode('big5', 'ignore')


class PTT():
    def __init__(self, debug=False):
        self.tn = telnetlib.Telnet('ptt.cc')
        if debug:
            self.tn.set_debuglevel(2)
        self.tn.read_until('guest')

    def login(self, id, password):
        self.tn.write('%s\r%s\r' % (id, password))

        while True:
            line = self.tn.read_very_eager()

            if big5('請勿頻繁登入以免造成系統過度負荷') in line:
                self.tn.write('\r')
            elif '[Y/n]' in line:
                self.tn.write('Y\r')
            elif big5('請按任意鍵繼續') in line:
                self.tn.write('\r')
            elif big5('分組討論區') in line:
                print '登入成功，進入主頁面'
                return True
            elif big5('密碼不對') in line:
                print '登入失敗'
                return False

    # 進入討論版
    def enter(self, board):
        # 搜尋
        self.tn.write('s')
        self.tn.write('%s\r' % board)

        self.tn.read_until(big5('請按任意鍵繼續'))
        self.tn.write('\r')

        if self.tn.read_until(big5('文章選讀')):
            print '進入 %s 版' % board
            return True

        return False

    def post(self, subject, content, dry_run=False):
        if dry_run:
            return True
        else:
            # 發表文章
            self.tn.write('')
            self.tn.write('\r')

            # 標題
            self.tn.write('%s\r' % big5(subject))

            # 內容
            for line in content.split('\n'):
                self.tn.write('%s\r' % big5(line.rstrip()))

            # 存檔
            self.tn.write('')
            self.tn.read_until(big5('確定要儲存檔案嗎'))
            self.tn.write('S')
            self.tn.write('\r')
            self.tn.read_until(big5('任意鍵繼續'))
            self.tn.write('\r')

            if self.tn.read_until(big5('文章選讀')):
                print '文章發布'
                return True

        return False

    def quit(self):
        while True:
            self.tn.write('e')
            line = self.tn.read_very_eager()

            if big5('離開') in line:
                self.tn.write('g')
                self.tn.write('\r')
                self.tn.read_until(big5('您確定要離開'))
                self.tn.write('y')
                self.tn.write('\r')
                self.tn.read_until(big5('此次停留時間'))
                print '離開 BBS'
                return True
