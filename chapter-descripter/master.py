import socket
import threading
import os
import select
from protocol import *
from util import *
from worker import *


class Master:

    def __init__(self, sock):
        self.sock = sock
        self.pids = []
        self.index = 0

    def loop(self):
        while True:
            conn, addr = self.sock.accept()
            conn.setblocking(False)
            if self.index >= len(self.pids):
                self.index = 0
            pid = self.pids[self.index][0]
            pw = self.pids[self.index][1]
            send_sock(pw, conn)
            self.index += 1
            conn.close()

    def prefork(self, num):
        for i in range(num):
            pr, pw = socket.socketpair()
            pid = os.fork()
            if pid:
                pr.close()
                self.pids.append((pid, pw))
            else:
                self.sock.close()
                pw.close()
                instance = Worker(pr)
                instance.loop()


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", 8080))
    sock.listen(10)
    master = Master(sock)
    master.prefork(10)
    master.loop()
