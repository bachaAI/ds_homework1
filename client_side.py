'''
from socket import AF_INET, SOCK_STREAM, socket
import threading
from server_side import Server

1


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



if __name__ == '__main__':
    print 'Application started'

    s = socket(AF_INET, SOCK_STREAM)
    print 'TCP Socket created'

    # No binding needed for client, OS will bind the socket automatically
    # when connect is issued

    server_address = ('127.0.0.1',7777)

    # Connecting ...
    try:
        s.connect(server_address)

        print 'Socket connected to %s:%d' % s.getpeername()
        print 'Local end-point is  bound to %s:%d' % s.getsockname()


        file_name = raw_input('Please, enter a name of the file to upload:')
        f = open(file_name,'rb')
        l = f.read(1024)
        while (l):
            s.send(l)
            print('Sent ', repr(l))
            l = f.read(1024)
        print 'Done sending'

    except SocketError:
        print " Communication ERROR "

    finally:
        f.close()
        # Wait for user input before terminating application
        raw_input('Press Enter to terminate ...')
        s.close()
        print 'Terminating ...'
