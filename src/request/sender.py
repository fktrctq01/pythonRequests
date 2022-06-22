from http.client import responses
import requests
import properties
import json
import allure


def formatted_text(obj):
    if obj:
        try:
            return json.dumps(json.loads(obj), indent=4)
        except (requests.exceptions.RequestException, BaseException):
            return json.dumps(obj, indent=4)
    else:
        return json.dumps(None, indent=4)


def attach(text, name, request):
    allure.attach(text, f"[{name}] [{request.method}] {request.url}", allure.attachment_type.JSON)


def attach_response(response):
    request = response.request
    attach(formatted_text(request.body), "REQUEST BODY", request)
    attach(formatted_text(request.headers.__dict__), "REQUEST HEADERS", request)
    attach(formatted_text(response.text), "RESPONSE BODY", request)
    attach(formatted_text(response.headers.__dict__), "RESPONSE HEADERS", request)
    attach(formatted_text(f"{response.status_code} {responses[response.status_code]}"), "RESPONSE STATUS", request)


def get_order(id, method='GET'):
    response = requests.request(
        method,
        properties.URL + properties.ENDPOINTS_GET,
        params={'id': id},
        verify=False)
    attach_response(response)
    return response


def delete_order(id, method='DELETE'):
    response = requests.request(
        method,
        properties.URL + properties.ENDPOINTS_DELETE,
        params={'id': id},
        verify=False)
    attach_response(response)
    return response


def clean(method='GET'):
    response = requests.request(
        method,
        properties.URL + properties.ENDPOINTS_CLEAN,
        verify=False)
    attach_response(response)
    return response


def get_marked_data(method='GET'):
    response = requests.request(
        method,
        properties.URL + properties.ENDPOINTS_MARKETDATA,
        verify=False)
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
