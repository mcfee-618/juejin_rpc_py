import socket,time
from protocol import *


def rpc(sock, message):
    if message == "ping":
        encoder(sock, message)
        response = decoder(sock)
        if response == "pong":
            return
        else:
            raise Exception("not pong")
    else:
        raise Exception("only support ping")


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8080))
    for i in range(10):
        time.sleep(50)
        rpc(s, "ping")
    s.close()
