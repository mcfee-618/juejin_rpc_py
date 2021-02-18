import socket
import threading
import os
import select
from protocol import *
from util import *


class Master:

    def __init__(self, sock):
        self.sock = sock
        self.pids = []

    def loop(self):
        conn, addr = self.sock.accept()
        conn.setblocking(False)
        ut

    def prefork(self, num):
        pr, pw = socket.socketpair()
        pid = os.fork()
        if pid:
            pr.close()
        else:
            self.sock.close()
            pw.close()


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", 8080))
    sock.listen(10)
    sock.setblocking(False)
    server = Server(sock)
    server.prefork(100)
