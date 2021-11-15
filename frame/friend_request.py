import tkinter.messagebox
from tkinter import *

from service import user_service


class FriendRequestFrame:
    width = 500
    height = 350

    def __init__(self, user):
        self.user = user
        self.users = []
        self.__root = Tk()
        screenwidth = self.__root.winfo_screenwidth()
        screenheight = self.__root.winfo_screenheight()
        align_str = '%dx%d+%d+%d' % (
            self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.__root.geometry(align_str)
        self.__root.resizable(width=False, height=False)
        self.user_input = None
        self.requestList = None
        self.initGui()
        self.initDate()
        self.__root.mainloop()

    def initGui(self):
        self.__root.title("好友申请")
        frame = Frame(self.__root)
        frame.place(x=0, y=0, relwidth=100, relheight=80)
        self.requestList = Listbox(frame)
        self.requestList.pack(side=TOP, fill=BOTH)
        accept_btn = Button(self.__root, text="接    受",
                         command=lambda: self.processFriend(self.user['id'], 100))
        ignore_btn = Button(self.__root, text="忽    略",
                         command=lambda: self.processFriend(self.user['id'], 0))
        deny_btn = Button(self.__root, text="拒    绝",
                       command=lambda: self.processFriend(self.user['id'], -100))
        accept_btn.place(x=80, y=300, anchor=W, width=100, height=40)
        ignore_btn.place(x=190, y=300, anchor=W, width=100, height=40)
        deny_btn.place(x=300, y=300, anchor=W, width=100, height=40)

    def initDate(self):
        self.requestList.delete(0,END)
        self.users = user_service.UserService.getRequest(self.user['id'])
        for user in self.users:
            self.requestList.insert(user['index'], f'{user["username"]} 请求添加你为好友')

    def processFriend(self,userid,action):
        try:
            friendindex = self.requestList.index(ACTIVE)
            rs = user_service.UserService.processFriend(userid, self.users[friendindex]['id'], action)
        except IndexError:
            tkinter.messagebox.showerror('错误', '没有选中好友申请')
            return
        if rs['result']:
            tkinter.messagebox.showinfo('信息',rs['message'])
            self.initDate()
        else:
            tkinter.messagebox.showerror('错误',rs['message'])



if __name__ == '__main__':
    FriendRequestFrame({})
