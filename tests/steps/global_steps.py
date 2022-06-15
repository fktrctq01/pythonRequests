import allure

from src.request import sender
from src.response.validator.message_validator import MessageValidator
from src.json_schemas.message import MESSAGE_SCHEMA


@allure.step("Инициируем очистку стакана заявок")
def step_check_response_body_and_status_code_for_clean_order_book():
    with allure.step("Инициируем отправку запроса /api/order/clean"):
        response = sender.clean()
    with allure.step("Валидируем код и тело ответа"):
        validator = MessageValidator(response)
        validator.validate_status_code(200).validate_body(MESSAGE_SCHEMA).validate_message("Order book is clean.")
