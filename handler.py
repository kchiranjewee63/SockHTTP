import re
from request import Request
from response import Response
import logging
from concurrent.futures import ThreadPoolExecutor
import traceback

logging.basicConfig(level=logging.DEBUG)

class Handler:
    def __init__(self, routes, thread_pool_size):
        self.routes = routes
        self.thread_pool_size = thread_pool_size
        self.executor = ThreadPoolExecutor(max_workers = self.thread_pool_size)

    def clientHandler(self, client_socket, address):
        while True:
            request = client_socket.recv(1024)
            if not request:
                break
            try:
                httpRequest = Request(request, client_socket)
            except Exception as e:
                logging.error(f"Received an error while parsing the http request.\n {e}", e)
                logging.error(traceback.format_exc())
                client_socket.sendall(Response(400, "Request format incorrect"))
                break
            response = self.processRequest(httpRequest)
            if httpRequest.headers.get("Connection") == "keep-alive" and not response.headers.get("Connection"):
                response.headers["Connection"] = "keep-alive"
            client_socket.sendall(response.encode())
            logging.info(f"Request {httpRequest} completed: {response.http_code}")
            if response.headers.get("Connection") != "keep-alive":
                break
        # Close the closed
        logging.info(f"Closing the connection with {address[0]}:{address[1]}")
        client_socket.close()

    def processRequest(self, request):
        try:
            logging.info(f"Received Request: {request}")
            path_match = None
            for handler in self.routes.values():
                if re.match(handler["pattern"], request.headers["path"]):
                    path_match = request.headers["path"]
                    if request.headers["method"] == handler["method"].value:
                        return handler["handler"](request)
            if path_match:
                logging.error(f"Error. '{request.headers['method']}' method not allowed for '{path_match}'")
                return Response(405)
            else:
                logging.error(f"Error. '{request.headers['path']}' not found")
                return Response(404)
        except Exception as e:
            logging.error(f"Received an error while processing the request.\n {e}")
            logging.error(traceback.format_exc())
            return Response(500)

    def handle(self, client_socket, address):
        self.executor.submit(self.clientHandler, client_socket, address)