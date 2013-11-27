# -*- coding: utf-8 -*-  

import string
import urllib2
import hashlib
import re
from WS import WS

class MBB_WS(WS):

    u'麦包包网宿'

    def __init__(self, username='', password=''):
        self.ws = WS.__init__(self, username, password)
    
    def sku(self, skus = []):
        u'静物图'
        dirs = self._skuToPicDir(skus)
        self.ws.dir(dirs)


    def model(self, sku):
        u'模特物'
        pass

    # sku转换成目录url
    def _skuToPicDir(self, skus = []):
        return ["sku.mbaobao.com/%s/%s/%s/" % (sku[:4],sku[:8],sku[8:]) for sku in skus]