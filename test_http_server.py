# -*- coding:UTF-8 -*-
from __future__ import unicode_literals
from server import response_error, response_ok
from email.utils import formatdate

import pytest


def test_response_ok():
    now = formatdate(usegmt=True)
    body = "Hello World, I need to travel."
    assert response_ok() == ('HTTP/1.1 200 OK\r\n'
        'Date: {}\r\nContent-Type: text/plain\r\nContent-Length: {}\r\n'
        'Connection: close\r\n\r\n{}'.format(now, len(body), body)
    )


def test_response_error():
    now = formatdate(usegmt=True)
    body = ("<html><body>\nThe server encountered an unexpected internal "
    "error.</body></html>")
    assert response_error() == ('HTTP 1.1 500 Internal Server Error'
        '\r\nDate:{}\r\nContent-Type: text/html\r\nContent-Length: {}\r\n'
        'Connection: close\r\n\r\n{}'.format(now, len(body), body)
    )