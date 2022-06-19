from http.client import responses

import requests
import properties
import json
import allure


def attach(name, text, request):
    allure.attach(text, f"[{name}] [{request.method}] {request.url}", allure.attachment_type.JSON)


def attach_response(response):
    request = response.request
    attach("REQUEST BODY", json.dumps(json.loads(request.body) if request.body else None, indent=4), request)
    attach("REQUEST HEADERS", json.dumps(request.headers.__dict__, indent=4), request)
    try:
        attach("RESPONSE BODY", json.dumps(response.json(), indent=4), request)
    except requests.exceptions.RequestException:
        attach("RESPONSE BODY", response.text, request)
    attach("RESPONSE HEADERS", json.dumps(response.headers.__dict__, indent=4), request)
    allure.attach(responses[response.status_code], f"[RESPONSE STATUS] [{response.status_code}]")


def get_order(id, method='GET'):
    response = requests.request(method, properties.URL + properties.ENDPOINTS_GET, params={'id': id}, verify=False)
    attach_response(response)
    return response


def delete_order(id, method='DELETE'):
    response = requests.request(method, properties.URL + properties.ENDPOINTS_DELETE, params={'id': id}, verify=False)
    attach_response(response)
    return response


def clean(method='GET'):
    response = requests.request(method, properties.URL + properties.ENDPOINTS_CLEAN, verify=False)
    attach_response(response)
    return response


def get_marked_data(method='GET'):
    response = requests.request(method, properties.URL + properties.ENDPOINTS_MARKETDATA, verify=False)
    attach_response(response)
    return response


def create_order(data, method='POST'):
    response = requests.request(
        method,
        properties.URL + properties.ENDPOINTS_CREATE,
        data=json.dumps(data),
        verify=False,
        headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    attach_response(response)
    return response
