from socket import AF_INET, SOCK_STREAM, socket
from socket import error as SocketErrors
from client_side import Client
from os import getpid
import select
import sys
import threading



class Server:
    def __init__(self):
        self.host = ''       # ip server's address
        self.port = 50000    # server's port
        self.backlog = 2     # at most server will work with three clients
        self.size = 1024     # max message size
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            self.server = socket(AF_INET, SOCK_STREAM)
            self.server.bind((self.host, self.port))
            self.server.listen(self.backlog)
        except SocketErrors, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)



    def run(self):
        self.open_socket()
        input = [self.server, sys.stdin]
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

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

                    # close all threads

        self.server.close()
        for c in self.threads:
            c.join()


     def file_syncronization(self):



    #############################################
    # ||                                     || #
    # ||          HERE WILL BE BLOCK,        || #
    # ||    WHICH DESCRIBES HOW THE SERVER   || #
    # ||      COMMUNICATE WITH THE CLIENT    || #
    # ||                                     || #
    #############################################