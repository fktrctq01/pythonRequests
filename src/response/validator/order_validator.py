import json

from jsonschema import validate
from src.enums.global_enums import GlobalErrorMessages


class OrderValidator:

    def __init__(self, response):
        self.response = response
        self.response_body = response.json()
        self.response_status = response.status_code
        self.headers = response.headers

    def validate_body(self, schema):
        validate(self.response_body, schema)
        return self

    def validate_status_code(self, status_code):
        assert self.response_status == status_code, GlobalErrorMessages.WRONG_STATUS_CODE.value
        return self

    def validate_id(self, id):
        assert self.response_body["id"] == str(id), GlobalErrorMessages.WRONG_RESPONSE_VALUE.value
        return self

    def validate_price(self, price):
        assert self.response_body["price"] == str(price), GlobalErrorMessages.WRONG_RESPONSE_VALUE.value
        return self

    def validate_quantity(self, quantity):
        assert self.response_body["quantity"] == str(quantity), GlobalErrorMessages.WRONG_RESPONSE_VALUE.value
        return self

    def validate_side(self, side):
        assert self.response_body["side"] == side.value, GlobalErrorMessages.WRONG_RESPONSE_VALUE.value
        return self

    def __str__(self):
        return f"""
        Status code: {self.response_status}. 
        Response body: {json.dumps(self.response_body, indent = 4)}
        Headers: {json.dumps(self.headers.__dict__, indent = 4)}.
        """
