# -*- coding: utf-8 -*-  

import re
import sys
import os

from Tkinter import *
from ttk import *
import Tkconstants
import tkSimpleDialog

from Config import Config
from CDN import *

cfg = Config()
cfg.init()

class MainFrame:

    def __init__(self, master):
        
        self.master = master

        self.initFrame()
        self.initMenu()
        self.updateCDNList()
        self.bindEvent()

        self.old_stdout  =  sys.stdout

    def initFrame(self):

        self.master.title(u'CDN刷新工具')
        self.master.resizable(False, False)
        self.master.maxsize(450, 700)
        # self.master.iconbitmap("logo.ico")

        # 服务商
        self.cdnGroup = LabelFrame(self.master, text=u"CDN服务商")
        self.cdnGroup.pack(padx=10, pady=10, fill=BOTH)

        self.currentCDN = StringVar()
        self.currentCDN.set('')

        # 刷新类型
        self.supportGroup = LabelFrame(self.master, text=u"刷新类型")
        self.supportGroup.pack(padx=10, pady=10, fill=BOTH)

        self.currentSupport = StringVar()
        self.currentSupport.set("")

        self.currentSupportCaption = StringVar()
        self.currentSupportCaption.set("")

        # 刷新内容
        self.contentGroup = LabelFrame(self.master, text=u"刷新内容")
        self.contentGroup.pack(padx=10, pady=10, fill=BOTH)

        self.pushContentText = Text(self.contentGroup, bg = "#ffffff", height=10)
        self.pushContentText.pack(fill=BOTH, padx = 5, pady = 5)
        Label(self.contentGroup, style='tip.TLabel', textvariable=self.currentSupportCaption).pack(side=LEFT, pady = 5, padx=5)

        # 返回结果
        returnGroup = LabelFrame(self.master, text=u"刷新结果")
        scrollbar = Scrollbar(returnGroup)
        scrollbar.pack(side=RIGHT, fill=Y)
        returnGroup.pack(padx=10, pady=10, fill=BOTH)

        self.pushReturnText = Text(returnGroup, bg = "#000000", fg="#45b100", height=5, state = DISABLED, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.pushReturnText.yview)
        self.pushReturnText.pack(fill=BOTH, pady=5, padx=5)

        sys.stdout = StdoutRedirector(self.pushReturnText)

        # 刷新按钮
        frame = Frame(self.master)
        frame.pack()

        self.pushBtn = Button(frame, text=u"刷新", width=20)
        self.pushBtn.grid(row = 0,column = 1, padx = 5, pady = 10)

    def initMenu(self):
        menubar = Menu(self.master)
        menubar.add_command(label=u"服务商设置", command=self.menuSetCDN)
        self.master.config(menu=menubar)

    def menuSetCDN(self):
        CDNManageFrame(self.master, self.onCDNManageClose)

    def updateCDNList(self):
        for child in self.cdnGroup.pack_slaves():
            child.destroy()

        validCDN = self.getValidCDN()
        if validCDN :
            frist = True
            for cdn in validCDN:
                radio = Radiobutton(self.cdnGroup, text=cdn['name'], variable=self.currentCDN, value=cdn['id'], command=self.onSelectedCDN)
                radio.pack(side=LEFT ,padx = 5, pady = 5)
                if frist :
                    radio.invoke()
                    frist = False
        else:
            Label(self.cdnGroup, text=u'请先从菜单中设置服务商', style='tip.TLabel').pack(pady = 10)
            self.updateSupportList()

    def updateSupportList(self):
        for child in self.supportGroup.pack_slaves():
            child.destroy()

        supports = self.getValidSupport()
        if supports :
            frist = True
            for support in supports:
                radio = Radiobutton(self.supportGroup, text=support[1], variable=self.currentSupport, value=support[0], command=self.onSelectedSupport)
                radio.pack(side=LEFT, padx = 5, pady = 5)
                if frist :
                    radio.invoke()
                    frist = False
        else:
            Label(self.supportGroup, text=u'请先选择服务商', style='tip.TLabel').pack(pady = 10)

    def bindEvent(self):
        self.pushBtn.bind('<ButtonRelease-1>', self.onPush)
        self.master.protocol("WM_DELETE_WINDOW", self.onCloseMainFrame)

    def onCloseMainFrame(self):
        sys.stdout = self.old_stdout
        self.master.destroy()

    def onCDNManageClose(self):
        self.updateCDNList()

    def onPush(self, event):

        CDNId = self.currentCDN.get()
        support = self.currentSupport.get()

        if CDNId == '' or support == '':
            return

        self.pushBtn.config(state =  DISABLED)

        content = [line for line in self.pushContentText.get(0.0,END).split("\n") if line.strip() != ""]

        CDN = CDNFactory.get(CDNId, cfg.getAccount(CDNId))

        getattr(CDN, support)(content)

        self.pushBtn.config(state =  ACTIVE)


    def onSelectedCDN(self):
        self.updateSupportList()

    def onSelectedSupport(self):
        supports = self.getValidSupport()
        curSupport = self.currentSupport.get()
        for s in supports:
            if s[0] == curSupport:
                return self.currentSupportCaption.set(s[2])

        
    def getValidCDN(self):
        allCDN = CDNFactory.all()
        if len(cfg.validCDN) > 0:
            return [a for v in cfg.validCDN for a in allCDN if v[0] == a['id']]
        else:
            return None

    def getValidSupport(self):
        CDNId = self.currentCDN.get()
        CDNS = self.getValidCDN()
        cdn = CDNS and filter(lambda cdn:cdn['id'] == CDNId, CDNS) or []
        return len(cdn) > 0 and cdn[0]['support'] or None


class CDNManageFrame:

    def __init__(self, parent, onClose = None):

        top = self.top = Toplevel(parent)
        top.grab_set()
        top.resizable(False, False)
        top.title(u"设置CDN服务商帐号")
        # top.iconbitmap("logo.ico")

        cfg = Config()

        self.closeCallback = onClose

        self.CDNSerList = Combobox(top, state="readonly")
        self.CDNSerList['values'] = [cdn['name'] for cdn in CDNFactory.all()]
        self.CDNSerList.grid(row=0, column=1, padx = 10, pady = 10, sticky=W)

        Label(top, text=u"服务商").grid(row=0, padx = 10, pady = 10, sticky=E)
        Label(top, text=u"刷新帐号").grid(row=1, padx = 10, pady = 10, sticky=E)
        Label(top, text=u"刷新密码").grid(row=2, padx = 10, pady = 10, sticky=E)

        self.username = StringVar()
        self.username.set('')
        self.password = StringVar()
        self.password.set('')

        Entry(top, textvariable=self.username).grid(row=1, column=1, padx = 10, pady = 10, sticky=W+E+N+S)
        Entry(top, textvariable=self.password).grid(row=2, column=1, padx = 10, pady = 10, sticky=W+E+N+S)

        self.ok = Button(top, text=u"保存", width=15)
        self.ok.grid(row = 3,column = 0, columnspan=2, padx = 5, pady = 10)

        self.bindEvent()

    def bindEvent(self):
        self.CDNSerList.bind('<<ComboboxSelected>>', self.onSelectedCDN)
        self.ok.bind('<ButtonRelease-1>', self.onSave)
        self.top.protocol("WM_DELETE_WINDOW", self.onCloseManage)

    def onCloseManage(self):
        self.closeCallback()
        self.top.destroy()

    def onSave(self, event):
        allCDN = CDNFactory.all()
        index = self.CDNSerList.current()
        if index < 0:
            return

        username = self.username.get()
        password = self.password.get()
        cdnId = allCDN[index]['id']

        if username != '' and password != '':
            self.ok.config(state =  DISABLED)
            cfg.saveAccount(cdnId, username, password)
            self.ok.config(state =  ACTIVE)

            self.onCloseManage()

    def onSelectedCDN(self, evnet):
        allCDN = CDNFactory.all()
        index = self.CDNSerList.current()
        username = password = ''

        if index > -1:
            cdnId = allCDN[index]['id']
            account = cfg.getAccount(cdnId)
            if account:
                username = account[0]
                password = account[1]

        self.username.set(username)
        self.password.set(password)


class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.config(state = NORMAL)
        self.text_space.insert('end', string)
        self.text_space.see('end')
        self.text_space.config(state = DISABLED)
        
def run():

    root = Tk()
    app = MainFrame(root)
    root.mainloop()


if __name__ == '__main__':
    
    run()