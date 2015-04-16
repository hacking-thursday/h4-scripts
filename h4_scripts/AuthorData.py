#!/usr/bin/env python
# encoding: utf-8


def normalize_alias(alias):
    result = alias
    result = result.replace(':', '')
    result = result.replace(',', '')
    result = result.replace('.', '')
    result = result.replace('-', '')
    result = result.replace('\'', '')
    result = result.replace('"', '')
    result = result.replace('_', '')
    result = result.replace(' ', '')
    result = result.lower()
    result = result.strip()

    return result


class AuthorData():
    collection = []
    collection2 = []
    collection3 = []
    collection4 = []
    user_mapping = []
    authors_cnt = []

    def append_data_per_author(self, author, date, data):
        self.collection += [(author, date, data)]

    def collect_unmapped_headding(self, heading, page):
        self.collection2 += [(page, heading)]

    def collect_notify(self, url_name):
        self.collection3 += [url_name]

    def collect_unnotify(self, url_name):
        self.collection4 += [url_name]

    def process_page_per_author(self, author):
        page_content = """
[[toc]]
"""

        for cc in self.collection:
            name = cc[0]
            date = cc[1]
            rows = cc[2]
            if name.lower() == author.lower():
                page_content += "\n+ " + date + "\n"
                page_content += "來源: [[[" + date + "]]]\n"
                for row in rows:
                    page_content += row + "\n"

        page_content = page_content.strip()  # Normalize

        return page_content

    def list_authors(self):
        result = []
        for item in self.user_mapping:
            name = item['url_name']
            if name in result:
                continue

            if name.strip() == "":
                continue

            result += [name]

        return result

    def find_author_by_heading(self, heading):
        result = None

        alias = normalize_alias(heading)

        for row in self.user_mapping:
            aliases = row['alias']
            for a in aliases:
                    a2 = normalize_alias(a)
                    if alias == a2:
                            result = row

        return result

    def find_author_by_name(self, url_name):
        result = None

        for row in self.user_mapping:
            if url_name == row['url_name']:
                    result = row

        return result

    def get_author_cnt(self, rel_name):
            cnt = -1
            for row in self.authors_cnt:
                if row[0] == rel_name:
                    cnt = row[1]

            return cnt

    def parse_data_from_page(self, page, parts):
        # workaround
        #parts = partition_page(page)

        for part in parts:
            heading_str = part[0]
            data = part[1]

            heading_ary = heading_str.split(',')
            for heading in heading_ary:
                heading = heading.strip()

                # 如果該段是作者，則加入資料收集
                author_data = self.find_author_by_heading(heading)
                if author_data is not None:
                    author = author_data['url_name']
                    print("mapped  :: %s :: %s => %s " % (page, heading, author))
                    self.append_data_per_author(author, page, data)
                else:
                    print("unmapped:: %s :: %s " % (page, heading))
                    self.collect_unmapped_headding(heading, page)

    def make_index_of_authors(self):
        result = """
* [# H4ckers]
"""
        authors = self.list_authors()
        authors2 = []
        for au in authors:
            if self.get_author_cnt(au.lower()) > 0:
                    authors2.append(au)
        authors = authors2

        #en_char = "abcdefghijklmnopqrstuvwxyz"
        data_dict = {
            "abc": [],
            "def": [],
            "ghi": [],
            "jkl": [],
            "mno": [],
            "pqr": [],
            "stu": [],
            "vwx": [],
            "yz": [],
        }
        data_dict_nonen = []

        en_keys = data_dict.keys()
        en_keys.sort()  # 這裡作一次排序，以避免字母順序錯誤

        for author in authors:
            isNonEn = True
            for key in en_keys:
                if author[0].lower() in key and not author in data_dict[key]:
                        data_dict[key] += [author]
                        isNonEn = False
            if isNonEn:
                data_dict_nonen += [author]

        for key in en_keys:
            result += """ * [# 字母%s-%s]
""" % (key[:1].upper(), key[-1:].upper())
            items = data_dict[key]
            items.sort()  # 這裡作一次排序
            for item in items:

                # 這裡將作者名稱再轉成更個人化一些
                author_data = self.find_author_by_name(item)
                rel_name = author_data['rel_name']

                if item.lower() == rel_name.lower() or rel_name.strip() == "":
                        name = "%s" % (item)
                else:
                        name = "%s (%s)" % (rel_name, item)

                result += "  * [[[user:" + item + "|" + name + "]]]\n"

        # 目前 wikidot 不支援中文條目
        result += """ * [# 非英文字母]
* [[[user:non-en]]]
"""

        for item in data_dict_nonen:
            print("非英文項目: ", item)

        return result
