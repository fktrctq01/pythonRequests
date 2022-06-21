from src.json_schemas.order import ORDER_SCHEMA_RS
from src.request import sender
from src.response.validator.order_validator import OrderValidator
from allure import step


@step('Инициируем отправку запроса создания заявки на бирже')
def create_order(order):
    return sender.create_order(order.json())


@step('Проверяем, что заявка успешно создана')
def check_order(order):
    response_validator = OrderValidator(sender.get_order(order.id))
    response_validator\
        .validate_body(ORDER_SCHEMA_RS) \
        .validate_id(order.id)
