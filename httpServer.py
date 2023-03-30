import socket
from concurrent.futures import ThreadPoolExecutor
from processing import threaded
import logging

logging.basicConfig(level=logging.DEBUG)

class Server:
    def __init__(self, handler, backlog = 5, thread_pool_size = 4):
        self.handler = handler
        self.backlog = backlog
        self.thread_pool_size = thread_pool_size

    def start(self, port):
        server_socket = socket.socket()
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(self.backlog)
        logging.info(f'Listening on port {port}...')
        executor = ThreadPoolExecutor(max_workers = self.thread_pool_size)
        while True:
            client_socket, address = server_socket.accept()
            logging.info(f"Connected to {address[0]}:{address[1]}")
            executor.submit(threaded, self.handler, client_socket, address)