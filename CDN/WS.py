# -*- coding: utf-8 -*-  

import string
import urllib2
import hashlib
import re

class WS:

    u'网宿'

    # url地址的最大长度
    _urlMaxLength = 8000

    _API = 'http://wscp.lxdns.com:8080/wsCP/servlet/contReceiver?username=%s&passwd=%s&url=%s&dir=%s&delaytime=0'


    def __init__(self, username='', password=''):

        self.username = username
        self.password = password

    def url(self, arr = []):
        u'网址'
        urls = self._groupUrl(arr)
        for u in urls:
            self._push(url = u)


    def dir(self, arr = []):
        u'目录'
        dirs = self._groupUrl(arr)
        for d in dirs:
            self._push(dir = d)


    def _push(self, url=[], dir=[]):

        if len(url) == 0 and len(dir) == 0:
            print 'lost url and dir.'
            return

        push_url = self._API%(
                        self.username,
                        self._md5(self.username+self.password+";".join(url)+";".join(dir)),
                        ";".join(url),
                        ";".join(dir)
                    )
        
        print 'start push...'
        print url + dir
        print 'Push Data -> ' + push_url
        print urllib2.urlopen(push_url).read()

    
    # 防止URL过长需对提交的url分组后刷新
    def _groupUrl(self, urls = []):
        group = []
        length = len(urls)
        start = 0
        str = ''

        # WS的URL是不需要http://的
        urls = [re.sub(r'^http:\/\/', '', u) for u in urls]

        for i in range(length):
            
            url = urls[i]
            
            if len(str) + len(url) >= self._urlMaxLength: 
                group.append(urls[start:i+1])
                str = url
                start = i + 1
            elif i + 1 == length:
                group.append(urls[start:])
            else:
                str = str + url

        return group

    def _md5(self, str):
        m = hashlib.md5()   
        m.update(str)
        return m.hexdigest()
