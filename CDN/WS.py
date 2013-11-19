# -*- coding: utf-8 -*-  

import string
import urllib2
import hashlib
import re

class WS:

    # cdn0*.mbbimg.cn
    cdnDomainId = range(1,10)

    # url地址的最大长度
    urlMaxLength = 8000

    API = 'http://wscp.lxdns.com:8080/wsCP/servlet/contReceiver?username=%s&passwd=%s&url=%s&dir=%s&delaytime=0'


    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.name = u'网宿'
        self.support  = {
                        'url'    : [u'网址', u'静态资源的网址'],
                        'dir'    : [u'目录', u'目录网址'],
                        'sku'    : [u'静物图', u'商品静物图,填写商品SKU'],
                        'model'  : [u'模特图', u'商品模特图,填写商品SKU']
                        }

    def url(self, arr = []):
        urls = self.groupUrl(arr)
        for u in urls:
            self.push(url = u)

    def dir(self, arr = []):
        dirs = self.groupUrl(arr)
        for d in dirs:
            self.push(url = d)

    def sku(self, skus = []):
        dirs = self.skuToPicDir(skus)
        self.dir(dirs)

    def model(self, sku):
        pass


    def push(self, url=[], dir=[]):

        if len(url) == 0 and len(dir) == 0:
            print 'lost url and dir.'
            return

        push_url = self.API%(
                        self.username,
                        self.md5(self.username+self.password+";".join(url)+";".join(dir)),
                        ";".join(url),
                        ";".join(dir)
                    )
        
        print 'start push...'
        print url + dir
        print urllib2.urlopen(push_url).read()

    
    # 防止URL过长需对提交的url分组后刷新
    def groupUrl(self, urls = []):
        group = []
        length = len(urls)
        start = 0
        str = ''

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

    # sku转换成目录url
    def skuToPicDir(self, skus = []):

        urls = []
        for skuDir in ["%s/%s/%s/" % (sku[:4],sku[:8],sku[8:]) for sku in skus]:
            urls = urls + ['cdn0%s.mbbimg.cn/%s' % (id,skuDir) for id in self.cdnDomainId]
        return urls

    def md5(self, str):
        m = hashlib.md5()   
        m.update(str)
        return m.hexdigest()

if __name__ == '__main__':
    
    ws = WS('mbbimg', '123!@#qwe')
    ws.url(['cdn01.mbbimg.cn/1407/14070052/02/60/04.jpg'])
    # ws.dir(['cdn01.mbbimg.cn/1407/14070052/02/60/'])
    # ws.sku(['1407005202'])
