#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telnetlib


def big5(str):
    return str.decode('utf-8', 'ignore').encode('big5', 'ignore')


class PTT():
    def __init__(self, id, password, debug=False):
        self.id = id
        self.password = password

        self.tn = telnetlib.Telnet('ptt.cc')
        if debug:
            self.tn.set_debuglevel(2)
        self.tn.read_until('guest')

        self._login()

    def _login(self):
        self.tn.write('%s\r%s\r' % (self.id, self.password))

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

        return False

    # 進入討論版
    def enter(self, board):
        # 搜尋
        self.tn.write('s')
        self.tn.write('%s\r' % board)

        self.tn.read_until(big5('請按任意鍵繼續'))
        self.tn.write('\r')

        self.tn.read_until(big5('文章選讀'))

        print '進入 %s 版' % board

    def post(self, subject, content):
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

        self.tn.read_until(big5('文章選讀'))

        print '文章發布'

    def quit(self):
        self.tn.write('eee')
        self.tn.write('ee')
        self.tn.write('g')
        self.tn.write('\r')
        self.tn.write('y')
        self.tn.write('\r')
        self.tn.write('\r\r')

        print '離開 BBS'

        # sess_op = tn.read_all()
        # print sess_op

if __name__ == '__main__':
    ID = ''
    PASSWORD = ''

    board = 'Test'
    subject = '[活動] 2008-08-21 固定聚會'
    content = '1234\n測試內容\n5678'

    ptt = PTT(ID, PASSWORD)
    ptt.enter(board)
    ptt.post(subject, content)
    ptt.quit()
