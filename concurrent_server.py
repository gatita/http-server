from server import parse_request, response_error, response_ok, resolve_uri
from gevent.server import StreamServer
from gevent.monkey import patch_all


def create_server():
    patch_all()
    gevent_server = StreamServer(('127.0.0.1', 8001), respond)
    print('Starting gevent server on port 8001')
    gevent_server.serve_forever()


def respond(socket, address):
    message_in = ""
    message_out = ""
    while True:
        msg = socket.recv(1024)
        message_in += msg
        if len(msg) < 1024:
            break
    try:
        uri = parse_request(message_in)
    except (NotImplementedError, ValueError, AttributeError) as e:
        message_out = response_error(e.message)
    else:
        # send parsed request to resolve uri
        try:
            body, resource_type = resolve_uri(uri)
        except (LookupError, ValueError, IOError) as e:
            message_out = response_error(e.message)
        else:
            message_out = response_ok(body, resource_type)
    socket.sendall(message_out)
    socket.close()


if __name__ == '__main__':
    create_server()
