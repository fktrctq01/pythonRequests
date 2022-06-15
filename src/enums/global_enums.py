from enum import Enum


class GlobalErrorMessages(Enum):
    WRONG_STATUS_CODE = "Received status code is not equal to expected."
    WRONG_RESPONSE_VALUE_MESSAGE = "Value parameters 'message' in received response not match with expected value."
    WRONG_RESPONSE_VALUE = "Value parameter in received response not match with expected value."
