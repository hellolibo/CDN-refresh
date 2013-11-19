# -*- coding: utf-8 -*- 

import WS

class List:

    def __init__(self):

        self.list = {
            'ws' : WS()
        }

    def get(self):

        return self.list