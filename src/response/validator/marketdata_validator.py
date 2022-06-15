from src.enums.global_enums import GlobalErrorMessages
from src.response.validator.main_validator import MainValidator


class MarketDataValidator(MainValidator):

    def validate_body(self, schema):
        schema.parse_obj(self.response_body)
        return self

    def check_count_asks(self, count):
        assert len(self.response_body["asks"]) == count, GlobalErrorMessages.WRONG_COUNT_ORDER_IN_RESPONSE.value
        return self

    def check_count_bids(self, count):
        assert len(self.response_body["bids"]) == count, GlobalErrorMessages.WRONG_COUNT_ORDER_IN_RESPONSE.value
        return self

    def check_availability_of_ask(self, price, quantity):
        asks = dict((order.get("price"), order.get("quantity")) for order in self.response_body["asks"])
        assert True if asks.get(price) == quantity else False, GlobalErrorMessages.WRONG_VALUE_ORDER_IN_RESPONSE.value
        return self

    def check_availability_of_a_bid(self, price, quantity):
        bids = dict((order.get("price"), order.get("quantity")) for order in self.response_body["bids"])
        assert True if bids.get(price) == quantity else False, GlobalErrorMessages.WRONG_VALUE_ORDER_IN_RESPONSE.value
        return self
