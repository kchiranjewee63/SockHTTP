import sys
sys.path.append('../../..')
sys.path.append('../../../SockHTTP')
from SockHTTP import httpServer
from app import app


# Start the server
server = httpServer.Server(routes= app, thread_pool_size = 8)
server.start(6060)
