import _thread
from tkinter import Tk

from frame import login_frame

def start():
    root = Tk()
    login_frame.LoginFrame(root)

start()