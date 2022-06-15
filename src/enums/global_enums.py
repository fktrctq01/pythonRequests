from enum import Enum


class GlobalErrorMessages(Enum):
    WRONG_STATUS_CODE = "Received status code is not equal to expected."
    WRONG_RESPONSE_VALUE_MESSAGE = "Value parameters 'message' in received response not match with expected value."
    WRONG_RESPONSE_VALUE = "Value parameter in received response not match with expected value."
    WRONG_RESPONSE_HEADERS_VALUE = "Header value in received response not match with expected value."
    WRONG_COUNT_ORDER_IN_RESPONSE = "The number of orders in the order book does not match the expected."
    WRONG_VALUE_ORDER_IN_RESPONSE = "The quantity or price of the order in the response is not as expected."
    EMPTY_ORDERBOOK = "Asks or bids in the order book is empty"
