# -*- coding: utf-8 -*-  

from Tkinter import *
import Tkconstants

from CDN import *

__version__="0.1"
__author__ = "libo"
__email__ = "hellolibo@gmail.com"


class App:

    def __init__(self, master):


        master.title(u'CDN刷新工具')
        master.resizable(False, False)

        cdnGroup = LabelFrame(master, text="CDN服务商", padx=5, pady=5)
        cdnGroup.pack(padx=10, pady=10, fill=BOTH)

        self.cdnServer = StringVar()
        self.cdnServer.set("ws")
        self.CDNListCCA = Radiobutton(cdnGroup, text="ChinaCache", variable=self.cdnServer, value="cca")
        self.CDNListWS = Radiobutton(cdnGroup, text="网宿", variable=self.cdnServer, value="ws")
        self.CDNListWS.grid(row = 0,column = 1, padx = 5, pady = 5)
        self.CDNListWS.select()
        self.CDNListCCA.grid(row = 0,column = 2, padx = 5, pady = 5)

        typeGroup = LabelFrame(master, text="刷新类型", padx=5, pady=5)
        typeGroup.pack(padx=10, pady=10, fill=BOTH)

        self.pushType = StringVar()
        self.pushType.set("url")
        self.pushTypeUrl = Radiobutton(typeGroup, text="网址", variable=self.pushType, value="url")
        self.pushTypeDir = Radiobutton(typeGroup, text="目录", variable=self.pushType, value="dir")
        self.pushTypeSku = Radiobutton(typeGroup, text="SKU", variable=self.pushType, value="sku")
        self.pushTypeUrl.grid(row = 0,column = 1, padx = 5, pady = 5)
        self.pushTypeDir.grid(row = 0,column = 2, padx = 5, pady = 5)
        self.pushTypeSku.grid(row = 0,column = 3, padx = 5, pady = 5)
        self.pushTypeUrl.select()


        contentGroup = LabelFrame(master, text="刷新内容", padx=5, pady=5)
        contentGroup.pack(padx=10, pady=10, fill=BOTH)

        self.pushContentText = Text(contentGroup, bg = "#ffffff", height=10, width=50)
        self.pushContentText.grid(row = 0,column = 1, padx = 5, pady = 5)


        returnGroup = LabelFrame(master, text="刷新结果", padx=5, pady=5)
        self.scrollbar = Scrollbar(returnGroup)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        returnGroup.pack(padx=10, pady=10, fill=BOTH)

        self.pushReturnText = Text(returnGroup, bg = "#000000", fg="#45b100", height=5, width=50, state = DISABLED, yscrollcommand=self.scrollbar.set)
        self.pushReturnText.grid(row = 0,column = 1, padx = 5, pady = 5)
        self.scrollbar.config(command=self.pushReturnText.yview)
        self.pushReturnText.pack()

        frame = Frame(master, padx = 10, pady = 10)
        frame.pack()

        self.pushBtn = Button(frame, text="刷新", width=20, command=self.push)
        self.pushBtn.grid(row = 0,column = 1, padx = 5, pady = 10)

    def progress(self, url, returnInfo):
        self.writeInfo('\n'.join([
                'Push ws-CDN url&directory:',
                '\n'.join(url),
                returnInfo
            ]))

    def writeInfo(self, info):
        self.pushReturnText.config(state =  NORMAL)
        self.pushReturnText.insert(END, info)
        self.pushReturnText.yview(END)
        self.pushReturnText.config(state =  DISABLED)

    def push(self):
        
        self.pushBtn.config(state =  DISABLED)

        cdnServer = self.cdnServer.get()
        pushType = self.pushType.get()
        content = [re.sub(r'^http:\/\/', '', line) for line in self.pushContentText.get(0.0,END).split("\n") if line.strip() != ""]

        getattr(self.CDN, pushType)(content)
        # self.pushContentText.delete(1.0, END)
        self.pushBtn.config(state =  ACTIVE)
        

if __name__ == '__main__':
    
    root = Tk()
    App(root)
    root.mainloop()