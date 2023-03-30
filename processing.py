import re
from request import readHttpRequest
from response import constructHeader, generateResponse
import logging
import json

logging.basicConfig(level=logging.DEBUG)

def processRequest(handlers, request):
    try:
        logging.info(f"Received Request: {request}")
        path_match = None
        for handler in handlers.values():
            if re.match(handler["pattern"], request["path"]):
                path_match = request["path"]
                if request["method"] == handler["method"]:
                    return handler["handler"](request)
        if path_match:
            logging.error(f"Error. '{request['method']}' method not allowed for '{path_match}'")
            body = {
                "error": {
                    "code": 405,
                    "message": "Method not allowed."
                }
            }
            return {"http-code": 405, "headers": {"Content-Type": "application/json"}, "body": json.dumps(body)}
        else:
            logging.error(f"Error. '{request['path']}' not found")
            body = {
                "error": {
                    "code": 404,
                    "message": "Resource not found."
                }
            }
            return {"http-code": 404, "headers": {"Content-Type": "application/json"}, "body": json.dumps(body)}
    except Exception as e:
        logging.error(f"Received an error while processing the request.\n {e}")
        body = {
            "error": {
                "code": 500,
                "message": "Some internal error occurred."
            }
        }
        return {"http-code": 500, "headers": {"Content-Type": "application/json"}, "body": json.dumps(body)}

def threaded(handlers, client_socket, address):
    while True:

        request = client_socket.recv(1024)
        if not request:
            break

        try:
            httpRequest = readHttpRequest(request, client_socket)
        except Exception as e:
            logging.error(f"Received an error while parsing the http request.\n {e}", e)
            client_socket.sendall(generateResponse(http_code = 400, body = "Request format incorrect"))
            break

        handler_response = processRequest(handlers, httpRequest)
        response_http_code = handler_response["http-code"] if handler_response and handler_response.get("http-code") else 200
        response_headers = constructHeader(httpRequest, handler_response)
        response_body = handler_response["body"] if handler_response and handler_response.get("body") else ""

        client_socket.sendall(generateResponse(response_http_code, response_headers, response_body))

        if response_headers.get("Connection") != "keep-alive":
            break
    # Close the closed
    logging.info(f"Closing the connection with {address[0]}:{address[1]}")
    client_socket.close()