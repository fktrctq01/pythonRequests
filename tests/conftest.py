from src.entity.order import Order
from src.json_schemas.message import MESSAGE_SCHEMA
from src.json_schemas.order import ORDER_SCHEMA
from src.request import sender
from src.response.validator.message_validator import MessageValidator
from src.response.validator.order_validator import OrderValidator
from allure import step
from pytest import fixture


@step("Инициируем очистку стакана заявок")
def clean_orderbook():
    with step("Инициируем отправку запроса /api/order/clean"):
        response = sender.clean()
    with step("Валидируем код и тело ответа"):
        validator = MessageValidator(response)
        validator.validate_status_code(200).validate_body(MESSAGE_SCHEMA).validate_message("Order book is clean.")


@step('Отправляем запрос на создание заявки на бирже')
def create_order():
    order = Order()
    sender.create_order(order.json())
    return order


@step('Проверяем, что заявка успешно создана')
def check_order(order):
    response_validator = OrderValidator(sender.get_order(order.id))
    response_validator.validate_status_code(200) \
        .validate_body(ORDER_SCHEMA) \
        .validate_id(order.id)


@step('Удаляем созданную для теста заявку на бирже')
def delete_order(order):
    response_validator = OrderValidator(sender.delete_order(order.id))
    response_validator.validate_status_code(404)


@fixture
def create_and_delete_order():
    order = create_order()
    check_order(order)
    yield
    delete_order(order)

    return order
