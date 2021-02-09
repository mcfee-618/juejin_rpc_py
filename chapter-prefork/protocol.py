import struct


def encoder(sock, message):
    message_length = len(message)
    sock.sendall("rpc".encode("utf-8"))  ## prefix
    message_length_bytes = struct.pack("I", message_length)  ## length
    sock.sendall(message_length_bytes)
    sock.sendall(message.encode("utf-8"))  ## data


def decoder(sock):
    prefix = sock.recv(3)
    if len(prefix) == 0:
        print("结束了")
        ## 如果recv函数在等待协议接收数据时网络中断了，那么它返回0
        raise ConnectionAbortedError()
    if str(prefix, encoding="utf-8") != "rpc":
        raise Exception("protocol error")
    length_prefix = sock.recv(4)
    message_length, = struct.unpack("I", length_prefix)
    message = sock.recv(message_length)
    return str(message, encoding="utf-8")
