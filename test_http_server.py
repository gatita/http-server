# -*- coding:UTF-8 -*-
from __future__ import unicode_literals
import server
from email.utils import formatdate

import pytest


def test_response_ok():
    now = formatdate(usegmt=True)
    body = "Hello World"
    assert server.response_ok() == ('HTTP/1.1 200 OK\r\n\
        Date: {}\r\nContent-Type: text/plain\r\nContent-Length: {}\r\n\
        Connection: close\r\n\r\nHello World'.format(now, len(body))
    )


def test_response_error():
    now = formatdate(usegmt=True)
    body = "<html><body>\nThe server encountered an unexpected internal \
    error.</body></html>"
    assert server.response_error() == ('HTTP 1.1 500 Internal Server Error\
        \r\nDate:{}\r\nContent-Type: text/html\r\nContent-Length: {}\r\n\
        Connection: close\r\n\r\n{}'.format(now, len(body), body)
    )