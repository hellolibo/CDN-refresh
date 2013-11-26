# -*- coding: utf-8 -*- 

import os
import string


user_home = os.path.expanduser("~")

configFileName = '.CDNConfig'

configFilePath = '%s/%s'%(user_home, configFileName)


def init():
    
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

def saveAccount(CDNId, username, password):
    exist = False
    for cdn in validCDN:
        if cdn[0] == CDNId:
            cdn[1] = username
            cdn[2] = password
            exist = True
    if not exist:
        validCDN.append([CDNId, username, password])

    configFile = open(configFilePath, 'w')
    configFile.write('\n'.join([' '.join(cdn) for cdn in validCDN]))
    configFile.close()





