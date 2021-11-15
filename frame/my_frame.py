import tkinter.messagebox
from tkinter import *

from frame import add_friend, friend_request, chat_frame
from service import user_service


class MyFrame:
    width = 350
    height = 800

    def __init__(self, user):
        self.user = user
        self.__root = Tk()
        self.friendList = None
        self.friends = []
        screenwidth = self.__root.winfo_screenwidth()
        screenheight = self.__root.winfo_screenheight()
        align_str = '%dx%d+%d+%d' % (
            self.width, self.height, (screenwidth - self.width) / 2 + self.width * 2, (screenheight - self.height) / 2)
        self.__root.geometry(align_str)
        self.__root.resizable(width=False, height=False)
        self.initGui()
        self.getFriend()
        self.__root.mainloop()

    def initGui(self):
        print(f'欢迎你,{self.user["username"]}!')
        self.__root.title(f'欢迎你，{self.user["username"]}!')
        logout_btn = Button(self.__root, text="登    出", command=self.__root.destroy)
        logout_btn.place(x=250, y=750, anchor=W, width=80, height=40)
        new_friend = Button(self.__root, text="新增好友", command=self.addFriend)
        new_friend.place(x=20, y=750, anchor=W, width=80, height=40)
        friend_req = Button(self.__root, text="好友请求", command=self.friendReq)
        chat_btn  = Button(self.__root,text="开始聊天",command=self.startChat)
        fresh_btn = Button(self.__root,text="刷新",command=self.getFriend)
        fresh_btn.place(x=300, y=650, anchor=W, width=40, height=40)
        chat_btn.place(x=140, y=650, anchor=W, width=80, height=40)
        friend_req.place(x=140, y=750, anchor=W, width=80, height=40)
        self.friendList = Listbox(self.__root)
        self.friendList.place(x=0,y=0,relwidth=100,height=600)

    def addFriend(self):
        add_friend.AddFrame(self.user)

    def startChat(self):
        try:
            friendindex = self.friendList.index(ACTIVE)
            friend = {
                'id':self.friends[friendindex]['id'],
                'username':self.friends[friendindex]['username']
            }
            chat_frame.ChatFrame(self.user,friend)
        except IndexError:
            tkinter.messagebox.showerror('错误', '没有选中好友')

    def getFriend(self):
        self.friends = user_service.UserService.getFriend(self.user['id'])
        self.friendList.delete(0,END)
        for user in self.friends:
            self.friendList.insert(user['index'],'1. '+user['username'])


    def friendReq(self):
        friend_request.FriendRequestFrame(self.user)

if __name__ == '__main__':
    MyFrame({'id':1,'username':'Crush'})