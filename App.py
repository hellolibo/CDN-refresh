# -*- coding: utf-8 -*- 

from Tkinter import *
import Tkconstants

import Config
import CDN
import UI

class CDNRefreshApp:

    def __init__(self):

        Config.init(CDN.list)

    def run(self):

        root = Tk()
        app = UI.MainFrame(root, Config, CDN)
        root.mainloop()


def main():

    CDNRefreshApp().run()


if __name__ == '__main__':
    
    main()