from routes import lookUpHandler, orderHandler

app = {"look-up": {"pattern": r'^/stocks/([a-zA-Z]+)$',
                         "method": "GET", 
                         "handler": lookUpHandler},
       "order":   {"pattern": r'^/orders$',
                         "method": "POST",
                         "handler": orderHandler}}
