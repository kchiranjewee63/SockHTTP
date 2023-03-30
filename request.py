def readBody(request, length, client_socket):
    body = request.split("\r\n\r\n", 1)[1]
    while len(body) < length:
        body += client_socket.recv(length - len(body)).decode()
    return body

def readHttpRequest(request, client_socket):
    request = request.decode()
    lines = request.split("\r\n")
    method, path, _ = lines[0].split()
    headers = {}
    body = None
    for line in lines[1:]:
        if line == "":
            break
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()
    if "Content-Length" in headers:
        length = int(headers["Content-Length"])
        body = readBody(request, length, client_socket)
    return {"method": method, "path": path, "headers": headers, "body": body}