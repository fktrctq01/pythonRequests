import requests
import properties
import json

def doGetRequest(id):
    params = {'id': id}
    return requests.get(properties.URL+properties.ENDPOINTS_GET, params, verify=False)

def doDeleteRequest(id):
    params = {'id': id}
    return requests.delete(properties.URL+properties.ENDPOINTS_DELETE, params=params, verify=False)

def doCleanRequest():
    return requests.get(properties.URL+properties.ENDPOINTS_CLEAN, verify=False)

def doGetMarkedDataRequest():
    return requests.get(properties.URL+properties.ENDPOINTS_MARKETDATA, verify=False)

def doCreateOrderRequest(data):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    return requests.post(properties.URL+properties.ENDPOINTS_CREATE, data=json.dumps(data), verify=False, headers=headers)