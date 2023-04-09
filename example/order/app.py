from routes import orderHandler
from SockHTTP.request import Method

app = {"order":   {"pattern": r'^/order/orders$',
                   "method": Method.POST,
                   "handler": orderHandler}}
