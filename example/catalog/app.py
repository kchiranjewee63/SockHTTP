from routes import lookUpHandler, orderHandler
from SockHTTP.request import Method

app = {"look-up": {"pattern": r'^/catalog/stocks/([a-zA-Z]+)$',
                   "method": Method.GET,
                    "handler": lookUpHandler},
       "order":   {"pattern": r'^/catalog/orders$',
                   "method": Method.POST,
                   "handler": orderHandler}}
