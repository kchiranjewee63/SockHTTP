# SockHTTP: An HTTP framework built with sockets

SockHTTP is an HTTP framework built from socket programming, designed to help developers better understand how HTTP APIs
and servers work.

SockHTTP is an HTTP framework built from socket programming, designed to help developers better understand how HTTP APIs
and servers work. This project was created for educational purposes and aims to provide a practical demonstration
of how HTTP servers and APIs are constructed from the ground up using sockets. The framework includes several key
features, such as routing, support for HTTP methods, handling HTTP requests and responses, and thread pooling for
concurrent request processing. Additionally, the repository includes
[an example application consisting of three microservices](example/README.md#example-microservices) built using the
SockHTTP framework. The application is designed to demonstrate how this simple framework can be used to build complex
applications. Overall, SockHTTP provides a hands-on, educational experience that allows developers to gain a deeper
understanding of HTTP APIs and servers.

The code is written in python and is very simple to understand. The framework totally consists of only four files:
`httpServer.py`, `handler.py`, `request.py`, and `response.py`.

### How to use the framework to build HTTP servers

`httpServer.py` provides `Server` class. The class's constructor takes three arguments:

1. `routes`
A map that consists an entry for each API. And for each API, it consists of a regular expression representing the
path URL of the API, its HTTP method type(GET, POST, ...), and the function that processes the particular API requests.
The function takes the request as argument and return the response. The framework parses a http request
and sends the Request Object to the handler method. The method should return a Response Object. The framework encodes
the Response Object and response to the request.

2. `backlog`
The maximum number of connections that can be waiting in the queue while the server is processing previous requests.
This is basically passed as the argument to server's
[socket listen method](https://docs.python.org/3/library/socket.html#:~:text=socket.listen(%5Bbacklog%5D)).

3. `thread_pool_size`
The maximum number of threads in the server's thread pool.

Create an object of the class, and call `start` method on the object, which takes a port number as the argument.

For instance, the below server provides an API `GET /reverse` to reverse the request body and runs at port number `8080`.

```python
from SockHTTP.httpServer import Server
from SockHTTP.response import Response

def reverseBody(Request):
    request_body = Request.body
    response_body = request_body[-1:]
    return Response(200, response_body)
    
routes = {"Reverse": {"pattern": r'^/reverse$',
                      "method": "GET",
                      "handler": reverseBody}}

httpServer = Server(routes, backlog = 5, thread_pool_size = 8)
httpServer.start(8080)
```

Check [this](example/README.md#example-microservices) for an example application consisting of three microservices
build using this framework.