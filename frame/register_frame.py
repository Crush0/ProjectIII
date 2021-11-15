import tkinter.messagebox
from tkinter import *

from frame import login_frame
from service import user_service


class RegisterFrame:
    width = 500
    height = 350
    __reg_btn = None

    def __init__(self):
        self.__root = Tk()
        screenwidth = self.__root.winfo_screenwidth()
        screenheight = self.__root.winfo_screenheight()
        align_str = '%dx%d+%d+%d' % (
            self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.__root.geometry(align_str)
        self.__root.resizable(width=False, height=False)
        self.__username = StringVar()
        self.__password = StringVar()
        self.__twice = StringVar()
        self.initGui()

    def mainloop(self):
        self.__root.mainloop()

    def initGui(self):
        self.__root.title("用户注册")
        user_label = Label(self.__root, text="用    户    名：")
        user_label.place(x=110, y=80, anchor=W, width=80, height=40)
        pass_label = Label(self.__root, text="密        码：")
        pass_label.place(x=110, y=150, anchor=W, width=80, height=40)
        twice_label = Label(self.__root, text="在输入一次：")
        twice_label.place(x=110, y=220, anchor=W, width=80, height=40)
        user_input = Entry(self.__root, textvariable=self.__username, font=('microsoft yahei', 16, 'bold'))
        user_input.place(x=200, y=80, anchor=W, width=150, height=40)
        pass_input = Entry(self.__root, textvariable=self.__password, font=('microsoft yahei', 16, 'bold'), show="*")
        pass_input.place(x=200, y=150, anchor=W, width=150, height=40)
        twice_input = Entry(self.__root, textvariable=self.__twice, font=('microsoft yahei', 16, 'bold'), show="*")
        twice_input.place(x=200, y=220, anchor=W, width=150, height=40)
        self.__reg_btn = Button(self.__root, text="注    册",command=self.register)
        self.__reg_btn.place(x=160, y=300, anchor=W, width=80, height=40)
        logout_btn = Button(self.__root, text="返    回", command=self.open_login)
        logout_btn.place(x=260, y=300, anchor=W, width=80, height=40)

    def open_login(self):
        self.__root.destroy()
        root = Tk()
        login_frame.LoginFrame(root)

    def register(self):
        rs = user_service.UserService.register(self.__username.get(),self.__password.get(),self.__twice.get())
        if rs['result']:
            tkinter.messagebox.showinfo('信息','注册成功,请登录')
            self.open_login()
        else:
            tkinter.messagebox.showerror('错误',rs['message'])

