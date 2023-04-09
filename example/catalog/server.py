import sys
sys.path.append('../../..')
sys.path.append('../../../SockHTTP')
from SockHTTP.httpServer import Server
from app import app

# Start the server
server = Server(routes= app, thread_pool_size = 8)
server.start(7070)