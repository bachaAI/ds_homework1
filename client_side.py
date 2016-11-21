'''
from socket import AF_INET, SOCK_STREAM, socket
import threading
from server_side import Server



class Client(threading.Thread):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.socket = socket
        self.size = 1024

    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            if data:
                self.client.send(data)
            else:
                self.client.close()
                running = 0

if __name__ == "__main__":
    s = Server()
    s.run()

'''





from socket import AF_INET, SOCK_STREAM, socket
from socket import error as SocketError

import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox


SOCKETS = [50001, 50002, 50003]

if __name__ == '__main__':

    print 'Application started'

    """
    print 'Application started'
    # ---------- Starting User dialog ----------
    exit0 = 0
    while exit0 == 0:
        print 'Press n to create new file or d to download existing'
        ans = raw_input()
        if ans == 'n':
            exit1 = 0
            while exit1 == 0:
                f_name = raw_input('Enter file name: ')

                #request to the server for creating new file if curent name is free
                #server ansver
                s_ans = 'ok'
                if s_ans =='ok':
                    #start gui
                    root = Tkinter.Tk(className=" Collaborative Text Editor")
                    textPad = ScrolledText(root, width=100, height=80)
                    textPad.pack()
                    root.mainloop()
                    exit1 = 1
                    print 'ok'
                elif s_ans == 'no':
                    print 'Choose another name'
                else:
                    print 'Something wrong, try again!'
            exit0 = 1
        elif ans == 'd':
            exit2 = 0
            while exit2 == 0:
                print 'Enter file name:'
                f_name = raw_input()
                #request to the server if current file exist
                s_ans = ''
                if s_ans == 'ok':
                    #response with file
                    #gui.set(resp_file)
                    print 'file is ok'
                    exit2 = 1
                elif s_ans == 'no':
                    print 'There is no file with this name on server, try again!'
            exit0 = 1
        else:
            print 'Wront choice, try again!'

    #--------------------------------------
    """
    s = socket(AF_INET, SOCK_STREAM)
    print 'TCP Socket created'

    # No binding needed for client, OS will bind the socket automatically
    # when connect is issued

    server_address = ('172.31.132.48', 50001)

    # Connecting ...
    '''

    for elem in SOCKETS:
        server_address = ('172.31.132.48', elem)
        #server_address = ('127.0.1.1', elem)
        if s.connect(server_address):
            break
        else:
            print "Server is busy"
    '''
    try:
        s.connect(server_address)
        decision = ''
        filename = ''
        password = ''

        print 'Socket connected to %s:%d' % s.getpeername()
        print 'Local end-point is  bound to %s:%d' % s.getsockname()
        decision=raw_input('Waiting for decision...')
        s.send(decision)
        if decision == '1':
            filename=raw_input('Enter file name: ')
            password=raw_input('Set password: ')
            s.send(filename)
            s.send(password)
            f = open(filename, 'rb')
            l = f.read(1024)
            while (l):
                s.send(l)
                print('Sent ', repr(l))
                l = f.read(1024)
            print 'Done sending'
        elif decision == '2':
            print '2'
        elif decision=='3':
            print '3'
        else:
            print 'Wrong input.'


        #file_name = raw_input('Please, enter a name of the file to upload:')


    except SocketError:
        print " Communication ERROR "

    finally:
        #f.close()
        # Wait for user input before terminating application
        raw_input('Press Enter to terminate ...')
        s.close()
        print 'Terminating ...'
