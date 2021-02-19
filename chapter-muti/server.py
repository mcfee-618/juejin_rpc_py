import socket
import threading
import os
import select
from protocol import *


class Server:

    def __init__(self, sock):
        self.sock = sock
        self.r_fds = [sock]
        self.w_fds = []

    def loop(self):
        while True:
            readable_fds, writable_fds, _, = select.select(self.r_fds, self.w_fds, [])
            for readable_fd in readable_fds:
                self.handle_read(readable_fd)
            for writable_fd in writable_fds:
                self.handle_write(writable_fd)

    def handle_read(self, readable_fd):
        if readable_fd is self.sock:
            conn, addr = sock.accept()
            conn.setblocking(False)
            self.r_fds.append(conn)
        else:
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


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", 8080))
    sock.listen(10)
    sock.setblocking(False)
    server = Server(sock)
    server.loop()
