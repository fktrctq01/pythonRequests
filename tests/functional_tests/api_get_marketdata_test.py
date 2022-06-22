# @Date   : 21.06.2022
# @Author : Alexey Khmarskiy
# @File   : api_get_marketdata_test.py

from allure import feature, story, title, severity, step
from pytest import mark, param

from src.entity.market_data import MarketData
from src.response.validator.marketdata_validator import MarketDataValidator
from src.response.validator.order_validator import OrderValidator
from tests.steps.api_orderbook_clean_steps import clean_orderbook
from tests.steps.api_marketdata_steps import get_marketdata, check_marketdata_is_empty, \
    check_marketdata_bids_is_empty, check_marketdata_asks_is_empty, check_availability_of_a_bid, \
    check_availability_of_ask
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
@mark.parametrize("count_buy,count_sell", [
    (0, 0),
    (0, 1),
    (1, 0),
    param(1, 1, marks=mark.smoke),
    (10, 5),
    (3, 15)
])
def test_check_response_body_not_empty_orderbook(count_buy, count_sell, clean, prepare_temporary_orders):
    """
    Предусловия: В стакане есть набор заявок на покупку и/или продажу
    Описание: В тест-кейсе проверяем, что запрос корректно обрабатывается при получении не пустого стакана.
    Также валидируем значения в заявках
    """
    # Получаем заявки на покупку и продажу, которые подготовили для выполнения теста
    buy_orders, sell_orders = prepare_temporary_orders

    # Получаем маркетдату и проверяем код ответа
    response = MarketDataValidator(get_marketdata())
    check_status_code(response, 200)

    # Проверяем, что заявок на покупку ожидаемое количество(из предусловия)
    if count_buy == 0:
        check_marketdata_asks_is_empty(response)
    else:
        # Валидируем заявки на соответствие цены и количества
        for i in range(count_buy):
            check_availability_of_ask(response, buy_orders[i].price, buy_orders[i].quantity)

    # Проверяем, что заявок на продажу ожидаемое количество(из предусловия)
    if count_sell == 0:
        check_marketdata_bids_is_empty(response)
    else:
        # Валидируем заявки на соответствие цены и количества
        for i in range(count_sell):
            check_availability_of_a_bid(response, sell_orders[i].price, sell_orders[i].quantity)


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
    with step('Проверяем, что применена сортировка от большей цены к меньшей'):
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
