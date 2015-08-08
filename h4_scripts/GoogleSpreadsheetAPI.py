# coding=utf8

import gdata
import gdata.spreadsheet
import gdata.spreadsheet.service
import re

DEBUG = False


class Spreadsheet:
    def __init__(self, username, password, doc_name):
        # Connect to Google
        self.spr_client = gdata.spreadsheet.service.SpreadsheetsService()
        self.spr_client.email = username
        self.spr_client.password = password
        self.spr_client.ProgrammaticLogin()

        self.doc_name = doc_name
        self.spreadsheet_id = self._getSpreadsheetId()

    def _getSpreadsheetId(self):
        q = gdata.spreadsheet.service.DocumentQuery()
        q['title'] = self.doc_name
        q['title-exact'] = 'true'

        feed = self.spr_client.GetSpreadsheetsFeed(query=q)
        if DEBUG:
            print(feed)
            print('\n')
            print(feed.entry)
            print('\n')
            print(type(feed.entry))
            print('\n')
            print(len(feed.entry))
            print('\n')

        for f in feed.entry:
            spreadsheet_id = f.id.text.rsplit('/', 1)[1]

            return spreadsheet_id

    def getWorksheetId(self):
        feed = self.spr_client.GetWorksheetsFeed(self.spreadsheet_id)
        if DEBUG:
            print(feed)
            print('\n')

        # worksheet_id = [{f.title.text: f.id.text.rsplit('/', 1)[1]} for f in feed.entry]
        worksheet_id = dict((f.title.text, f.id.text.rsplit('/', 1)[1]) for f in feed.entry)

        return worksheet_id

    def getWorksheetCellArray(self, worksheet):
        worksheet = self.Worksheet(self, worksheet)
        return worksheet.getCellArray()

    def updateWorksheetCell(self, worksheet, row, col, inputValue):
        worksheet = self.Worksheet(self, worksheet)
        return worksheet.updateCell(row, col, inputValue)

    class Worksheet:
        ''' An iterable google spreadsheet object.  Each row is a dictionary with an entry for each field, keyed by the header.  GData libraries from Google must be installed.'''

        def __init__(self, spr_object, worksheet_name):
            self.spr_client = spr_object.spr_client

            self.spreadsheet_id = spr_object.spreadsheet_id

            self.worksheet_id = spr_object.getWorksheetId()[worksheet_name]

            self.count = 0

        def formRows(self):
            ListFeed = self.spr_client.GetListFeed(self.spreadsheet_id, self.worksheet_id)
            rows = []
            for entry in ListFeed.entry:
                d = {}
                for key in entry.custom.keys():
                    d[key] = entry.custom[key].text
                rows.append(d)
            return rows

        def updateCell(self, row, col, inputValue):
            self.spr_client.UpdateCell(row, col, inputValue, self.spreadsheet_id, self.worksheet_id)

        def __iter__(self):
            return self

        def next(self):
            if self.count >= len(self.rows):
                self.count = 0
                raise StopIteration
            else:
                self.count += 1
                return self.rows[self.count - 1]

        def __getitem__(self, item):
            return self.rows[item]

        def __len__(self):
            return len(self.rows)

        def getCells(self):
            return self.spr_client.GetCellsFeed(self.spreadsheet_id, self.worksheet_id)

        def getCellArray(self):
            res_ary = []
            col_mapping = {}
            result_ary = {}

            # 取得列表內容
            feed = self.getCells()

            for i, entry in enumerate(feed.entry):
                #print (i, entry.title.text, entry.content.text)
                pattern = r"(\w)(\d+)"
                matches = re.findall(pattern, entry.title.text)
                #print matches
                col_idx = matches[0][0]
                row_idx = matches[0][1]

                res_ary.append((row_idx, col_idx, entry.content.text))

            # 取得欄位名稱對應
            for item in res_ary:
                row_idx = item[0]
                col_idx = item[1]
                value = item[2]

                if row_idx == "1":
                    col_mapping[col_idx] = value.strip()

            # 處理並產生回傳陣列
            for item in res_ary:
                row_idx = item[0]
                col_idx = item[1]
                value = item[2]

                if row_idx != '1':
                    if not row_idx in result_ary:
                        result_ary[row_idx] = {}
                        for col_name in col_mapping.values():
                            result_ary[row_idx][col_name] = ''

                    col_name = col_mapping[col_idx]

                    # 修正手機的格式
                    if col_name == "Mobile" and value.__len__() == 9:
                        value = "0" + value

                    result_ary[row_idx][col_name] = value

            return result_ary


if __name__ == '__main__':
    # DEBUG = 1
    username = 'YOUR_EMAIL'
    passwd = 'YOUR_PASSWORD'
    doc_name = 'YOU_GOOGLE_SPREADSHEET_FILENAME'
    sheet_name = 'WORKSHEET_NAME'


    # spr = Spreadsheet(username, passwd, doc_name)

    # print spr.spreadsheet_id
    # print spr.getWorksheetId()


    # work = Spreadsheet.Worksheet(spr, sheet_name)

    # print work.formRows()
    # print work.getCells()

    # work.updateCell(4, 4, '1234')
