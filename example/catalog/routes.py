from SockHTTP import response
import re
import json
import logging
from readerwriterlock import rwlock

logging.basicConfig(level = logging.DEBUG)

catalog_rwlock = rwlock.RWLockFair()

catalog = {"NXTI": {"Price": 210.19, "Volume": 0, "Available": 8000},
           "SOLBIO": {"Price": 100.9, "Volume": 0, "Available": 1000},
           "QXIL": {"Price": 102.1, "Volume": 0, "Available": 300}}

def lookUpHandler(request):
    share_name = re.match(r'^/catalog/stocks/([a-zA-Z]+)$', request.headers["path"]).group(1)
    with catalog_rwlock.gen_rlock():
        share = catalog.get(share_name)
        if not share:
            body = {
                "error": {
                    "code": 404,
                    "message": "stock not found"
                }
            }
            logging.error(f"Stock {share} not found.")
            return response.Response(404, json.dumps(body), {"Content-Type": "application/json"})
        body = {
            "data": {
                "name": share_name,
                "price": share["Price"],
                "quantity": share["Available"]
            }
        }
        return response.Response(200, json.dumps(body), {"Content-Type": "application/json"})

def orderHandler(request):
    request_body = json.loads(request.body)
    share_name, quantity, operation = request_body["name"], request_body["quantity"], request_body["type"]
    with catalog_rwlock.gen_wlock():
        if not catalog.get(share_name):
            body = {
                "error": {
                    "code": 404,
                    "message": "stock not found"
                }
            }
            logging.error(f"Stock {share_name} not found.")
            return response.Response(404, json.dumps(body), {"Content-Type": "application/json"})
        if operation == "sell":
            catalog[share_name].update({"Available": catalog[share_name]["Available"] + quantity,
                                                    "Volume": catalog[share_name]["Volume"] + quantity})
            return response.Response(200)
        elif operation == "buy":
            if catalog[share_name]["Available"] >= quantity:
                catalog[share_name].update({"Available": catalog[share_name]["Available"] - quantity,
                                                    "Volume": catalog[share_name]["Volume"] + quantity})
                return response.Response(200)
            else:
                body = {
                    "error": {
                        "code": 400,
                        "message": "Buy failed. Requested number of shares not available."
                    }
                }
                logging.error(f"{quantity} of {share_name} not available to buy")
                return response.Response(400, json.dumps(body), {"Content-Type": "application/json"})
        else:
            body = {
                "error": {
                    "code": 400,
                    "message": f"Incorrect operation type provided in the request."
                }
            }
            logging.error(f"Incorrect operation type {operation} provided in the request.")
            return response.Response(400, json.dumps(body), {"Content-Type": "application/json"})