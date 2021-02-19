import socket, array, struct


def send_sock(pw, sock):
    msg = [b'x']
    # 辅助数据，携带描述符
    ancdata = [(
        socket.SOL_SOCKET,
        socket.SCM_RIGHTS,
        struct.pack('i', sock.fileno()))]
    pw.sendmsg(msg, ancdata)


def recv_sock(pr):
    ancsize = socket.CMSG_LEN(struct.calcsize('i'))
    msg, ancdata, flags, addr = pr.recvmsg(1,  ancsize)
    cmsg_level, cmsg_type, cmsg_data = ancdata[0]
    fd = struct.unpack('i', cmsg_data)[0]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, fileno=fd)
    return sock
