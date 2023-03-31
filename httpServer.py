import socket
import handler
import logging

logging.basicConfig(level=logging.DEBUG)

class Server:
    def __init__(self, routes, backlog = 5, thread_pool_size = 4):
        self.routes = routes
        self.backlog = backlog
        self.thread_pool_size = thread_pool_size
        self.server_socket = None
        self.handler = None

    def start(self, port):
        try:
            self.server_socket = socket.socket()
            self.handler = handler.Handler(self.routes, self.thread_pool_size)
            self.server_socket.bind(('0.0.0.0', port))
            self.server_socket.listen(self.backlog)
            logging.info(f'Listening on port {port}...')
            while True:
                client_socket, address = self.server_socket.accept()
                logging.info(f'Connected to {address[0]}:{address[1]}')
                self.handler.handle(client_socket, address)
        except Exception as e:
            logging.info(f'An error encountered while starting the server: {e}')