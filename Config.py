# -*- coding: utf-8 -*- 

import os
import string

class Config:

    def __init__(self):

        self.validCDN = []

        local_encoding = getLocalEncoding()

        self.user_home = os.path.expanduser("~").decode(local_encoding)

        self.configFileName = '.CDNConfig'

        self.configFilePath = '%s/%s'%(self.user_home, self.configFileName)

    def init(self):
          
        if os.path.exists(self.configFilePath):
            configFile = open(self.configFilePath, 'r+')

            for line in configFile.readlines() : 
                cdn = string.split(line, ' ') 
                self.validCDN.append(cdn)
        else:
            configFile = open(self.configFilePath, 'w')

        configFile.close()



    def getAccount(self, CDNId):
        _validCDN = [c for c in self.validCDN if c[0] == CDNId]
        return len(_validCDN) > 0 and _validCDN[0][1:] or None

    def saveAccount(self, CDNId, username, password):
        exist = False
        for cdn in self.validCDN:
            if cdn[0] == CDNId:
                cdn[1] = username
                cdn[2] = password
                exist = True
        if not exist:
            self.validCDN.append([CDNId, username, password])

        configFile = open(self.configFilePath, 'w')
        configFile.write('\n'.join([' '.join(cdn) for cdn in self.validCDN]))
        configFile.close()



def getLocalEncoding():
    u"""取得本地编码"""

    import locale
    import codecs

    return "%s" % codecs.lookup(locale.getpreferredencoding()).name

