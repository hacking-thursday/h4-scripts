#!/usr/bin/env python
# encoding: utf-8

import xmlrpclib
from xmlrpclib import ServerProxy

EP_URL = 'www.wikidot.com/xml-rpc-api.php'


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

    def get_page(self, page_url):
        return self.proxy.pages.get_one({"site": self.site, "page": page_url})

    def get_pages_meta(self, page_url_arr):
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
