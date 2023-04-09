from SockHTTP.response import Response
import json
import requests
import os

catalog_host = os.environ.get('CATALOG_HOST')
catalog_port = os.environ.get('CATALOG_PORT')
order_host = os.environ.get('ORDER_HOST')
order_port = os.environ.get('ORDER_PORT')

def lookUpHandler(request):
    catalog_response = requests.get(f"http://{catalog_host}:{catalog_port}/catalog{request.headers['path']}")
    http_code = catalog_response.status_code
    headers = catalog_response.headers
    body = catalog_response.text
    catalog_response.close()
    return Response(http_code, body, {"Content-Type": headers["content-type"]})

def orderHandler(request):
    order_response = requests.post(f"http://{order_host}:{order_port}/order/orders", json = json.loads(request.body))
    http_code = order_response.status_code
    headers = order_response.headers
    body = order_response.text
    order_response.close()
    return Response(http_code, body, {"Content-Type": headers["content-type"]})