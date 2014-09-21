#!/usr/bin/env python
# encoding: utf-8

import os
import xmlrpclib
from xmlrpclib import ServerProxy

EP_URL = 'www.wikidot.com/xml-rpc-api.php'
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_cache")

class Wikidot():
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

    def save_page(self, page_url, title=None, content=None):
        data = {}
        data['site'] = self.site
        data['page'] = page_url
        if title:
            data['title'] = title
        if content:
            data['content'] = content

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
