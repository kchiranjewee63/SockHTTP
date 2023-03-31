from routes import lookUpHandler, orderHandler

app = {"look-up": {"pattern": r'^/catalog/stocks/([a-zA-Z]+)$',
                   "method": "GET",
                    "handler": lookUpHandler},
       "order":   {"pattern": r'^/catalog/orders$',
                   "method": "POST",
                   "handler": orderHandler}}
