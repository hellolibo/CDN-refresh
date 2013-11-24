# -*- coding: utf-8 -*- 

import os
import string


user_home = os.path.expanduser("~")

configFileName = '.CDNConfig'

configFilePath = '%s/%s'%(user_home, configFileName)

def update():
    
    global validCDN

    validCDN = []
    
    if os.path.exists(configFilePath):
        configFile = open(configFilePath, 'r+')

        for line in configFile.readlines() : 
            cdn = string.split(line, ' ') 
            validCDN.append(cdn)
    else:
        configFile = open(configFilePath, 'w')

    configFile.close()



def getAccount(CDNId):
    _validCDN = [c for c in validCDN if c[0] == CDNId]
    return len(_validCDN) > 0 and _validCDN[0][1:] or None
