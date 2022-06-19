from behave import *
from src.request import sender
from src.response.validator.order_validator import OrderValidator
from src.json_schemas.order import ORDER_SCHEMA
from src.entity.order import Order, OrderType


@when('отправляем запрос {id} на создание заявки на {side} по цене={price} в количестве={quantity}')
def create_order(context, id, side, price, quantity):
    response = sender.create_order(Order().set_id(id).set_price(price).set_quantity(quantity).set_side(OrderType(side)).json())
    context.response = response


@then('проверяем, что в ответе вернулся код {code}')
def check_status_code(context, code):
    response_validator = OrderValidator(context.response)
    response_validator.validate_status_code(200)


@then('проверяем, что в ответе тело сообщения с id={id}, price={price}, quantity={quantity} и side={side}')
def check_body(context, id, price, quantity, side):
    response_validator = OrderValidator(context.response)
    response_validator.validate_body(ORDER_SCHEMA) \
        .validate_id(id)\
        .validate_price(price)\
        .validate_quantity(quantity)\
        .validate_side(OrderType(side))
