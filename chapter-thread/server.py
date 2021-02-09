import socket
import threading
from protocol import *


def handle_conn(sock, addr):
    while True:
        try:
            print("1111")
            decoder(sock)
            print("2222")
            encoder(sock, "pong")
            print("pong")
        except ConnectionAbortedError as e1:
            break
    sock.close()  ##不然可能一直处于半断开的状态



def loop(sock):
    while True:
        conn, addr = sock.accept()  # 接收连接
        thread = threading.Thread(target=handle_conn, args=(conn, addr))
        thread.run()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 8080))
    s.listen(10)
    loop(s)
