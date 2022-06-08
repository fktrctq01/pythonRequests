import pytest

from src.entity.order import Order
from src.request import sender


@pytest.fixture
def create_order():
    response = sender.create_order(Order().default().build())
    return Order(response.json())
