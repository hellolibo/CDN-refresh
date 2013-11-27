# -*- coding: utf-8 -*- 

from WS import WS
from MBB_WS import MBB_WS

def get(CDNId, account):

    if CDNId == 'WS':
        print account
        return WS(account[0], account[1])

    elif CDNId == 'MBB_WS':
        return MBB_WS(account[0], account[1])

    else:
        return None

def all():
    cdns = [WS, MBB_WS]
    cdnInfo = []
    for cdn in cdns:
        cdnInfo.append({
            'id'      : cdn.__name__,
            'name'    : cdn.__doc__,
            'support' : [ (fun, getattr(cdn, fun).__doc__) for fun in [m for m in dir(cdn) if m[0] != '_'] ]
            })

    return cdnInfo


if __name__ == '__main__':
    
    print all()