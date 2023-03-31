import http.client
import logging

logging.basicConfig(level=logging.DEBUG)
class Response:
    def __init__(self, http_code, body = None, headers = {}):
        self.http_code = http_code
        self.body = body
        self.headers = {}
        self.version = "HTTP/1.1"
        if self.body:
            self.headers["Content-Type"] = "text/html"
            self.headers["Content-Length"] = str(len(body))
        else:
            self.headers["Content-Length"] = str(0)
        self.headers.update(headers)

    def encode(self):
        status_text = http.client.responses.get(self.http_code, "Unknown")
        status_line = f"{self.version} {self.http_code} {status_text}\r\n".encode()
        encoded_headers = {key.encode(): value.encode() for key, value in self.headers.items()}
        headers = b"\r\n".join([k + b": " + v for k, v in encoded_headers.items()])
        body = self.body.encode() if self.body else b""
        return status_line + headers + b"\r\n\r\n" + body