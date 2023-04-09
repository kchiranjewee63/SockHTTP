from SockHTTP.response import Response
import json
import requests
import logging
from readerwriterlock import rwlock
import os

logging.basicConfig(level = logging.DEBUG)

catalog_host = os.environ.get('CATALOG_HOST')
catalog_port = os.environ.get('CATALOG_PORT')

order_rwlock = rwlock.RWLockFair()

transaction_number = 0

def orderHandler(request):
    request_body = json.loads(request.body)
    catalog_response = requests.post(f"http://{catalog_host}:{catalog_port}/catalog/orders", json = request_body)
    catalog_http_code = catalog_response.status_code
    catalog_headers = catalog_response.headers
    catalog_body = catalog_response.text
    catalog_response.close()
    if catalog_http_code == 200:
        with order_rwlock.gen_wlock():
            global transaction_number
            transaction_number += 1
            body = {
                "data": {
                    "transaction_number": transaction_number
                }
            }
            return Response(200, json.dumps(body), {"Content-Type": "application/json"})
    else:
        logging.error(f"Received a {catalog_http_code} error from the catalog service: {catalog_body}")
        return Response(catalog_http_code, catalog_body, {"Content-Type": catalog_headers["Content-Type"]})