# @Date   : 21.06.2022
# @Author : Alexey Khmarskiy
# @File   : api_get_marketdata_test.py

from allure import feature, story, title, severity
from pytest import mark

from src.entity.market_data import MarketData
from src.response.validator.marketdata_validator import MarketDataValidator
from src.response.validator.order_validator import OrderValidator
from tests.steps.api_orderbook_clean_steps import clean_orderbook
from tests.steps.api_marketdata_steps import get_marketdata, check_marketdata_is_empty
from tests.steps.common_steps import check_status_code


@feature("Тестирование работы сервиса биржевого стакана")
@story("5. Тестирование запроса получения стакана")
@title("5.01. Валидация кода и тела ответа при получении пустого стакана")
@severity('normal')
@mark.functional
@mark.positive
def test_check_response_body_empty_orderbook():
    """
    Предусловия: Нет
    Описание: В тест-кейсе проверяем, что запрос корректно обрабатывается при получении пустого стакана.
    Также проверяем, что в теле сообщение нет заявок
    """
    clean_orderbook()
    response = get_marketdata()
    check_status_code(MarketDataValidator(response), 200)
    check_marketdata_is_empty(MarketDataValidator(response))


@feature("Тестирование работы сервиса биржевого стакана")
@story("5. Тестирование запроса получения стакана")
@title("5.02. Валидация кода и тела ответа при получении стакана с заявками")
@severity('critical')
@mark.functional
@mark.positive
# TODO
def test_check_response_body_not_empty_orderbook(clean):
    """
    Предусловия: Нет
    Описание: В тест-кейсе проверяем, что запрос корректно обрабатывается при получении не пустого стакана.
    Также валидируем значения в заявках
    """
    response = get_marketdata()
    check_status_code(MarketDataValidator(response), 200)


@feature("Тестирование работы сервиса биржевого стакана")
@story("5. Тестирование запроса получения стакана")
@title("5.03. Проверка сортировки по убыванию цены")
@severity('normal')
@mark.functional
@mark.positive
@mark.parametrize("count", [10])
def test_check_sorted_orderbook(count, clean, prepare_temporary_orders):
    """
    Предусловия: Нет
    Описание: В тест-кейсе проверяем, что заявки на покупку и продажу сортируются по убыванию цены
    """
    buy_orders, sell_orders = prepare_temporary_orders
    buy_prices, sell_prices = [order.price for order in buy_orders], [order.price for order in sell_orders]
    buy_prices.sort(reverse=True, key=int)
    sell_prices.sort(reverse=True, key=int)

    response = MarketData(get_marketdata().json())
    for i in range(count):
        assert response.asks[i].price == buy_prices[i]
        assert response.bids[i].price == sell_prices[i]


@feature("Тестирование работы сервиса биржевого стакана")
@story("5. Тестирование запроса получения стакана")
@title("5.04. Проверка обработки запроса с методом {method}")
@severity('minor')
@mark.security
@mark.parametrize("method", ["POST", "PUT", "DELETE"])
def test_validate_response_get_orderbook_incorrect_method(method):
    """
    Описание: В тест-кейсе проверяем, что сервис отвечает ошибкой на запрос /api/marketdata, если метод отличный от GET
    """
    check_status_code(OrderValidator(get_marketdata(method)), 405)
