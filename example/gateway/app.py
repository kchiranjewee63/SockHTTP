from routes import lookUpHandler, orderHandler
from SockHTTP.request import Method

app = {"look-up": {"pattern": r'^/stocks/([a-zA-Z]+)$',
                         "method": Method.GET,
                         "handler": lookUpHandler},
       "order":   {"pattern": r'^/orders$',
                         "method": Method.POST,
                         "handler": orderHandler}}
