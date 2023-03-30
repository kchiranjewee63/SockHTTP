import socket
from concurrent.futures import ThreadPoolExecutor
from processing import threaded
import logging

logging.basicConfig(level=logging.DEBUG)

def server(port, handlers, thread_pool_size = 4):
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    logging.info(f'Listening on port {port}...')
    executor = ThreadPoolExecutor(max_workers = thread_pool_size)
    while True:
        client_socket, address = server_socket.accept()
        logging.info(f"Connected to {address[0]}:{address[1]}")
        executor.submit(threaded, handlers, client_socket, address)