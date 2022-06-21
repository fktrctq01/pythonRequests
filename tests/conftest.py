from pytest import fixture

from allure import step
from src.entity.order import Order
from src.enums.order_type import OrderType
from tests.steps.api_order_get_steps import get_order
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
    response = create_order(Order().set_id(id).set_price(price).set_quantity(quantity).set_side(side))
    yield Order(response.json())
    delete_order(response.json()["id"])


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


@fixture
def check_order_and_delete_if_found(id):
    with step("Если id известен, тогда ищем по нему заявку и удаляем ее"):
        if id is not None and get_order(id).status_code == 200:
            delete_order(id)
