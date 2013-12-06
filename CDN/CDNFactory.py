# -*- coding: utf-8 -*- 

from WS import WS
from MBB_WS import MBB_WS

ws = WS()
mbb_ws = MBB_WS()

cdns = [ws, mbb_ws]

def get(CDNId, account):
    for cdn in cdns:
        if cdn.id == CDNId:
            return cdn.open(account[0], account[1])
    return None

def all():
    cdnInfo = []
    for cdn in cdns:
        cdnInfo.append({
            'id'      : cdn.id,
            'name'    : cdn.name,
            'support' : cdn.support
            })

    return cdnInfo


if __name__ == '__main__':
    
    print all()