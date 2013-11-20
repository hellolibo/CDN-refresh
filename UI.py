# -*- coding: utf-8 -*-  

from Tkinter import *
import Tkconstants

class MainFrame:

    def __init__(self, master, Config, CDN):

        self.Config = Config
        self.CDN = CDN

        self.currentCDN = None

        # 初始化
        self.initFrame()
        self.updateCDNList()
        self.bindEvent()

    def initFrame(self):

        master.title(u'CDN刷新工具')
        master.resizable(False, False)

        # 服务商
        self.cdnGroup = LabelFrame(master, text="CDN服务商", padx=5, pady=5)
        self.cdnGroup.pack(padx=10, pady=10, fill=BOTH)

        self.cdnServer = StringVar()
        self.cdnServer.set('')


        # 刷新类型
        self.typeGroup = LabelFrame(master, text="刷新类型", padx=5, pady=5)
        self.typeGroup.pack(padx=10, pady=10, fill=BOTH)

        self.pushType = StringVar()
        self.pushType.set("")

        # 刷新内容
        self.contentGroup = LabelFrame(master, text="刷新内容", padx=5, pady=5)
        self.contentGroup.pack(padx=10, pady=10, fill=BOTH)

        self.pushContentText = Text(contentGroup, bg = "#ffffff", height=10, width=50)
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

        self.pushBtn = Button(frame, text="刷新", width=20, command=self.push)
        self.pushBtn.grid(row = 0,column = 1, padx = 5, pady = 10)
    
    def updateCDNList(self):

        cdnList = self.CDN.get(Config.on())

        if cdnList :

            for cdn, i in cdnList, range(1, len(cdnList)):
                radio = Radiobutton(self.cdnGroup, text=cdn.name, variable=self.cdnServer, value=cdn.id)
                radio.grid(row = 0,column = i, padx = 5, pady = 5)
                radio.bind('<Button-1>', self.onSelectedCDN)
                if i == 1 :
                    self.currentCDN = cdn
                    radio.select()
        else:
            pass

    def updatePushTypeList(self):

        typeList = self.currentCDN.support

        for type, i in typeList, range(1, len(typeList)):
            radio = Radiobutton(typeGroup, text=type.name, variable=self.pushType, value=type.id)
            radio.grid(row = 0,column = i, padx = 5, pady = 5)
            if i == 1 :
                radio.select()



    def bindEvent(self):

        self.pushBtn.bind('<Button-1>', self.onPush)


    def onPush(self):

        self.pushBtn.config(state =  DISABLED)

        cdnServer = self.cdnServer.get()
        pushType = self.pushType.get()

        content = [re.sub(r'^http:\/\/', '', line) for line in self.pushContentText.get(0.0,END).split("\n") if line.strip() != ""]

        CDN = getattr(self.CDN, cdnServer)

        getattr(CDN, pushType)(content)

        self.pushBtn.config(state =  ACTIVE)

        

    def onSelectedCDN(self, event):

        self.updatePushTypeList()

        
        
      