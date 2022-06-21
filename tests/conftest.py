from pytest import fixture

from src.entity.order import Order
from src.enums.order_type import OrderType
from tests.steps.api_order_create_steps import create_order
from tests.steps.api_order_delete_steps import delete_order


@fixture
def prepare_temporary_rnd_order():
    order = Order()
    create_order(order)
    yield order
    delete_order(order.id)


@fixture
def prepare_temporary_order_by_params(id, price, quantity, side):
    order = Order().set_id(id).set_price(price).set_quantity(quantity).set_side(side)
    rs = create_order(order)
    yield Order(rs.json())
    delete_order(rs.json()["id"])


@fixture
def prepare_temporary_order_on_buy():
    order = Order()
    create_order(order.set_side(OrderType.BUY))
    yield order
    delete_order(order.id)


@fixture
def prepare_temporary_order_on_sell():
    order = Order()
    create_order(order.set_side(OrderType.SELL))
    yield order
    delete_order(order.id)
