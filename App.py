# -*- coding: utf-8 -*-  

import re

from Tkinter import *
from ttk import *
import Tkconstants
import tkSimpleDialog

import Config
from CDN import *

class MainFrame:

    def __init__(self, master):
        
        Config.update()

        self.master = master

        self.initFrame()
        self.initMenu()
        self.updateCDNList()
        self.bindEvent()

    def initFrame(self):

        self.master.title(u'CDN刷新工具')
        self.master.resizable(False, False)

        Style().theme_settings("default", {
           "TLabelFrame": {
               "configure": {"padding": 5}
           },
           "TFrame": {
                "configure": {"padding": 10}
           },
           "tip.TLabel": {
                "configure": {"foreground": '#999999'}
           }
        })


        # 服务商
        self.cdnGroup = LabelFrame(self.master, text="CDN服务商")
        self.cdnGroup.pack(padx=10, pady=10, fill=BOTH)

        self.currentCDN = StringVar()
        self.currentCDN.set('')

        # 刷新类型
        self.supportGroup = LabelFrame(self.master, text="刷新类型")
        self.supportGroup.pack(padx=10, pady=10, fill=BOTH)

        self.currentSupport = StringVar()
        self.currentSupport.set("")

        # 刷新内容
        self.contentGroup = LabelFrame(self.master, text="刷新内容")
        self.contentGroup.pack(padx=10, pady=10, fill=BOTH)

        self.pushContentText = Text(self.contentGroup, bg = "#ffffff", height=10, width=50)
        self.pushContentText.grid(row = 0,column = 1, padx = 5, pady = 5)

        # 返回结果
        returnGroup = LabelFrame(self.master, text="刷新结果")
        scrollbar = Scrollbar(returnGroup)
        scrollbar.pack(side=RIGHT, fill=Y)
        returnGroup.pack(padx=10, pady=10, fill=BOTH)

        self.pushReturnText = Text(returnGroup, bg = "#000000", fg="#45b100", height=5, width=50, state = DISABLED, yscrollcommand=scrollbar.set)
        self.pushReturnText.grid(row = 0,column = 1, padx = 5, pady = 5)
        scrollbar.config(command=self.pushReturnText.yview)
        self.pushReturnText.pack()

        # 刷新按钮
        frame = Frame(self.master)
        frame.pack()

        self.pushBtn = Button(frame, text="刷新", width=20)
        self.pushBtn.grid(row = 0,column = 1, padx = 5, pady = 10)

    def initMenu(self):
        menubar = Menu(self.master)
        menubar.add_command(label="服务商设置", command=self.menuSetCDN)
        menubar.add_command(label="关于软件", command=self.menuAbout)
        self.master.config(menu=menubar)

    def menuSetCDN(self):
        CDNManageFrame(self.master, self.onCDNManageClose)

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
                radio.bind('<Button-1>', self.onSelectedCDN)
                radio.pack(side=LEFT)
                radio.grid(row = 0,column = i, padx = 5, pady = 5)
                if i == 0 :
                    radio.invoke()
                    self.updateSupportList()
                i = i + 1
        else:
            Label(self.cdnGroup, text=u'请先从菜单中设置服务商', style='tip.TLabel').grid(row = 0,column = 0, padx = 5, pady = 5).pack()

    def updateSupportList(self):
        for child in self.supportGroup.pack_slaves():
            child.destroy()

        supports = self.getValidSupport()
        if supports :
            i = 0
            for support in supports:
                radio = Radiobutton(self.supportGroup, text=support[1], variable=self.currentSupport, value=support[0])
                radio.pack(side=LEFT)
                radio.grid(row = 0,column = i, padx = 5, pady = 5)
                if i == 0 :
                    radio.invoke()
                i = i + 1
        else:
            Label(self.supportGroup, text=u'请先选择服务商', style='tip.TLabel').grid(row = 0,column = 0, padx = 5, pady = 5)

    def bindEvent(self):
        self.pushBtn.bind('<Button-1>', self.onPush)

    def onCDNManageClose():
        self.updateCDNList()

    def onPush(self, event):

        CDNId = self.currentCDN.get()
        support = self.currentSupport.get()

        if CDNId == '' or support == '':
            return

        self.pushBtn.config(state =  DISABLED)

        content = [line for line in self.pushContentText.get(0.0,END).split("\n") if line.strip() != ""]

        CDN = CDNFactory.get(CDNId, Config.getAccount(CDNId))

        getattr(CDN, support)(content)

        self.pushBtn.config(state =  ACTIVE)


    def onSelectedCDN(self, event):
        self.updateSupportList()

        
    def getValidCDN(self):
        allCDN = CDNFactory.all()
        if len(Config.validCDN) > 0:
            return [a for v in Config.validCDN for a in allCDN if v[0] == a['id']]
        else:
            return None

    def getValidSupport(self):
        CDNId = self.currentCDN.get()
        cdn = filter(lambda cdn:cdn['id'] == CDNId, self.getValidCDN())
        return len(cdn) > 0 and cdn[0]['support'] or None


class CDNManageFrame:

    def __init__(self, parent, onClose = None):
        top = self.top = Toplevel(parent)
        top.grab_set()
        top.title(u"设置CDN服务商帐号")

        self.currentCDN = StringVar()
        self.currentCDN.set('')

        self.CDNSer = Combobox(top, textvariable= self.currentCDN, state="readonly")
        self.CDNSer['values'] = ("a", "b", "c")
        self.CDNSer.grid(row=0, column=1, padx = 10, pady = 10)

        Label(top, text=u"服 务 商:").grid(row=0, padx = 10, pady = 10)
        Label(top, text=u"刷新帐号:").grid(row=1, padx = 10, pady = 10)
        Label(top, text=u"刷新密码:").grid(row=2, padx = 10, pady = 10)

        self.usename = Entry(top)
        self.password = Entry(top)

        self.usename.grid(row=1, column=1, padx = 10, pady = 10)
        self.password.grid(row=2, column=1, padx = 10, pady = 10)

        self.ok = Button(top, text="确认", width=15)
        self.ok.grid(row = 3,column = 0, columnspan=2, padx = 5, pady = 10)
        
def run():

    root = Tk()
    app = MainFrame(root)
    root.mainloop()


if __name__ == '__main__':
    
    run()