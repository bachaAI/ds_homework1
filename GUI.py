import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox
import time

disableFlag = False
shiftFlag = False

def save_command(textPad):
    file = tkFileDialog.asksaveasfile(mode='w')
    if file != None:
        # slice off the last character from get, as an extra return is added
        data = textPad.get('1.0', END + '-1c')
        file.write(data)
        file.close()
def exit_command(root):
    if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()
def about_command():
    label = tkMessageBox.showinfo("About", "Collaborative text editor \n Developed by Bachinskiy A., Shapaval R., \
                                    Shuchorukov M., Tkachuk D. using Tk.tkinter.\n No rights left to reserve :)")

#Here come all button handlers

def key_enter(textPad, event, queue):
    s = textPad.index(INSERT)
    add_to_queue(textPad,s,queue,"ent")


def key_backspace(textPad, event, queue):
    s = textPad.index(INSERT)
    add_to_queue(textPad,s,queue,"bs")

def key_disable(textPad, event):
    textPad.config(state=DISABLED)
    global disableFlag
    disableFlag = True

def mouse_button(textPad, event):
    textPad.config(state=NORMAL)

def key_shift(textPad, event):
    global shiftFlag
    shiftFlag = True

def key(textPad, event, queue):
    #print event.keycode
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
            s = textPad.index(INSERT)
            add_to_queue(textPad, s, queue)
            shiftFlag = False
        else:
            #Block output for Arrows keys
            if event.keycode == 113 or event.keycode == 114 or \
                    event.keycode == 112 or event.keycode == 116:
                return
            #Block output for Ctrl, Shift, BackSpace
            if event.keycode == 37 or event.keycode == 50 or \
                            event.keycode == 22 or event.keycode == 36:
                return
            textPad.config(state=NORMAL)
            s = textPad.index(INSERT)
            add_to_queue(textPad, s, queue)


def key_press(textPad, event):
    textPad.config(state=DISABLED)
    time.sleep(0.2)
    textPad.config(state=NORMAL)

def add_to_queue(textPad, s, queue, key=""):
    point_index = s.index(".")
    index1 = int(s[:point_index])
    index2 = int(s[point_index + 1:])
    out = textPad.get("%d.%d" % (index1, index2 - 1), "%d.%d" % (index1, index2))
    if key:
        if key == "ent":
            queue.append("%d,%d,%s" % (index1-1, index2, key))
        if key == "bs":
            queue.append("%d,%d,%s" % (index1-1, index2-1, key))
    else:
        queue.append("%d,%d,%s" % (index1-1, index2-1, out))
    print queue

def run_gui(queue, file=""):
    root = Tkinter.Tk(className=" Collaborative Text Editor")
    textPad = ScrolledText(root, width=100, height=80)
    menu = Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Save", command= lambda x=textPad: save_command(x))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command= lambda x=root: exit_command(x))
    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About...", command=about_command)
    #Insert given text
    if file:
        f = open(file, 'r')
        textPad.insert(END,"\n")
        textPad.insert(END,f.read())
    #Keybord bindings to virtual events
    textPad.bind("<Button-1>",lambda event: mouse_button(textPad, event))
    textPad.bind("<Control-v>", lambda event: key_disable(textPad, event))
    textPad.bind("<Control-c>", lambda event: key_disable(textPad, event))
    textPad.bind("<Shift_L>", lambda event: key_shift(textPad, event))
    textPad.bind("<Delete>", lambda event: key_disable(textPad, event))
    textPad.bind("<Insert>", lambda event: key_disable(textPad, event))
    textPad.bind("<Return>", lambda event: key_enter(textPad, event,queue))
    textPad.bind("<BackSpace>", lambda event: key_backspace(textPad, event,queue))
    textPad.bind("<Key>", lambda event: key_press(textPad, event))
    textPad.bind("<KeyRelease>", lambda event: key(textPad, event,queue))


    textPad.pack()
    root.mainloop()

if __name__ == "__main__":
    run_gui([],"test.txt")