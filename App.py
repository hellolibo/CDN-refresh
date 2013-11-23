# -*- coding: utf-8 -*-  

import re

from Tkinter import *
import Tkconstants
import tkSimpleDialog

import Config
from CDN import *

class MainFrame:

    def __init__(self, master):

        self.allCDN = CDNFactory.all()
        
        Config.update()

        self.initFrame(master)
        self.initMenu(master)
        self.updateCDNList()
        self.bindEvent()

    def initFrame(self, master):

        master.title(u'CDN刷新工具')
        master.resizable(False, False)

        # 服务商
        self.cdnGroup = LabelFrame(master, text="CDN服务商", padx=5, pady=5)
        self.cdnGroup.pack(padx=10, pady=10, fill=BOTH)

        self.currentCDN = StringVar()
        self.currentCDN.set('')

        # 刷新类型
        self.supportGroup = LabelFrame(master, text="刷新类型", padx=5, pady=5)
        self.supportGroup.pack(padx=10, pady=10, fill=BOTH)

        self.currentSupport = StringVar()
        self.currentSupport.set("")

        # 刷新内容
        self.contentGroup = LabelFrame(master, text="刷新内容", padx=5, pady=5)
        self.contentGroup.pack(padx=10, pady=10, fill=BOTH)

        self.pushContentText = Text(self.contentGroup, bg = "#ffffff", height=10, width=50)
        self.pushContentText.grid(row = 0,column = 1, padx = 5, pady = 5)

        # 返回结果
        returnGroup = LabelFrame(master, text="刷新结果", padx=5, pady=5)
        scrollbar = Scrollbar(returnGroup)
        scrollbar.pack(side=RIGHT, fill=Y)
        returnGroup.pack(padx=10, pady=10, fill=BOTH)

        self.pushReturnText = Text(returnGroup, bg = "#000000", fg="#45b100", height=5, width=50, state = DISABLED, yscrollcommand=scrollbar.set)
        self.pushReturnText.grid(row = 0,column = 1, padx = 5, pady = 5)
        scrollbar.config(command=self.pushReturnText.yview)
        self.pushReturnText.pack()

        # 刷新按钮
        frame = Frame(master, padx = 10, pady = 10)
        frame.pack()

        self.pushBtn = Button(frame, text="刷新", width=20)
        self.pushBtn.grid(row = 0,column = 1, padx = 5, pady = 10)

    def initMenu(self, master):
        menubar = Menu(master)
        menubar.add_command(label="服务商设置", command=self.menuSetCDN)
        menubar.add_command(label="关于软件", command=self.menuAbout)
        master.config(menu=menubar)

    def menuSetCDN(self):
        pass

    def menuAbout(self):
        pass
    
    def updateCDNList(self):
        
        for child in self.cdnGroup.pack_slaves():
            child.destroy()

        validCDN = self.getValidCDN()
        if validCDN :
            i = 0
            for cdn in validCDN:
                radio = Radiobutton(self.cdnGroup, text=cdn['name'], variable=self.currentCDN, value=cdn['id'])
                radio.grid(row = 0,column = i, padx = 5, pady = 5)
                radio.bind('<Button-1>', self.onSelectedCDN)
                if i == 0 :
                    radio.select()
                    self.updateSupportList()
                i = i + 1
        else:
            Label(self.cdnGroup, text=u'请先从菜单中设置服务商', fg='#999999').grid(row = 0,column = 0, padx = 5, pady = 5)

    def updateSupportList(self):

        for child in self.supportGroup.pack_slaves():
            child.destroy()

        supports = self.getValidSupport()
        if supports :
            i = 0
            for support in supports:
                radio = Radiobutton(self.supportGroup, text=support[1], variable=self.currentSupport, value=support[0])
                radio.grid(row = 0,column = i, padx = 5, pady = 5)
                if i == 0 :
                    radio.select()
                i = i + 1
        else:
            pass

    def bindEvent(self):

        self.pushBtn.bind('<Button-1>', self.onPush)


    def onPush(self, event):

        CDNId = self.currentCDN.get()
        support = self.currentSupport.get()

        if CDNId == '' or support == '':
            return

        self.pushBtn.config(state =  DISABLED)

        content = [re.sub(r'^http:\/\/', '', line) for line in self.pushContentText.get(0.0,END).split("\n") if line.strip() != ""]

        CDN = CDNFactory.get(CDNId, Config.getAccount(CDNId))

        getattr(CDN, support)(content)

        self.pushBtn.config(state =  ACTIVE)


    def onSelectedCDN(self, event):

        self.updateSupportList()

        
    def getValidCDN(self):
        if len(Config.validCDN) > 0:
            return [a for v in Config.validCDN for a in self.allCDN if v[0] == a['id']]
        else:
            return None

    def getValidSupport(self):
        CDNId = self.currentCDN.get()
        cdn = filter(lambda cdn:cdn['id'] == CDNId, self.getValidCDN())
        return len(cdn) > 0 and cdn[0]['support'] or None

        
def run():

    root = Tk()
    app = MainFrame(root)
    root.mainloop()


if __name__ == '__main__':
    
    run()