import http.client

def constructHeader(httpRequest, handler_response):
    response_headers = {}

    if httpRequest["headers"].get("Connection") == "keep-alive":
        response_headers["Connection"] = "keep-alive"

    if handler_response and handler_response.get("body"):
        response_headers["Content-Type"] = "text/html"
        response_headers["Content-Length"] = str(len(handler_response["body"]))
    else:
        response_headers["Content-Length"] = str(0)

    if handler_response and handler_response.get("headers"):
        response_headers.update(handler_response["headers"])

    return response_headers

def generateResponse(http_code = 200, headers = {}, body = ""):
    http_version = "HTTP/1.1"
    status_text = http.client.responses.get(http_code, "Unknown")
    status_line = f"{http_version} {http_code} {status_text}\r\n".encode()
    encoded_headers = {key.encode(): value.encode() for key, value in headers.items()}
    headers = b"\r\n".join([k + b": " + v for k, v in encoded_headers.items()])
    body = body.encode()
    response = status_line + headers + b"\r\n\r\n" + body
    return response