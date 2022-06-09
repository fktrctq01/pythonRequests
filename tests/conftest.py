import pytest

from src.entity.order import Order
from src.request import sender


@pytest.fixture
def create_order():
    order = Order()
    sender.create_order(order.json())
    return order
