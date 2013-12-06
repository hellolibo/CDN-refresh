# -*- coding: utf-8 -*-  

import string
import urllib2
import hashlib
import re
from HTMLParser import HTMLParser

from WS import WS

class MBB_WS(WS):

    def __init__(self):

        super(MBB_WS, self).__init__()
        
        self.id = 'mbbws'
        self.name = u'麦包包' + self.name
        self.support = self.support + [
                                        ('sku', u'静物图', u'填写SKU即可'),
                                        ('model', u'模特物', u'填写SKU即可')
                                      ]
    

    def sku(self, skus = []):
        dirs = self._skuToPicDir(skus)
        self.dir(dirs)


    def model(self, skus=[]):
        item_url = 'http://www.mbaobao.com/item/%s'%skus[0]  
        goodsHtml = urllib2.urlopen(item_url).read()

        goodsPageHTMLParser = GoodsPageHTMLParser()
        goodsPageHTMLParser.feed(goodsHtml)
        self.url(goodsPageHTMLParser.pics)

    # sku转换成目录url
    def _skuToPicDir(self, skus = []):
        return ["sku.mbaobao.com/%s/%s/%s/" % (sku[:4],sku[:8],sku[8:]) for sku in skus]


class GoodsPageHTMLParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.pics = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr in attrs:
                if (attr[0] == 'src' or attr[0] == 'src2') and attr[1][:22] == 'http://img.mbaobao.com':
                    self.pics.append(attr[1])
            
                
        


if __name__ == '__main__':
    
    ws = MBB_WS()
    
    ws.model('1409003203')

