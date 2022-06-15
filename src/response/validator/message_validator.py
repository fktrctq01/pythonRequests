from src.enums.global_enums import GlobalErrorMessages
from src.response.validator.main_validator import MainValidator


class MessageValidator(MainValidator):

    def validate_message(self, message):
        assert self.response_body["message"] == message, GlobalErrorMessages.WRONG_RESPONSE_VALUE_MESSAGE.value
        return self
