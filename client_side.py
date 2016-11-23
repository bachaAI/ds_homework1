from socket import AF_INET, SOCK_STREAM, socket, SHUT_WR
from socket import error as SocketError
import GUI

SOCKETS = [50001, 50002, 50003]

if __name__ == '__main__':

    print 'Application started'

    s = socket(AF_INET, SOCK_STREAM)
    print 'TCP Socket created'

    server_address = ('127.0.0.1', 50001)

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
        print 'Please enter 1 if you want to upload your file.\n Please enter 2 if you want to create New File.\n Please enter 3 if you want to open existing file.\n'
        decision=raw_input()
        s.send(decision)
        if decision == '1':
            filename=raw_input('Enter file name: ')
            s.send(filename)
            password=raw_input('Please, a password for a file: ')
            s.send(password)
            f = open(filename, 'rb')
            while True:
                l = f.read(1024)
                s.send(l)
                if not l:
                    s.send('STOP')
                    break
            print 'Done sending'
            result = s.recv(1024)
            client_GUI = GUI.GUI(filename,s)

        elif decision == '2':
            filename = raw_input('Please, enter a name of the file to create: ')
            s.send(filename)
            password = raw_input('Please, set a password for a file:')
            s.send(password)
            client_GUI = GUI.GUI(filename,s)

        elif decision == '3':
            filename = raw_input('Please, enter a name of the file you want to open: ')
            s.send(filename)
            password = raw_input('Please, a password for a file: ')
            s.send(password)
            filename1 = 'randomfile.txt'
            with open(str(filename1), 'wb') as f:
                data = s.recv(1024)
                while data:
                    print('receiving data...')
                    #print('data:', (data))
                    if data[-4:] == 'STOP':
                        f.write(data[:-4])
                        break
                    else:
                        f.write(data)
                    data = s.recv(1024)
            f.close()
            client_GUI = GUI.GUI(filename1,s)

        else:
            print 'Wrong input.'

    except SocketError:
        print " Communication ERROR "

    finally:
        raw_input('Press Enter to terminate ...')
        s.close()
        print 'Terminating ...'
