# -*- coding:UTF-8 -*-
# from __future__ import unicode_literals
from server import response_error, response_ok
from email.utils import formatdate

import pytest
import socket


@pytest.fixture
def connection():
    addr = ('127.0.0.1', 8001)

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP
    )

    client.connect(addr)
    return client


@pytest.fixture
def okresponse():
    now = formatdate(usegmt=True)
    body = "Thank you for the appropriate request."
    return ('HTTP/1.1 200 OK\r\n'
        'Date: {}\r\nContent-Type: text/plain\r\nContent-Length: {}\r\n'
        'Connection: close\r\n\r\n{}'.format(now, len(body), body))


def test_response_ok(okresponse):
    assert response_ok() == okresponse


def test_response_error():
    now = formatdate(usegmt=True)
    body = 'Method Not Allowed'
    assert response_error('405') == ('HTTP 1.1 405 Method Not Allowed'
        '\r\nDate: {}\r\nContent-Type: text/plain\r\nContent-Length: {}\r\n'
        'Connection: close\r\n\r\n{}'.format(now, len(body), body)
    )


def test_http_response(connection, okresponse):
    msg = "GET path/to/stuff HTTP/1.1\r\nHost: www.codefellows.org\r\n\r\n"
    connection.sendall(msg)
    connection.shutdown(socket.SHUT_WR)
    message_in = ''
    while True:
        part = connection.recv(16)
        message_in += part
        if len(part) < 16:
            break
    connection.close()
    assert message_in == okresponse
