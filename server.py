import socket
from email.utils import formatdate

ADDR = ('127.0.0.1', 8001)

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
    socket.IPPROTO_IP
)

server.bind(ADDR)
server.listen(1)


def response_ok():
    now = formatdate(usegmt=True)
    body = "Hello World"
    return ('HTTP/1.1 200 OK\r\n'
        'Date: {}\r\nContent-Type: text/plain\r\nContent-Length: {}\r\n'
        'Connection: close\r\n\r\n{}'.format(now, len(body), body))


def response_error():
    now = formatdate(usegmt=True)
    body = "<html><body>\nThe server encountered an unexpected internal \
    error.</body></html>"
    return ('HTTP 1.1 500 Internal Server Error'
        '\r\nDate:{}\r\nContent-Type: text/html\r\nContent-Length: {}\r\n'
        'Connection: close\r\n\r\n{}'.format(now, len(body), body))


while True:
    try:
        conn, addr = server.accept()
        msg = ""
        while True:
            msg = msg + conn.recv(16)
            conn.sendall(response_ok())
            if len(msg) < 16:
                conn.close()
                break
        print msg
    except KeyboardInterrupt:
        break
