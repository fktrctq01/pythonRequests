from src.json_schemas.message import MESSAGE_SCHEMA
from src.json_schemas.order import ORDER_SCHEMA
from src.request import sender
from src.response.validator.message_validator import MessageValidator
from src.response.validator.order_validator import OrderValidator
from allure import step

@step("Инициируем очистку стакана заявок")
def clean_orderbook():
    with step("Инициируем отправку запроса /api/order/clean"):
        response = sender.clean()
    with step("Валидируем код и тело ответа"):
        validator = MessageValidator(response)
        validator.validate_status_code(200).validate_body(MESSAGE_SCHEMA).validate_message("Order book is clean.")


@step('Отправляем запрос создания заявки на бирже')
def send_request_create_order(order):
    return sender.create_order(order.json())


@step('Проверяем, что заявка успешно создана')
def check_order(order):
    response_validator = OrderValidator(sender.get_order(order.id))
    response_validator.validate_status_code(200) \
        .validate_body(ORDER_SCHEMA) \
        .validate_id(order.id)


@step('Удаляем созданную для теста заявку на бирже')
def delete_order(order):
    OrderValidator(sender.delete_order(order.id))
