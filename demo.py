# -*- coding: utf-8 -*-
# @Time    : 2017/4/18 23:34
# @Author  : euscu
# @remark  : 
__author__ = 'euscu'

from tkinter import *
from tkinter.ttk import *
import threading
from smtplib import SMTP
from email.header import Header
from email.mime.text import MIMEText


class mymail(object):
    def __init__(self, master):
        self.master = master
        self.label1 = Label(master, text='发送到:')
        self.entry1 = Entry(master, width=40)
        self.label2 = Label(master, text="标题:")
        self.entry2 = Entry(master, width=40)
        self.label3 = Label(master, text="内容:")
        self.text1 = Text(master, width=40, height=4)
        self.progressbar = Progressbar(mode="indeterminate", maximum=20)
        self.btn1 = Button(master, text='发送', command=self.toSendMail)
        self.label4 = Label(master, width=40)

        # 发送到：
        self.label1.grid(row=0, column=0)
        self.entry1.grid(row=0, column=1)
        # 标题：
        self.label2.grid(row=1, column=0)
        self.entry2.grid(row=1, column=1)
        # 内容
        self.label3.grid(row=2, column=0)
        self.text1.grid(row=2, column=1)
        self.btn1.grid(row=3, column=0)
        self.label4.grid(row=3, column=1)

    def toSendMail(self):
        mymsg = self.text1.get("0.0", "end")
        mysubject = self.entry2.get().strip()
        addresses = self.entry1.get().strip().split(",")
        if mysubject == "":
            if mymsg == "":
                mymailsender = MailSender()
            else:
                mymailsender = MailSender(msg=mymsg)
        else:
            if mymsg == "":
                mymailsender = MailSender(mysubject)
            else:
                mymailsender = MailSender(mysubject, msg=mymsg)

        mymailsender.init_sender()
        mymailsender.send_mails(*addresses)


class MailSender(object):
    def __init__(self, mysubject="这是一封测试邮件", *, msg):
        self.__from_account = "13507590956@163.com"
        self.__from_password = "mytest2017"
        self.SMTP_host = "smtp.163.com"
        self.email_client = SMTP(self.SMTP_host)
        self.msg = MIMEText(msg, 'plain', 'utf-8')
        self.msg['Subject'] = Header(mysubject, 'utf-8')
        self.msg['From'] = "13507590956@qq.com"
        self.lock = threading.Lock()

    def init_sender(self):
        self.email_client.login(self.__from_account, self.__from_password)

    def send_mails(self, *addresses):
        for address in addresses:
            self.thread = threading.Thread(target=self.send_mail, args=(address,))
            self.thread.start()

    def send_mail(self, address):
        self.lock.acquire()
        try:
            self.msg['To'] = address
            self.email_client.sendmail(self.__from_account, address, self.msg.as_string())
        finally:
            self.lock.release()

    def quit_sender(self):
        self.email_client.quit()


if __name__ == '__main__':
    root = Tk()
    root.title('多线程群发邮件客户端')
    myalitool = mymail(root)
    root.mainloop()
