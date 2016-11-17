import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox
import time

keybord_string = "qwertyuiopasdfghjklzxcvbnm"
#[]{};:''|<>,./?1234567890-=!@#$%^&*()_+\\`~
root = Tkinter.Tk(className=" Collaborative Text Editor")
textPad = ScrolledText(root, width=100, height=80)



''' Uploading of file received from server

contents = file.read()
textPad.insert('1.0', contents)
file.close()

'''
# create a menu & define functions for each menu item

def open_command():
    file = tkFileDialog.askopenfile(parent=root, mode='rb', title='Select a file')
    if file != None:
        contents = file.read()
        textPad.insert('1.0', contents)
        file.close()


def save_command(self):
    file = tkFileDialog.asksaveasfile(mode='w')
    if file != None:
        # slice off the last character from get, as an extra return is added
        data = self.textPad.get('1.0', END + '-1c')
        file.write(data)
        file.close()


def exit_command():
    if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()


def about_command():
    label = tkMessageBox.showinfo("About", "Just Another TextPad \n Copyright \n No rights left to reserve")


def dummy():
    print "I am a Dummy Command, I will be removed in the next step"

def getText():
     return textPad.get(1.0, END)


def get_info():
    print textPad.index(INSERT)
    textPad.insert(INSERT, "Some text")
    print textPad.index(INSERT)

def key_enter(event):
    s = textPad.index(INSERT)
    print s



def key_backspace(event):
    pass

def key_disable(event):
    textPad.config(state=DISABLED)

def key(event):
    s = textPad.index(INSERT)
    point_index = s.index(".")
    index1 = int(s[:point_index])
    index2 = int(s[point_index+1:])
    out = textPad.get("%d.%d" % (index1, index2 - 1), "%d.%d" % (index1, index2))
    if out:
        print s,out

def key_press(event):
    textPad.config(state=DISABLED)
    time.sleep(0.3)
    textPad.config(state=NORMAL)


menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=dummy)
filemenu.add_command(label="Open...", command=open_command)
filemenu.add_command(label="Save", command=save_command)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_command)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=about_command)

textPad.bind("<Control-v>", key_disable)
textPad.bind("<Return>", key_enter)
textPad.bind("<BackSpace>", key_backspace)
textPad.bind("<Key>", key_press)
textPad.bind("<KeyRelease>", key)


textPad.pack()
root.mainloop()