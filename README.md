# SockHTTP: An HTTP framework built with sockets

SockHTTP is an HTTP framework built from socket programming, designed to help developers better understand how HTTP APIs
and servers work. This project was created for educational purposes and aims to provide a practical demonstration
of how HTTP servers and APIs are constructed from the ground up using sockets. The framework includes several key
features, such as routing, support for HTTP methods, handling HTTP requests and responses, and thread pooling for
concurrent request processing. Additionally, the repository includes
[an example application consisting of three microservices](https://github.com/kchiranjewee63/SockHTTP/tree/main/example)
built using the SockHTTP framework. This example application is designed to demonstrate how this simple framework can be
used to build complex applications. Overall, SockHTTP provides a hands-on, educational experience that allows developers
to gain a deeper understanding of HTTP APIs and servers.

The code is written in python and is very simple to understand. The framework totally consists of only four files:
`httpServer.py`, `handler.py`, `request.py`, and `response.py`.

### How to use the framework to build HTTP servers

`httpServer.py` provides `Server` class. The class's constructor takes three arguments:

1. `routes`
A map that consists an entry for each API. And for each API, it consists of a regular expression representing the
path URL of the API, its HTTP method type(`GET`, `POST`, ...), and the function that processes the particular API requests.
The function takes the request as argument and return the response. The framework parses a http request
and calls the function with the Request Object. The function should return a Response Object. The framework encodes
the Response Object and response to the request.

2. `backlog`
The maximum number of connections that can be waiting in the queue while the server is processing previous requests.
This is basically passed as the argument to the server's
[socket listen method](https://docs.python.org/3/library/socket.html#:~:text=socket.listen(%5Bbacklog%5D)). Its
default value is 5.

3. `thread_pool_size`
The maximum number of threads in the server's thread pool.

Create an object of the class, and call the `start` method on the object, which takes a port number as the argument.

For instance, the below server runs at the port number `8080` and provides an API `GET /reverse` that reverses the request body.

```python
from SockHTTP.httpServer import Server
from SockHTTP.response import Response
from SockHTTP.request import Method

def reverseBody(request):
    request_body = request.body
    response_body = request_body[::-1]
    return Response(200, response_body)
    
routes = {"Reverse": {"pattern": r'^/reverse$',
                      "method": Method.GET,
                      "handler": reverseBody}}

http_server = Server(routes, thread_pool_size = 8)
http_server.start(8080)
```

Check [this](https://github.com/kchiranjewee63/SockHTTP/tree/main/example) for an example application consisting of
three microservices build using this framework.
