import json

from jsonschema import validate, ValidationError


class OrderValidator:

    def __init__(self, request):
        self.request = request
        self.request_body = request.json
        self.request_headers = request.headers

    def validate_body(self, schema):
        try:
            validate(self.request_body, schema)
        except ValidationError:
            return False
        return True


    def __str__(self):
        return f"""
        Request body: {json.dumps(self.request_body, indent = 0)}
        Headers: {self.request_headers}.
        """
