import socket
from email.utils import formatdate
import os
import mimetypes

CRLF = '\r\n'
ROOT = os.path.join(os.getcwd(), 'webroot')


def create_server():
    addr = ('127.0.0.1', 8001)

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP
    )

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(addr)
    server.listen(1)
    return server


def respond():
    server = create_server()
    while True:
        try:
            conn, addr = server.accept()
            message_in = ""
            while True:
                msg = conn.recv(16)
                message_in += msg
                if len(msg) < 16:
                    break
            try:
                uri = parse_request(message_in)
            except (NotImplementedError, ValueError, AttributeError) as e:
                conn.sendall(response_error(e.message))
            else:
                # send parsed request to resolve uri
                try:
                    body, resource_type = resolve_uri(uri)
                except LookupError as e:
                    conn.sendall(response_error(e.message))
                conn.sendall(response_ok(body, resource_type))
            conn.close()
        except KeyboardInterrupt:
            break


def response_ok(body, resource_type):
    response = []
    now = formatdate(usegmt=True)
    response.append('HTTP/1.1 200 OK')
    response.append('Date: {}'.format(now))
    response.append('Content-Type: {}'.format(resource_type))
    response.append('Content-Length: {}'.format(len(body)))
    response.append('Connection: close')
    response.append('')
    response.append(body)
    return CRLF.join(response)


def response_error(message):
    codes = {'405': 'Method Not Allowed',
             '505': 'HTTP Version Not Supported',
             '400': 'Bad Request',
             '404': 'Not Found'
             }
    response = []
    now = formatdate(usegmt=True)
    body = (codes[message])
    response.append('HTTP 1.1 {} {}'.format(message, codes[message]))
    response.append('Date: {}'.format(now))
    response.append('Content-Type: text/plain')
    response.append('Content-Length: {}'.format(len(body)))
    response.append('Connection: close')
    response.append('')
    response.append(body)
    return CRLF.join(response)


def parse_request(request):
    header, body = request.split(CRLF*2, 1)
    header_lines = header.split(CRLF)
    host = False
    if 'GET' not in header_lines[0]:
        raise NotImplementedError('405')
    elif 'HTTP/1.1' not in header_lines[0]:
        raise ValueError('505')
    for line in header_lines[1:]:
        if 'Host:' in line:
            host = True
    if not host:
        raise AttributeError('400')
    request_line = header_lines[0].split()
    return request_line[1]


def resolve_uri(uri):
    body = ''
    resource_type = ''
    if os.path.isdir(ROOT + uri):
        body = '<!DOCTYPE html><html><body><ul>'
        for file_ in os.listdir(ROOT + uri):
            body += '<li>' + file_ + '</li>'
        body += '</ul></body></html>'
        resource_type = 'text/html'
    elif os.path.isfile(ROOT + uri):
        with open((ROOT + uri), 'rb') as file_:
            body = file_.read()
        resource_type, encoding = mimetypes.guess_type(uri)
    else:
        raise LookupError('404')
    return (body, resource_type)


if __name__ == '__main__':
    respond()
