from src.enums.global_enums import GlobalErrorMessages
from src.response.validator.main_validator import MainValidator


class OrderValidator(MainValidator):

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
