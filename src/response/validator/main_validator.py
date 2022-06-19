import json

import requests
from jsonschema import validate
from src.enums.global_enums import GlobalErrorMessages


class MainValidator:

    def __init__(self, response):
        self.response = response
        try:
            self.response_body = response.json()
        except requests.exceptions.JSONDecodeError:
            self.response_body = response.text
        self.response_status = response.status_code
        self.response_headers = response.headers

    def validate_body(self, schema):
        validate(self.response_body, schema)
        return self

    def is_empty_body(self, flag):
        assert (len(str(self.response_body)) == 0) is flag, GlobalErrorMessages.WRONG_BODY.value
        return self

    def validate_status_code(self, status_code):
        assert self.response_status == status_code, GlobalErrorMessages.WRONG_STATUS_CODE.value
        return self

    def validate_header(self, name, value):
        assert self.response_headers.get(name) == value, GlobalErrorMessages.WRONG_RESPONSE_HEADERS_VALUE.value
        return self

    def __str__(self):
        return f"""
        Status code: {self.response_status}. 
        Response body: {json.dumps(self.response_body, indent = 4)}
        Headers: {json.dumps(self.response_headers.__dict__, indent = 4)}.
        """
