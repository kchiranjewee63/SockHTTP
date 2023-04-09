from enum import Enum

class Request:
    def __init__(self, raw_request, client_socket):
        self.raw_request = raw_request.decode()
        self.client_socket = client_socket
        self._headers = None
        self._body = None

    def get_headers(self):
        raw_headers = self.raw_request.split("\r\n\r\n", 1)[0]
        headers = {}
        lines = raw_headers.split("\r\n")
        headers["method"], headers["path"], headers["version"] = lines[0].split()
        for line in lines[1:]:
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
        return headers

    def get_body(self):
        if "Content-Length" in self.headers:
            length = int(self.headers["Content-Length"])
            body = self.raw_request.split("\r\n\r\n", 1)[1]
            while len(body) < length:
                body += self.client_socket.recv(length - len(body)).decode()
            return body

    @property
    def headers(self):
        if self._headers:
            return self._headers
        else:
            self._headers = self.get_headers()
            return self._headers

    @property
    def body(self):
        if self._body:
            return self._body
        else:
            self._body = self.get_body()
            return self._body

    def __str__(self):
        return f'{self.headers["method"]} {self.headers["path"]}'

class Method(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'