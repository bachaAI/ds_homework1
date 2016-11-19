from socket import AF_INET, SOCK_STREAM, socket
from socket import error as SocketErrors
from text_file import File
from os import getpid
import select
import sys
from threading import Thread



class Server:
    def __init__(self):
        self.host = ''       # ip server's address
        self.port = 50000    # server's port
        self.backlog = 2     # at most server will work with three clients
        self.size = 1024     # max message size
        self.server = None
        self.threads = []
        text = File()


    def file_syncronization(self, triple, text, client_socket, threads,queue):
        client_socket.recv(triple)
        for elem in threads:
            if elem.getName() == 'Thread-1':
                queue.add_user1(triple)
                text.change(triple)

            if elem.getName() == 'Thread-2':
                queue.add_user2(triple)
                text.change(triple)

            if elem.getName() == 'Thread-3':
                queue.add_user3(triple)
                text.change(triple)

    def edit_function(self,text, client_socket,triple):
        if client_socket.recv(triple)
            self.file_syncronization(triple, text)

    def open_socket(self):
        try:
            self.server = socket(AF_INET, SOCK_STREAM)
            self.server.bind((self.host, self.port))
            self.server.listen(self.backlog)
            while True:
                client_socket, client_addr = self.server.accept()
                client_socket.send('Please enter 1 if you want to Upload New File.\n'
                                   'Please enter 2 if you want to Create New File.\n'
                                   'Please enter 3 if you want to Download Existed File.\n')
                decision = ''
                filename = ''
                password = ''
                client_socket.recv(decision)
                if decision == '1':
                    client_socket.recv(filename)
                    client_socket.recv(password)
                    with open(str(filename), 'wb') as f:
                        print 'file %s opened' % str(filename)
                        while True:
                            data = client_socket.recv(1024)
                            if not data:
                                break
                            print('receiving data...')
                            print('data:', (data))
                            # write data to a file
                            f.write(data)
                    text = open(filename, 'rb')
                    self.edit_function(text)



                elif decision == '2':
                    client_socket.recv(filename)
                    client_socket.recv(password)
                    text = open(filename, 'rb')
                    self.edit_function(text)


                elif decision == '3':
                    client_socket.recv(filename)
                    client_socket.recv(password)
                    text = open(filename, 'rb')
                    if password == password_file:
                       l = text.read(1024)
                       while (l):
                           client_socket.send(l)
                           print('Sent ', repr(l))
                           l = f.read(1024)
                       self.edit_function(text)

                else:
                    client_socket.send('You have made wrong decision. Good luck!\n')



        except SocketErrors, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)



    def run(self):
        self.open_socket()
        input = [self.server]
        running = 1
        while running:
            in_ready, out_ready, except_ready = select.select(input, [], [])

            # in_ready: wait until ready for reading
            # out_ready: wait until ready for writing
            # except_ready: wait for an “exceptional condition”

            for s in in_ready:

                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)
                    for c in self.threads:
                        c.join()
                elif SocketErrors:
                    running = 0
                    self.server.close()



    def open_socket_edition(self):
        try:
            self.server = socket(AF_INET, SOCK_STREAM)
            self.server.bind((self.host, self.port))
            while True:
               self.server.listen(self.backlog)
               thread = Thread(target=self.open_socket(), args=)
               thread.start()
               self.threads.append(thread)
            for t in self.threads:
                t.join()

if __name__ == '__main__':
    s = Server()
    s.run()
    print 'Server started!'


    #############################################
    # ||                                     || #
    # ||          HERE WILL BE BLOCK,        || #
    # ||    WHICH DESCRIBES HOW THE SERVER   || #
    # ||      COMMUNICATE WITH THE CLIENT    || #
    # ||                                     || #
    #############################################