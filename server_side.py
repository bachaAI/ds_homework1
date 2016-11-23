from socket import AF_INET, SOCK_STREAM, socket
from socket import error as SocketErrors
from text_file import File
from class_queue import Queue
import sys
from threading import Thread



class Server:
    def __init__(self):
        self.host = '127.0.0.1'       # ip server's address
        self.port1 = 50001    # server's port
        self.port2 = 50002
        self.port3 = 50003
        self.backlog = 0     # at most server will work with three clients
        self.size = 1024     # max message size
        self.server = None
        self.threads = []
        #text = File()


    def file_syncronization(self, triple, text, client_socket, queue, port):

        if port == self.port1:
            queue.add_user1(triple)
            i,j,elem = text.parse_triple(triple)
            text.change(i,j,elem)
            text.show()
            #print triple

        if port == self.port2:
            queue.add_user2(triple)
            i,j,elem = text.parse_triple(triple)
            text.change(i,j,elem)
            text.show()

        if port == self.port3:
            queue.add_user3(triple)
            i,j,elem = text.parse_triple(triple)
            text.change(i,j,elem)
            text.show()

    def edit_function(self, text, client_socket, port):
        while True:
            queue = Queue()
            triple = client_socket.recv(1024)
            print triple
            while triple != 'Nothing':
                print triple
                self.file_syncronization(triple, text, client_socket, queue, port)
                triple = client_socket.recv(1024)
            if port == self.port1:
                while queue.q_user2.__len__() != 0:
                    client_socket.send(queue.take2())
                if queue.q_user2.__len__() == 0:
                    client_socket.send('Nothing')
                while queue.q_user3.__len__() != 0:
                    client_socket.send(queue.take3())
                if queue.q_user3.__len__() == 0:
                    client_socket.send('Nothing')
            if port == self.port1:
                while queue.q_user1.__len__() != 0:
                    client_socket.send(queue.take1())
                if queue.q_user1.__len__() == 0:
                    client_socket.send('Nothing')
                while queue.q_user3.__len__() != 0:
                    client_socket.send(queue.take3())
                if queue.q_user3.__len__() == 0:
                    client_socket.send('Nothing')
            if port == self.port1:
                while queue.q_user1.__len__() != 0:
                    client_socket.send(queue.take1())
                if queue.q_user1.__len__() == 0:
                    client_socket.send('Nothing')
                while queue.q_user2.__len__() != 0:
                    client_socket.send(queue.take2())
                if queue.q_user2.__len__() == 0:
                    client_socket.send('Nothing')


    def open_socket(self, port):
        try:
            print port
            self.server = socket(AF_INET, SOCK_STREAM)
            self.server.bind((self.host, port))
            self.server.listen(self.backlog)
            print 'Lets Go!'
            while True:
                client_socket, client_addr = self.server.accept()
                print 'New Client has been connected!'
                #client_socket.send('Please enter 1 if you want to Upload New File.\n'
                                  # 'Please enter 2 if you want to Create New File.\n'
                                   #'Please enter 3 if you want to Download Existed File.\n')

                print 'BOOM!'
                decision = client_socket.recv(1024)
                print decision
                if decision == '1':
                    filename = client_socket.recv(1024)
                    password = client_socket.recv(1024)
                    with open(str('FileNew.txt'), 'wb') as f:
                        print 'file %s opened' % str('FileNew.txt')
                        data = client_socket.recv(1024)
                        while data:
                            print('receiving data...')
                            print('data:', (data))
                            f.write(data)
                            data = client_socket.recv(1024)
                            if data[-4:] == 'STOP':
                                print data
                                break
                    f.close()
                    client_socket.send('OKEY!')
                    print 'Ooooops!'
                    text = File()
                    text.download_from_txt('FileNew.txt')
                    self.edit_function(text, client_socket, port)




                elif decision == '2':
                    client_socket.recv(filename)
                    client_socket.recv(password)
                    text = File()
                    self.edit_function(text, client_socket, port)


                elif decision == '3':
                    client_socket.recv(filename)
                    client_socket.recv(password)
                    text = open(filename, 'rb')
                    #if password == password_file:
                    l = text.read(1024)
                    while (l):
                           client_socket.send(l)
                           print('Sent ', repr(l))
                           l = f.read(1024)
                    self.edit_function(text, client_socket, port)

                else:
                    client_socket.send('You have made wrong decision. Good luck!\n')

        except SocketErrors, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)



if __name__ == '__main__':
    s = Server()
    thread1 = Thread(target=s.open_socket, args=(s.port1,))
    thread2 = Thread(target=s.open_socket, args=(s.port2,))
    thread3 = Thread(target=s.open_socket, args=(s.port3,))
    s.threads.append(thread1)
    s.threads.append(thread2)
    s.threads.append(thread3)
    for t in s.threads:
        t.start()
    for t in s.threads:
        t.join()
    print 'Servers are dead!'



    #############################################
    # ||                                     || #
    # ||          HERE WILL BE BLOCK,        || #
    # ||    WHICH DESCRIBES HOW THE SERVER   || #
    # ||      COMMUNICATE WITH THE CLIENT    || #
    # ||                                     || #
    #############################################