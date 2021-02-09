import struct


def encoder(sock, message):
    message_length = len(message)
    byte_array = bytes()
    byte_array += "rpc".encode("utf-8")
    byte_array += struct.pack("I", message_length)
    byte_array += message.encode("utf-8")
    sock.sendall(byte_array)


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
