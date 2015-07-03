# -*- coding:UTF-8 -*-
# from __future__ import unicode_literals
from server import response_error, response_ok, respond
from email.utils import formatdate
import time

import pytest
import socket


@pytest.yield_fixture
def server_process(scope='session'):
    from multiprocessing import Process
    process = Process(target=respond)
    process.daemon = True
    process.start()
    time.sleep(.01)
    yield process


@pytest.fixture
def connection(server_process):
    addr = ('127.0.0.1', 8001)

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP
    )

    client.connect(addr)
    return client


# @pytest.fixture
# def request_builder(body, ctype, )


@pytest.fixture
def okresponse():
    now = formatdate(usegmt=True)
    body = "Thank you for the appropriate request."
    return ('HTTP/1.1 200 OK\r\n'
            'Date: {}\r\n'
            'Content-Type: text/plain\r\n'
            'Content-Length: {}\r\n'
            'Connection: close\r\n\r\n{}'.format(now, len(body), body))


@pytest.fixture
def errorresponse():
    now = formatdate(usegmt=True)
    body = 'Method Not Allowed'
    return ('HTTP 1.1 405 Method Not Allowed\r\n'
            'Date: {}\r\n'
            'Content-Type: text/plain\r\n'
            'Content-Length: {}\r\n'
            'Connection: close\r\n\r\n{}'.format(now, len(body), body)
    )


def test_response_ok(okresponse):
    body = 'this is a response'
    ctype = 'text/plain'
    response = response_ok(body, ctype)
    headers, rbody = response.split('\r\n\r\n')
    assert rbody == body
    lines = headers.split('\r\n')
    assert lines[0] == 'HTTP/1.1 200 OK'
    typefound = False
    for line in lines:
        if 'Content-Type: text/plain' in line:
            typefound = True
            break
    assert typefound


def test_response_error(errorresponse):
    assert response_error('405') == errorresponse


def test_http_response(server_process, connection, okresponse):
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


def test_error_response(server_process, connection, errorresponse):
    msg = "POST path/to/stuff HTTP/1.1\r\nHost: www.codefellows.org\r\n\r\n"
    connection.sendall(msg)
    connection.shutdown(socket.SHUT_WR)
    message_in = ''
    while True:
        part = connection.recv(16)
        message_in += part
        if len(part) < 16:
            break
    connection.close()
    assert message_in == errorresponse
