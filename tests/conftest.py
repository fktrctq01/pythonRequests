from pytest import fixture

from src.entity.order import Order
from src.enums.order_type import OrderType
from tests.steps.global_steps import send_request_create_order, check_order, delete_order


@fixture
def create_and_delete_rnd_order():
    order = Order()
    send_request_create_order(order)
    check_order(order)
    yield
    delete_order(order)

    return order

@fixture
def create_and_delete_buy_order():
    order = Order()
    send_request_create_order(Order().set_side(OrderType.BUY))
    check_order(order)
    yield
    delete_order(order)

    return order

@fixture
def create_and_delete_sell_order():
    order = Order()
    send_request_create_order(Order().set_side(OrderType.SELL))
    check_order(order)
    yield
    delete_order(order)

    return order
