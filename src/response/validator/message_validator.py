from src.enums.error import Error
from src.response.validator.main_validator import MainValidator


class MessageValidator(MainValidator):

    def validate_message(self, message):
        assert self.response_body["message"] == message, Error.WRONG_RESPONSE_VALUE_MESSAGE.value
        return self
