import json

from src.enums.global_enums import GlobalErrorMessages


class MarketDataValidator:

    def __init__(self, response):
        self.response = response
        self.response_body = response.json()
        self.response_status = response.status_code
        self.response_headers = response.headers

    def validate_body(self, schema):
        schema.parse_obj(self.response_body)
        return self

    def validate_status_code(self, status_code):
        assert self.response_status == status_code, GlobalErrorMessages.WRONG_STATUS_CODE.value
        return self

    def __str__(self):
        return f"""
        Status code: {self.response_status}. 
        Response body: {json.dumps(self.response_body, indent = 0)}
        Headers: {self.response_headers}.
        """
