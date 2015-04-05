#!/usr/bin/env python
# encoding: utf-8

import os
import subprocess
import re
import xmlrpclib
from xmlrpclib import ServerProxy

EP_URL = 'www.wikidot.com/xml-rpc-api.php'
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_cache")


def php_parse_wikidot_heading(path):
    cmd_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "parse_wikidot_heading.php")
    cmd = "php %s --file='%s'" % (cmd_path, path)
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
    result = out.strip().split('\n')

    return result


def file2string(path):
    result = ""
    f = open(path)
    for line in f:
        result += line

    f.close()

    return result


class Wikidot():
    site = None

    def auth(self, user, key):
        try:
            self.proxy = ServerProxy('https://' + user + ':' + key + '@' + EP_URL)
            if self.proxy.system.listMethods():
                return True
        except xmlrpclib.ProtocolError:
            return False

    def _page_is_valid(self, name):
        return len(name) < 100 and "/" not in name

    def _site_is_valid(self, name):
        return len(name) < 20 and "/" not in name

    def set_site(self, name):
        if(self._site_is_valid(name)):
            self.site = name
            try:
                self.list_pages()
                return True
            except xmlrpclib.Fault:
                # Site does not exist
                return False
        else:
            return False

    def save_page(self, page_url, title=None, content=None, dry_run=False):
        data = {}
        data['site'] = self.site
        data['page'] = page_url
        if title:
            data['title'] = title
        if content:
            data['content'] = content

        if dry_run:
            return True
        else:
            self.proxy.pages.save_one(data)
            if self.list_pages(page_url):
                return True
            else:
                return False

    def get_page(self, page_url):
        try:
            return self.proxy.pages.get_one({"site": self.site, "page": page_url})
        except xmlrpclib.Fault:
            # page does not exist
            return False

    def get_pages_meta(self, page_url_arr):
        if isinstance(page_url_arr, str):
            page_url_arr = [page_url_arr]

        return self.proxy.pages.get_meta({"site": self.site, "pages": page_url_arr})

    def list_pages(self, filter=None):
        pages = self.proxy.pages.select({'site': self.site})
        filtering = []
        if filter:
            import re
            for p in pages:
                if re.search(filter, p):
                    filtering.append(p)
            return filtering
        else:
            return pages

    #
    # 將頁面資料從 wikidot 先下載到本地端作cache
    #
    def pull_and_cache_pages(self):
        pages = self.list_pages()
        while pages.__len__() > 0:
            # 一次取10個
            page_ary = pages[0:10]
            meta_ary = self.get_pages_meta(page_ary)

            for page in page_ary:
                page_time = meta_ary[page]['updated_at']
                page_file = os.path.join(CACHE_DIR, page + '@' + page_time)

                if os.access(CACHE_DIR, os.R_OK | os.W_OK) is False:
                    os.mkdir(CACHE_DIR)

                if os.access(page_file, os.R_OK) is False:
                    exist_pages = os.listdir(CACHE_DIR)
                    for p in exist_pages:
                        if p[:page.__len__()] == page:
                            p_path = os.path.join(CACHE_DIR, p)
                            # Remove duplicate
                            os.remove(p_path)

                    # Fetching page
                    the_page = self.get_page(page)
                    content = the_page["content"].encode('utf8')
                    f = open(page_file, 'w')
                    f.write(content)
                    f.close()

            # 跳下一輪
            pages = pages[10:]

    def get_page_content(self, page):
        result = ""

        p_path = self.get_page_cache_path(page)
        if p_path is not None:
            result = file2string(p_path)

        return result

    def get_page_cache_path(self, page):
        result = None

        exist_pages = os.listdir(CACHE_DIR)
        for p in exist_pages:
            if p[:page.__len__() + 1] == page + "@":
                p_path = os.path.join(CACHE_DIR, p)
                result = p_path

        return result

    def list_date_pages(self):
            ret_data = []

            pages = self.list_pages()
            for page in pages:
                if page[0:2] == "20" and page[4] == "-" and page[7] == "-":
                    ret_data += [page]

            return ret_data

    def list_user_pages(self):
            ret_data = []

            pages = self.list_pages()
            for page in pages:
                if page[0:5] == "user:":
                    ret_data += [page]

            return ret_data

    def list_headings(self, page):
        result = []

        p_path = self.get_page_cache_path(page)
        if p_path is not None:
            result = php_parse_wikidot_heading(p_path)

        return result

    def partition_page(self, page):
        content = self.get_page_content(page)
        headings = self.list_headings(page)

        pos_ary = []
        parts = []
        content_rows = content.split("\n")

        for i in range(0, content_rows.__len__()):
            line = content_rows[i]
            #print(i,": ", line)
            result = re.findall('^\+ (.*)\s*$', line)
            if result.__len__() > 0:
                heading = result[0]
                if heading in headings:
                    pos_ary += [(heading, i)]

        for i in range(0, pos_ary.__len__()):
            data = []
            if i + 1 == pos_ary.__len__():  # 最後一個
                for j in range(pos_ary[i][1] + 1, content_rows.__len__()):
                    data += [content_rows[j]]
            else:
                for j in range(pos_ary[i][1] + 1, pos_ary[i + 1][1]):
                    data += [content_rows[j]]

            heading = pos_ary[i][0]
            parts += [(heading, data)]

        return parts
