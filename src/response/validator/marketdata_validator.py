from src.enums.error import Error
from src.response.validator.main_validator import MainValidator


class MarketDataValidator(MainValidator):

    def validate_body(self, schema):
        schema.parse_obj(self.response_body)
        return self

    def check_asks_count(self, count):
        assert len(self.response_body["asks"]) == count, Error.WRONG_COUNT_ORDER_IN_RESPONSE.value
        return self

    def check_bids_count(self, count):
        assert len(self.response_body["bids"]) == count, Error.WRONG_COUNT_ORDER_IN_RESPONSE.value
        return self

    def check_asks_is_not_empty(self):
        assert len(self.response_body["asks"]) > 0, Error.EMPTY_ORDERBOOK.value
        return self

    def check_bids_is_not_empty(self):
        assert len(self.response_body["bids"]) > 0, Error.EMPTY_ORDERBOOK.value
        return self

    def check_availability_of_ask(self, price, quantity):
        asks = dict((order.get("price"), order.get("quantity")) for order in self.response_body["asks"])
        assert asks.get(price) == quantity, Error.WRONG_VALUE_ORDER_IN_RESPONSE.value
        return self

    def check_availability_of_a_bid(self, price, quantity):
        bids = dict((order.get("price"), order.get("quantity")) for order in self.response_body["bids"])
        assert bids.get(price) == quantity, Error.WRONG_VALUE_ORDER_IN_RESPONSE.value
        return self
