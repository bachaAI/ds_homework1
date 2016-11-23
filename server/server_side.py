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

    def file_syncronization(self, triple, text, client_socket, queue, port, filename):

        if port == self.port1:
            queue.add_user1(triple)
            i,j,elem = text.parse_triple(triple)
            text.change(i,j,elem)
            text.upload_to_txt(filename)

        if port == self.port2:
            queue.add_user2(triple)
            i,j,elem = text.parse_triple(triple)
            text.change(i,j,elem)
            text.upload_to_txt('FileNew.txt')

        if port == self.port3:
            queue.add_user3(triple)
            i,j,elem = text.parse_triple(triple)
            text.change(i,j,elem)
            text.upload_to_txt('FileNew.txt')

    def edit_function(self, text, client_socket, port,queue, filename):
        while True:
            triple = client_socket.recv(1024)
            if triple != 'Nothing':
                self.file_syncronization(triple, text, client_socket, queue, port,filename)
            if port == self.port1:
                print queue.q_user2.__len__()
                while queue.q_user2.__len__() != 0:
                    client_socket.send(queue.take2())
                while queue.q_user3.__len__() != 0:
                    client_socket.send(queue.take3())
                if queue.q_user2.__len__() == 0:
                    client_socket.send('Nothing')
                if queue.q_user3.__len__() == 0:
                    client_socket.send('Nothing')

            if port == self.port2:
                print queue.q_user2.__len__()
                while queue.q_user1.__len__() != 0:
                    client_socket.send(queue.take1())
                while queue.q_user3.__len__() != 0:
                    client_socket.send(queue.take3())
                if queue.q_user1.__len__() == 0:
                    client_socket.send('Nothing')
                if queue.q_user3.__len__() == 0:
                    client_socket.send('Nothing')

            if port == self.port3:
                while queue.q_user1.__len__() != 0:
                    client_socket.send(queue.take1())
                while queue.q_user2.__len__() != 0:
                    client_socket.send(queue.take2())
                if queue.q_user1.__len__() == 0:
                    client_socket.send('Nothing')
                if queue.q_user2.__len__() == 0:
                    client_socket.send('Nothing')

    def open_socket(self, port,text,queue):
        try:
            print port
            self.server = socket(AF_INET, SOCK_STREAM)
            self.server.bind((self.host, port))
            self.server.listen(self.backlog)
            print 'Lets Go!'
            while True:
                client_socket, client_addr = self.server.accept()
                print 'New Client has been connected!'
                decision = client_socket.recv(1024)
                if decision == '1':
                    filename = client_socket.recv(1024)
                    password = client_socket.recv(1024)
                    with open(str(filename), 'wb') as f:
                        print 'file %s opened' % str(filename)
                        data = client_socket.recv(1024)
                        while data:
                            print('receiving data...')
                            f.write(data)
                            data = client_socket.recv(1024)
                            if data[-4:] == 'STOP':
                                break
                    f.close()
                    client_socket.send('Done receiving!')
                    text.download_from_txt(filename)
                    #text.download_from_txt(filename)
                    self.edit_function(text, client_socket, port,queue, filename)
                elif decision == '2':
                    filename = client_socket.recv(1024)
                    password = client_socket.recv(1024)
                    text.download_from_txt(filename)
                    self.edit_function(text, client_socket, port,queue)


                elif decision == '3':
                    filename = client_socket.recv(1024)
                    password = client_socket.recv(1024)
                    f = open(filename, 'rb')
                    while True:
                        l = f.read(1024)
                        client_socket.send(l)
                        #print('Sent ', repr(l))
                        if not l:
                            client_socket.send('STOP')
                            break
                    f.close()
                    text.download_from_txt(filename)
                    self.edit_function(text, client_socket, port, queue, filename)

                else:
                    client_socket.send('You have made wrong decision. Good luck!\n')

        except SocketErrors, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)



if __name__ == '__main__':
    s = Server()
    queue = Queue()
    text = File()
    thread1 = Thread(target=s.open_socket, args=(s.port1,text,queue))
    thread2 = Thread(target=s.open_socket, args=(s.port2,text,queue))
    thread3 = Thread(target=s.open_socket, args=(s.port3,text,queue))
    s.threads.append(thread1)
    s.threads.append(thread2)
    s.threads.append(thread3)
    for t in s.threads:
        t.start()
        print 'Servers are born!'
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