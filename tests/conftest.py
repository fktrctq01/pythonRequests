from pytest import fixture

from allure import step
from src.entity.order import Order
from src.enums.order_type import OrderType
from tests.steps.api_order_get_steps import get_order
from tests.steps.api_order_create_steps import create_order
from tests.steps.api_order_delete_steps import delete_order
from tests.steps.api_orderbook_clean_steps import clean_orderbook


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
def prepare_temporary_orders(count_buy, count_sell):
    buy_orders = [Order().set_id(i).set_side(OrderType.BUY) for i in range(1, count_buy + 1)]
    sell_orders = [Order().set_id(i + count_buy).set_side(OrderType.SELL) for i in range(1, count_sell + 1)]

    for i in range(count_buy):
        create_order(buy_orders[i])
    for i in range(count_sell):
        create_order(sell_orders[i])

    yield buy_orders, sell_orders

    for i in range(count_buy):
        delete_order(buy_orders[i].id)
    for i in range(count_sell):
        delete_order(sell_orders[i].id)


@fixture
def clean():
    clean_orderbook()


@fixture
def check_order_and_delete_if_found(id):
    with step("Если id известен, тогда ищем по нему заявку и удаляем ее"):
        if id is not None and get_order(id).status_code == 200:
            delete_order(id)
