import tkinter.messagebox
from tkinter import *

from frame import my_frame
from frame.register_frame import RegisterFrame
from service import user_service


class LoginFrame:
    width = 500
    height = 350
    __login_btn = None

    def __init__(self,root):
        self.__root = root
        screenwidth = self.__root.winfo_screenwidth()
        screenheight = self.__root.winfo_screenheight()
        align_str = '%dx%d+%d+%d' % (
            self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.__username = StringVar()
        self.__password = StringVar()
        self.__remember = IntVar()
        self.__root.geometry(align_str)
        self.__root.resizable(width=False, height=False)
        self.initGui()
        self.__root.mainloop()

    def initGui(self):
        self.__root.title("用户登录")  # #窗口标题
        user_label = Label(self.__root,text="用户名：")
        user_label.place(x=110,y=80, anchor=W, width=80, height=40)
        pass_label = Label(self.__root, text="密    码：")
        pass_label.place(x=110, y=150, anchor=W, width=80, height=40)
        user_input = Entry(self.__root,textvariable=self.__username,font=('microsoft yahei', 16, 'bold'))
        user_input.place(x=200, y=80, anchor=W, width=150, height=40)
        pass_input = Entry(self.__root, textvariable=self.__password, font=('microsoft yahei', 16, 'bold'),show="*")
        pass_input.place(x=200, y=150, anchor=W, width=150, height=40)
        reg_btn = Button(self.__root,text="注    册",command=self.open_reg)
        reg_btn.place(x=400, y=300, anchor=W, width=80, height=20)
        self.__login_btn = Button(self.__root,text="登    录",command=self.login)
        self.__login_btn.place(x=160, y=210, anchor=W, width=80, height=40)
        logout_btn = Button(self.__root,text="退    出",command=self.close)
        logout_btn.place(x=260, y=210, anchor=W, width=80, height=40)


    def close(self):
        self.__root.destroy()

    def open_reg(self):
        self.close()
        RegisterFrame().mainloop()

    def login(self):
        rs = user_service.UserService.login(self.__username.get(),self.__password.get())
        if rs['result']:
            user = rs['user']
            self.close()
            my_frame.MyFrame(user)

        else:
            tkinter.messagebox.showerror('错误',rs['message'])
