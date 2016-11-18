import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox
import time

disableFlag = False

#keybord_string = "qwertyuiopasdfghjklzxcvbnm"
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
    label = tkMessageBox.showinfo("About", "Collaborative text editor \n Developed by Bachinskiy A., Shapaval R., \
                                    Shuchorukov M., Tkachuk D. using Tk.tkinter.\n No rights left to reserve :)")



def getText():
     return textPad.get(1.0, END)

def key_enter(event):
    s = textPad.index(INSERT)
    print s

def key_backspace(event):
    s = textPad.index(INSERT)
    point_index = s.index(".")
    index1 = int(s[:point_index])
    index2 = int(s[point_index + 1:])
    #out = textPad.get("%d.%d" % (index1, index2 - 1), "%d.%d" % (index1, index2))
    print "%d.%d" % (index1, index2 - 1)

def key_disable(event):
    textPad.config(state=DISABLED)
    global disableFlag
    disableFlag = True


def mouse_button(event):
    textPad.config(state=NORMAL)


def key(event):
    print event.keycode
    global disableFlag
    if disableFlag == True:
        print "disabled"
    elif disableFlag == True and event.keycode != 37:
        disableFlag = False
    else:
        #Block output for Arrows keys
        if event.keycode == 113 or event.keycode == 114 or \
                event.keycode == 112 or event.keycode == 116:
            return
        #Block output for Ctrl button
        if event.keycode == 37:
            return
        #Block output for v if Ctrl pressed
        textPad.config(state=NORMAL)
        s = textPad.index(INSERT)
        point_index = s.index(".")
        index1 = int(s[:point_index])
        index2 = int(s[point_index+1:])
        out = textPad.get("%d.%d" % (index1, index2 - 1), "%d.%d" % (index1, index2))
        if out:
            print "%d.%d" % (index1, index2 - 1), out

def key_press(event):
    textPad.config(state=DISABLED)
    time.sleep(0.2)
    textPad.config(state=NORMAL)


menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open...", command=open_command)
filemenu.add_command(label="Save", command=save_command)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_command)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=about_command)

#Keybord bindings to virtual events
textPad.bind("<Button-1>",mouse_button)
textPad.bind("<Control-v>", key_disable)
textPad.bind("<Control-c>", key_disable)
textPad.bind("<Delete>", key_disable)
textPad.bind("<Insert>", key_disable)
textPad.bind("<Return>", key_enter)
textPad.bind("<BackSpace>", key_backspace)
textPad.bind("<Key>", key_press)
textPad.bind("<KeyRelease>", key)


textPad.pack()
root.mainloop()