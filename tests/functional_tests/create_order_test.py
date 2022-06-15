# @Date   : 14.06.2022
# @Author : Alexey Khmarskiy
# @File   : create_order_test.py

from src.entity.order import Order
from src.request import sender
from src.response.validator.order_validator import OrderValidator
from src.json_schemas.order import ORDER_SCHEMA
from src.enums.order_type import OrderType
from allure import feature, story, title, severity, step
from pytest import mark


@feature("Тестирование работы сервиса биржевого стакана")
@story("Тестирование запроса создания заявки")
@title("Валидация кода и тела ответа на запрос создания заказа с параметрами")
@severity('critical')
@mark.parametrize("id,price,quantity,side", [
    (1, 100, 10, OrderType.SELL),
    (2, 200, 20, OrderType.BUY)
])
def test_check_response_body_clean_order_book(id, price, quantity, side):
    """
    В тест-кейсе проверяем, что запрос создания заказа обрабатыватся с различными входными параметрами
    """
    order = Order().set_id(id).set_price(price).set_quantity(quantity).set_side(side).json()
    response_validator = OrderValidator(sender.create_order(order))
    response_validator.validate_status_code(200).validate_body(ORDER_SCHEMA)\
        .validate_id(id)\
        .validate_price(price)\
        .validate_quantity(quantity)\
        .validate_side(side)
