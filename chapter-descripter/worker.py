import select
from protocol import *

class Worker:
    
    def __init__(self) -> None:
        self.r_fds = []
        self.w_fds = []
    
    def loop(self):
        while True:
            readable_fds, writable_fds, _, = select.select(self.r_fds, self.w_fds, [])
            for readable_fd in readable_fds:
                self.handle_read(readable_fd)
            for writable_fd in writable_fds:
                self.handle_write(writable_fd)

    def handle_read(self, readable_fd):
            try:
                message = decoder(readable_fd)
                print(message)
                if message == "ping":
                    self.w_fds.append(readable_fd)
            except Exception as e:
                readable_fd.close()
                self.r_fds.remove(readable_fd)

    def handle_write(self, writeable_fd):
        encoder(writeable_fd, "pong")
        self.w_fds.remove(writeable_fd)
