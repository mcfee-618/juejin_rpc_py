import socket
import threading
import os
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
        conn, addr = sock.accept()  # 接收连接,只有一个进程可以抢到
        print(addr,os.getpid())
        thread = threading.Thread(target=handle_conn, args=(conn, addr))
        thread.run()


def prefork(n):
    for i in range(n):
        pid = os.fork()
        if pid < 0:  # fork error
            return
        if pid > 0:  # parent process
            continue
        if pid == 0:
            break  # child process


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("localhost", 8080))
    s.listen(10)
    prefork(8)
    loop(s)
