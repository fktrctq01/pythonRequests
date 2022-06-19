from pytest import fixture

from src.entity.order import Order
from src.enums.order_type import OrderType
from tests.steps.api_order_create_steps import create_order, check_order
from tests.steps.api_order_delete_steps import delete_order


@fixture
def prepare_temporary_rnd_order():
    order = Order()
    create_order(order)
    check_order(order)
    yield order
    delete_order(order.id)


@fixture
def create_and_delete_buy_order():
    order = Order()
    create_order(order.set_side(OrderType.BUY))
    check_order(order)
    yield order
    delete_order(order.id)


@fixture
def create_and_delete_sell_order():
    order = Order()
    create_order(order.set_side(OrderType.SELL))
    check_order(order)
    yield order
    delete_order(order.id)
