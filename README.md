# http-server

#### Implementation of a simple HTTP server with the following functions:
* response_ok: Returns a well formed HTTP "200 OK" response as a byte string suitable for transmission through a socket.
* reponse_error: Returns a well formed HTTP "500 Internal Server Error" response.

When run, the server accumuates an incoming request into a variable,
'logs' that request by printing it to stdout, and returns a well-formed
HTTP 200 response to the client.



