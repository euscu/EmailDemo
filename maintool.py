# -*- coding: utf-8 -*-
# @Time    : 2017/3/16 23:28
# @Author  : euscu
# @remark  :
__author__ = 'euscu'

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
from AliTool import mytool
import threading


class alitool(object):
    def __init__(self, master):
        self.master = master
        self.label1 = Label(master, text='关键词')
        self.entry1 = Entry(master, )
        self.label5 = Label(master, text='起始页数')
        self.entry2 = Entry(master, width=10, text='1')
        self.label6 = Label(master, text='终止页数')
        self.entry3 = Entry(master, width=10)
        self.btn1 = Button(master, text='选择保存位置', command=self.store_path)
        self.label2 = Label(master, text='请设置保存位置')
        self.btn2 = Button(master, text='start!', width=30, command=self.start)
        self.label3 = Label(master, text='提示：')
        self.label4 = Label(master, )
        # 进度条，创建但不放入布局
        self.progressbar = Progressbar(mode="indeterminate", maximum=20)
        # 布局
        self.label1.grid(row=0, column=0)
        self.entry1.grid(row=0, column=1)
        self.label5.grid(row=1, column=0)
        self.entry2.grid(row=1, column=1, sticky=W)
        self.label6.grid(row=2, column=0)
        self.entry3.grid(row=2, column=1, sticky=W)
        self.btn1.grid(row=3, column=0)
        self.label2.grid(row=3, column=1)
        self.btn2.grid(row=4, column=0, columnspan=2)
        self.label3.grid(row=5, column=0)
        self.label4.grid(row=5, column=1)

    def store_path(self):
        # global root
        file = askdirectory()
        self.label2['text'] = file

    def get_message(self):
        self.label4['text'] = mytool.message

    def judge(self):
        judge=True
        mystr = self.entry2.get().strip() + self.entry3.get().strip()
        print(mystr)
        for x in mystr:
            print(x, ord(x))
            if ord(x) < 48 or ord(x) > 57:
                self.label4['text'] = '页数只能是正整数'
                judge=False
                break
            else:
                continue
        return judge

    def start(self):
        #    先进行一系列判断
        if self.entry1.get().strip() == "" or self.entry2.get().strip() == "" or self.entry3.get().strip() == "":
            self.label4['text'] = "关键词和页数不能为空"
        else:
            result=self.judge()
            if result==True:
                if int(self.entry2.get().strip()) > 100 or int(self.entry3.get().strip()) > 100:
                    self.label4['text'] = '不能爬取超过一百页'
                else:
                    if (int(self.entry3.get().strip()) - int(self.entry2.get().strip())) < 1:
                        self.label4['text'] = '无页数'
                    else:
                        if self.label2['text'].strip() == "" or self.label2['text'] == "请设置保存位置":
                            self.label4['text'] = '请设置保存位置'
                        else:
                            self.thread = threading.Thread(target=mytool.login_url, name='LoopThread', args=(
                                self.entry1.get().strip(), int(self.entry2.get().strip()),
                                int(self.entry3.get().strip()), self.label2['text']))
                            self.btn2.config(state="disabled")
                            self.progressbar.grid(row=6, column=1, columnspan=2)
                            self.label4['text'] = '爬取中，请耐心等待'
                            self.master.update()
                            self.thread.start()
                            self.progressbar.start()
                            # 每秒查看是否完成
                            self.master.after(1000, self.check_completed)

    def check_completed(self):
        if self.thread.is_alive():
            self.master.after(1000, self.check_completed)
        else:
            # if thread has finished stop and reset everything
            self.progressbar.stop()
            self.progressbar.grid_forget()
            self.btn2.config(state="enabled")
            self.label4['text'] = '爬取完成'
            self.master.update()


if __name__ == '__main__':
    root = Tk()
    root.title('AliTool')
    myalitool = alitool(root)
    root.mainloop()
