import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox
import time

disableFlag = False
shiftFlag = False

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

#Here come all button handlers

def key_enter(textPad, event, socket):
    s = textPad.index(INSERT)
    print s

def key_backspace(textPad, event, socket):
    print "backspace"
    s = textPad.index(INSERT)
    point_index = s.index(".")
    index1 = int(s[:point_index])
    index2 = int(s[point_index + 1:])
    print "%d.%d" % (index1, index2 - 1)

def key_disable(textPad, event, socket):
    textPad.config(state=DISABLED)
    global disableFlag
    disableFlag = True

def mouse_button(textPad, event, socket):
    textPad.config(state=NORMAL)

def key_shift(textPad, event, socket):
    global shiftFlag
    shiftFlag = True

def key(textPad, event, socket):
    global disableFlag
    global shiftFlag
    if disableFlag == True:
        print "disabled"
        if event.keycode != 37:
            disableFlag = False
    else:
        #print event.keycode
        #Shift handling
        if shiftFlag == True:
            print "shift"
            s = textPad.index(INSERT)
            output(textPad, s, socket)
            shiftFlag = False
        else:
            #Block output for Arrows keys
            if event.keycode == 113 or event.keycode == 114 or \
                    event.keycode == 112 or event.keycode == 116:
                return
            #Block output for Ctrl, Shift, BackSpace
            if event.keycode == 37 or event.keycode == 50 or \
                            event.keycode == 22:
                return
            textPad.config(state=NORMAL)
            s = textPad.index(INSERT)
            output(textPad, s, socket)

def output(textPad, s, socket):
    point_index = s.index(".")
    index1 = int(s[:point_index])
    index2 = int(s[point_index + 1:])
    out = textPad.get("%d.%d" % (index1, index2 - 1), "%d.%d" % (index1, index2))
    if out:
        print "%d.%d" % (index1, index2 - 1), out


def key_press(textPad, event, socket):
    textPad.config(state=DISABLED)
    time.sleep(0.2)
    textPad.config(state=NORMAL)

def run_gui(socket, file=""):
    root = Tkinter.Tk(className=" Collaborative Text Editor")
    textPad = ScrolledText(root, width=100, height=80)
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
    #Insert given text
    if file:
        f = open(file, 'r')
        textPad.insert(END,f.read())
    #Keybord bindings to virtual events
    textPad.bind("<Button-1>",lambda event: mouse_button(textPad, event,"Hello"))
    textPad.bind("<Control-v>", lambda event: key_disable(textPad, event,"Hello"))
    textPad.bind("<Control-c>", lambda event: key_disable(textPad, event,"Hello"))
    textPad.bind("<Shift_L>", lambda event: key_shift(textPad, event,"Hello"))
    textPad.bind("<Delete>", lambda event: key_disable(textPad, event,"Hello"))
    textPad.bind("<Insert>", lambda event: key_disable(textPad, event,"Hello"))
    textPad.bind("<Return>", lambda event: key_enter(textPad, event,"Hello"))
    textPad.bind("<BackSpace>", lambda event: key_backspace(textPad, event,"Hello"))
    textPad.bind("<Key>", lambda event: key_press(textPad, event,"Hello"))
    textPad.bind("<KeyRelease>", lambda event: key(textPad, event,"Hello"))


    textPad.pack()
    root.mainloop()

if __name__ == "__main__":
    run_gui("127.0.0.1","test.txt")