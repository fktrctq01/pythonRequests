import requests
import properties
import json
import allure


def attach_response(response):
    request = response.request
    allure.attach(json.dumps(json.loads(request.body) if request.body else None, indent=4),
                  f"[REQUEST BODY] [{request.method}] {request.url}",
                  allure.attachment_type.JSON)
    allure.attach(json.dumps(request.headers.__dict__, indent=4),
                  f"[REQUEST HEADERS] [{request.method}] {request.url}",
                  allure.attachment_type.JSON)
    allure.attach(json.dumps(response.json() if response.text else None, indent=4),
                  f"[RESPONSE BODY] [{request.method}] [{response.status_code}] {request.url}",
                  allure.attachment_type.JSON)
    allure.attach(json.dumps(response.headers.__dict__, indent=4),
                  f"[RESPONSE HEADERS] [{request.method}] [{response.status_code}] {request.url}",
                  allure.attachment_type.JSON)


def get_order(id):
    response = requests.get(properties.URL + properties.ENDPOINTS_GET, {'id': id}, verify=False)
    attach_response(response)
    return response


def delete_order(id):
    response = requests.delete(properties.URL + properties.ENDPOINTS_DELETE, params={'id': id}, verify=False)
    attach_response(response)
    return response


def clean():
    response = requests.get(properties.URL + properties.ENDPOINTS_CLEAN, verify=False)
    attach_response(response)
    return response


def get_marked_data():
    response = requests.get(properties.URL + properties.ENDPOINTS_MARKETDATA, verify=False)
    attach_response(response)
    return response


def create_order(data):
    response = requests.post(
        properties.URL + properties.ENDPOINTS_CREATE,
        data=json.dumps(data),
        verify=False,
        headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    attach_response(response)
    return response
