import requests
import properties
import json
import allure


def attach_response(response):
    allure.attach(f"[{response.request.method}] {response.request.url}", "request_method_and_url")
    allure.attach(response.request.body.__str__(), "request_body")
    allure.attach(response.request.headers.__str__(), "request_headers")
    allure.attach(response.text, "response_body")
    allure.attach(response.headers.__str__(), "response_header")


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
