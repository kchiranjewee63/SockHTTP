from routes import orderHandler

app = {"order":   {"pattern": r'^/order/orders$',
                   "method": "POST",
                   "handler": orderHandler}}
