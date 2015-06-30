import socket
from email.utils import formatdate

CRLF = '\r\n'


def response_ok():
    response = []
    now = formatdate(usegmt=True)
    body = "Hello World, I need to travel."
    response.append('HTTP/1.1 200 OK')
    response.append('Date: {}'.format(now))
    response.append('Content-Type: text/plain')
    response.append('Content-Length: {}'.format(len(body)))
    response.append('Connection: close')
    response.append('')
    response.append(body)
    return CRLF.join(response)


def response_error():
    response = []
    now = formatdate(usegmt=True)
    body = ('<html><body>\nThe server encountered an unexpected internal '
            'error.</body></html>')
    response.append('HTTP 1.1 500 Internal Server Error')
    response.append('Date: {}'.format(now))
    response.append('Content-Type: text/html')
    response.append('Content-Length: {}'.format(len(body)))
    response.append('Connection: close')
    response.append('')
    response.append(body)
    return CRLF.join(response)

if __name__ == '__main__':
    ADDR = ('127.0.0.1', 8001)

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP
    )

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(ADDR)
    server.listen(1)
    while True:
        try:
            conn, addr = server.accept()
            message_in = ""
            while True:
                msg = conn.recv(16)
                message_in += msg
                if len(msg) < 16:
                    break
            conn.sendall(response_ok())
            conn.close()
            print message_in
        except KeyboardInterrupt:
            break
