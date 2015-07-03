# -*- coding:UTF-8 -*-
# from __future__ import unicode_literals
from server import response_error, response_ok, respond
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


def process_response(response):
    headers, body = response.split('\r\n\r\n')
    lines = headers.split('\r\n')
    return lines, body


def test_response_ok():
    body = 'this is a response'
    ctype = 'text/plain'
    response = response_ok(body, ctype)
    headers, rbody = process_response(response)
    assert rbody == body
    assert headers[0] == 'HTTP/1.1 200 OK'
    typefound = False
    for header in headers:
        if 'Content-Type: text/plain' in header:
            typefound = True
            break
    assert typefound


def test_response_error():
    response = response_error('405')
    headers, body = process_response(response)
    assert headers[0] == 'HTTP/1.1 405 Method Not Allowed'


def test_response_error_unknown():
    with pytest.raises(KeyError):
        response_error('700')


def get_response(server_process, connection, msg):
    connection.sendall(msg)
    connection.shutdown(socket.SHUT_WR)
    message_in = ''
    while True:
        part = connection.recv(16)
        message_in += part
        if len(part) < 16:
            break
    connection.close()
    headers, body = process_response(message_in)
    return headers, body


def test_http_get_dir(server_process, connection):
    msg = "GET / HTTP/1.1\r\nHost: www.codefellows.org\r\n\r\n"
    headers, body = get_response(server_process, connection, msg)
    assert headers[0] == 'HTTP/1.1 200 OK'
    assert '<ul>' in body


def test_get_file(server_process, connection):
    msg = 'GET /sample.txt HTTP/1.1\r\nHost: localhost\r\n\r\n'
    headers, body = get_response(server_process, connection, msg)
    assert headers[0] == 'HTTP/1.1 200 OK'
    ctype = False
    for header in headers:
        if 'Content-Type: text/plain' in header:
            ctype = True
    assert ctype
    assert 'This is a very simple text file.' in body


def test_method_error(server_process, connection):
    msg = "POST path/to/stuff HTTP/1.1\r\nHost: www.codefellows.org\r\n\r\n"
    headers, body = get_response(server_process, connection, msg)
    assert headers[0] == 'HTTP/1.1 405 Method Not Allowed'


def test_not_found_error(server_process, connection):
    msg = 'GET /static/style.css HTTP/1.1\r\nHost: localhost\r\n\r\n'
    headers, body = get_response(server_process, connection, msg)
    assert headers[0] == 'HTTP/1.1 404 Not Found'


def test_no_host_error(server_process, connection):
    msg = 'GET / HTTP/1.1 \r\n\r\n'
    headers, body = get_response(server_process, connection, msg)
    assert headers[0] == 'HTTP/1.1 400 Bad Request'


def test_uplevel_error(server_process, connection):
    msg = 'GET /../../bin/stuff HTTP/1.1\r\nHost: localhost\r\n\r\n'
    headers, body = get_response(server_process, connection, msg)
    assert headers[0] == 'HTTP/1.1 403 Forbidden'
