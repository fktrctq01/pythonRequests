import json

import requests
from jsonschema import validate
from src.enums.error import Error


class MainValidator:

    def __init__(self, response):
        self.response = response
        self.response_status = response.status_code
        self.response_headers = response.headers
        try:
            self.response_body = response.json()
        except requests.exceptions.JSONDecodeError:
            self.response_body = response.text

    def validate_body(self, schema):
        validate(self.response_body, schema)
        return self

    def check_body_is_empty(self):
        assert "".__eq__(str(self.response_body)), Error.WRONG_BODY.value

    def check_body_is_not_empty(self):
        assert not "".__eq__(str(self.response_body)), Error.WRONG_BODY.value

    def validate_status_code(self, status_code):
        assert self.response_status == status_code, Error.WRONG_STATUS_CODE.value
        return self

    def validate_header(self, name, value):
        assert self.response_headers.get(name) == value, Error.WRONG_RESPONSE_HEADERS_VALUE.value
        return self

    def __str__(self):
        return json.dumps({
            "code": self.response_status,
            "body": self.response_body,
            "headers": self.response_headers.__dict__
        }, indent=4)

    def __repr__(self):
        return self.__str__()
