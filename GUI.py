import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox
import time
from threading import Thread
import text_file
from socket import AF_INET, SOCK_STREAM, socket


disableFlag = False
shiftFlag = False

class GUI:
    queue = []
    client_socket = None
    text = None

    #root = Tkinter.Tk(className=" Collaborative Text Editor")
    #textPad = ScrolledText(root, width=100, height=80)

    def __init__(self, file, socket):
        self.queue = []
        self.client_socket = socket
        self.text = text_file.File()
        self.text.download_from_txt(file)
        root = Tkinter.Tk(className=" Collaborative Text Editor")
        self.textPad = ScrolledText(root, width=100, height=80)
        menu = Menu(root)
        root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Save", command=self.save_command)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_command)
        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.about_command)
        # Insert given text
        if file:
            f = open(file, 'r')
            self.textPad.insert(END, f.read())
        # Keybord bindings to virtual events
        self.textPad.bind("<Button-1>", self.mouse_button)
        self.textPad.bind("<Control-v>", self.key_disable)
        self.textPad.bind("<Control-c>", self.key_disable)
        self.textPad.bind("<Shift_L>", self.key_shift)
        self.textPad.bind("<Delete>", self.key_disable)
        self.textPad.bind("<Insert>", self.key_disable)
        self.textPad.bind("<Return>", self.key_enter)
        self.textPad.bind("<BackSpace>",self.key_backspace)
        self.textPad.bind("<Key>", self.key_press)
        self.textPad.bind("<KeyRelease>", self.key)
        self.textPad.pack()
        root.bind('<<send_recv>>', self.send_receive)

        def heartbeat():
            while True:
                time.sleep(2)
                root.event_generate('<<send_recv>>', when='tail')

        th = Thread(None, heartbeat)
        th.setDaemon(True)
        th.start()

        root.mainloop()

    def send_receive(self, event):
        print "Good"
        if self.queue:
            self.client_socket.send(self.queue.pop(0))
        else:
            self.client_socket.send('Ooops')
            print "KuKu"
        triple = self.client_socket.recv(1024)
        print triple + "new"
        while triple != '':
            insert = self.text.parse_triple(triple)
            self.text.change(insert[0], insert[1], insert[2])
            self.textPad.insert("%d.%d" % (insert[0], insert[1]), insert[2])
            triple = self.client_socket.recv(1024)

    def save_command(self):
        file = tkFileDialog.asksaveasfile(mode='w')
        if file != None:
            # slice off the last character from get, as an extra return is added
            data = self.textPad.get('1.0', END + '-1c')
            file.write(data)
            file.close()
    def exit_command(self, root):
        if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
            root.destroy()
    def about_command(self):
        label = tkMessageBox.showinfo("About", "Collaborative text editor \n Developed by Bachinskiy A., Shapaval R., \
                                        Shuchorukov M., Tkachuk D. using Tk.tkinter.\n No rights left to reserve :)")

    #Here come all button handlers

    def key_enter(self, event):
        s = self.textPad.index(INSERT)
        self.add_to_queue(s,"ent")


    def key_backspace(self, event):
        s = self.textPad.index(INSERT)
        self.add_to_queue(s,"bs")

    def key_disable(self, event):
        self.textPad.config(state=DISABLED)
        global disableFlag
        disableFlag = True

    def mouse_button(self, event):
        self.textPad.config(state=NORMAL)

    def key_shift(self, event):
        global shiftFlag
        shiftFlag = True

    def key(self, event):
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
                s = self.textPad.index(INSERT)
                self.add_to_queue(s)
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
                self.textPad.config(state=NORMAL)
                s = self.textPad.index(INSERT)
                self.add_to_queue(s)


    def key_press(self, event):
        self.textPad.config(state=DISABLED)
        time.sleep(0.2)
        self.textPad.config(state=NORMAL)

    def add_to_queue(self, s, key=""):
        point_index = s.index(".")
        index1 = int(s[:point_index])
        index2 = int(s[point_index + 1:])
        out = self.textPad.get("%d.%d" % (index1, index2 - 1), "%d.%d" % (index1, index2))
        if key:
            if key == "ent":
                self.queue.append("%d,%d,%s" % (index1-1, index2, key))
            if key == "bs":
                self.queue.append("%d,%d,%s" % (index1-1, index2-1, key))
        else:
            self.queue.append("%d,%d,%s" % (index1-1, index2-1, out))
        print self.queue




if __name__ == "__main__":
    gui = GUI("test.txt",50001  )
