from src.enums.error import Error
from src.response.validator.main_validator import MainValidator


class OrderValidator(MainValidator):

    def validate_id(self, id):
        assert self.response_body["id"] == str(id), Error.WRONG_RESPONSE_VALUE.value
        return self

    def validate_price(self, price):
        assert self.response_body["price"] == str(price), Error.WRONG_RESPONSE_VALUE.value
        return self

    def validate_quantity(self, quantity):
        assert self.response_body["quantity"] == str(quantity), Error.WRONG_RESPONSE_VALUE.value
        return self

    def validate_side(self, side):
        assert self.response_body["side"] == side.value, Error.WRONG_RESPONSE_VALUE.value
        return self

    def validate_order(self, order):
        self.validate_id(order.id) \
            .validate_price(order.price) \
            .validate_quantity(order.quantity) \
            .validate_side(order.side)
        return self
