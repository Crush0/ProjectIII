import tkinter.messagebox
from tkinter import *

from service import user_service


class AddFrame:
    width = 500
    height = 120
    def __init__(self,user):
        self.user = user
        self.__root = Tk()
        screenwidth = self.__root.winfo_screenwidth()
        screenheight = self.__root.winfo_screenheight()
        align_str = '%dx%d+%d+%d' % (
            self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.__root.geometry(align_str)
        self.__root.resizable(width=False, height=False)
        self.user_input = None
        self.initGui()
        self.__root.mainloop()

    def initGui(self):
        self.__root.title("添加好友")  # #窗口标题
        user_label = Label(self.__root, text="好友名：")
        user_label.place(x=80, y=60, anchor=W, width=80, height=40)
        self.user_input = Entry(self.__root, font=('microsoft yahei', 16, 'bold'))
        self.user_input.place(x=150, y=60, anchor=W, width=150, height=40)
        add_btn = Button(self.__root, text="发送请求", command=self.send)
        add_btn.place(x=320, y=60, anchor=W, width=80, height=40)

    def send(self):
        if self.user['username'] == self.user_input.get():
            tkinter.messagebox.showerror('添加好友', '你不能添加自己为好友')
            return
        rs = user_service.UserService.addFriend(self.user['id'],self.user_input.get())
        if rs['result']:
            tkinter.messagebox.showinfo('添加好友',rs['message'])
        else:
            tkinter.messagebox.showerror('添加好友', rs['message'])