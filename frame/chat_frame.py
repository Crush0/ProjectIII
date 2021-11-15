import _thread
import time
import tkinter.messagebox
import uuid
from tkinter import *

from service import message_service


class ChatFrame:
    width = 975
    height = 660

    def __init__(self, user, friend):
        self.user = user
        self.friend = friend
        self.__root = Tk()
        self.chat_info = None
        self.textarea = None
        self.message = []
        screenwidth = self.__root.winfo_screenwidth()
        screenheight = self.__root.winfo_screenheight()
        align_str = '%dx%d+%d+%d' % (
            self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.__root.geometry(align_str)
        self.__root.resizable(width=False, height=False)
        self.initGui()
        self.thread = _thread
        self.thread.start_new_thread(ChatFrame.getMessage,(self,))
        self.__root.protocol("WM_DELETE_WINDOW",self.destory)
        self.__root.mainloop()

    def destory(self):
        self.thread.exit()
        self.__root.destroy()

    def initGui(self):
        self.__root.title(self.friend['username'])
        self.chat_info = Listbox(self.__root)
        self.chat_info['width'] = 150
        self.chat_info['height'] = 30
        self.chat_info.pack()
        self.textarea = Text(self.__root, width=65, height=50, font=('microsoft yahei', 16, 'bold'))
        self.textarea.pack(side=LEFT)
        send_btn = Button(self.__root, text="发送", font=('microsoft yahei', 16, 'bold'), command=self.send)
        send_btn['width'] = 130
        send_btn['height'] = 110
        send_btn.pack(side=LEFT)

    def send(self):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.chat_info.insert(END, f'({t}) {self.user["username"]}：{self.textarea.get("0.0", END)}')
        u = uuid.uuid1()
        self.message.append(str(u))
        rs = message_service.MessageService.sendMsg(self.user['id'], self.friend['id'],self.textarea.get("0.0", END),u)
        if rs['result']:
            self.textarea.delete('0.0', END)
        else:
            tkinter.messagebox.showerror('错误', rs['message'])

    def getMessage(self):
        while True:
            time.sleep(0.5)
            rs = message_service.MessageService.get_messageNear(fromId=self.friend['id'],toId=self.user['id'])
            for msg in rs:
                try:
                    self.message.index(msg['uuid'])
                except Exception:
                    self.message.append(msg['uuid'])
                    str = self.user['username'] if msg['from'] == self.user['id'] else self.friend['username']
                    self.chat_info.insert(END, f'({msg["time"]}) {str}：{msg["message"]}')
