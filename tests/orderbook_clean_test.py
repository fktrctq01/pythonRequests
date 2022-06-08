import pytest

from src.request import sender
from src.response.validator.message_validator import MessageValidator
from src.json_schemas.message import MESSAGE_SCHEMA
from src.entity.market_data import MarketData


def test_check_format_clean_order_book():
    """
    Проверка формата ответа на запрос /api/order/clean
    """
    response = sender.clean()
    validator = MessageValidator(response)
    validator.validate_status_code(200).validate_body(MESSAGE_SCHEMA, "Order book is clean.")


@pytest.mark.skip("Test in development")
def test_check_clean_order_book(create_order):
    """
    Проверка очистки стакана запросом /api/order/clean
    """

    response = sender.get_marked_data()
    market_data = MarketData(response.json())
    print()
    print(market_data)
    print(response.json())
    # if market_data.

    # response = sender.clean()
    # validator = MessageValidator(response)
    # validator.validate_status_code(200).validate_body(MESSAGE_SCHEMA, "Order book is clean")

