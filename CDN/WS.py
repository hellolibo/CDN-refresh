# -*- coding: utf-8 -*-  

import string
import urllib2
import hashlib
import re


class WS(object):

    def __init__(self):

        self.id = 'ws'
        self.name = u'网宿'
        self.support = [
            ('url', u'网址', u'http开头的网址,例如: http://www.yourdomain.com/path/to/pic.jpg'),
            ('dir', u'目录', u'http开头的目录,例如: http://www.yourdomain.com/path/to/')
            ]

        # url地址的最大长度
        self.urlMaxLength = 8000
        self.API = 'http://wscp.lxdns.com:8080/wsCP/servlet/contReceiver?username=%s&passwd=%s&url=%s&dir=%s&delaytime=0'

    def open(self, username='', password=''):
        self.username = username
        self.password = password
        return self

    def url(self, arr = []):
        urls = self._groupUrl(arr)
        for u in urls:
            self._push(url = u)

    def dir(self, arr = []):
        dirs = self._groupUrl(arr)
        for d in dirs:
            self._push(dir = d)

    def _push(self, url=[], dir=[]):

        if len(url) == 0 and len(dir) == 0:
            print 'lost url and dir.'
            return

        push_url = self.API%(
                        self.username,
                        self._md5(self.username+self.password+";".join(url)+";".join(dir)),
                        ";".join(url),
                        ";".join(dir)
                    )
        
        print 'Push Data -> ' + push_url
        print urllib2.urlopen(push_url).read()
        print '\n'

    
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
            
            if len(str) + len(url) >= self.urlMaxLength: 
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

if __name__ == '__main__':
    
    ws = WS()
    print ws.support