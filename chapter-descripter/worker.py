import select
import threading
from protocol import *
from util import *


class Worker:

    def __init__(self, sock) -> None:
        self.sock = sock
        self.r_fds = []
        self.w_fds = []

    def recv_fd(self):
        while True:
            fd = recv_sock(self.sock)
            self.r_fds.append(fd)

    def loop(self):
        thread = threading.Thread(target=self.recv_fd)
        thread.start()
        while True:
            readable_fds, writable_fds, _, = select.select(self.r_fds, self.w_fds, [],1)
            for readable_fd in readable_fds:
                self.handle_read(readable_fd)
            for writable_fd in writable_fds:
                self.handle_write(writable_fd)

    def handle_read(self, readable_fd):
        try:
            message = decoder(readable_fd)
            if message == "ping":
                self.w_fds.append(readable_fd)
        except Exception as e:
            readable_fd.close()
            self.r_fds.remove(readable_fd)

    def handle_write(self, writeable_fd):
        encoder(writeable_fd, "pong")
        self.w_fds.remove(writeable_fd)
