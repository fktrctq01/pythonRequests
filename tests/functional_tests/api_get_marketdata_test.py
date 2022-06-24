# @Date   : 21.06.2022
# @Author : Alexey Khmarskiy
# @File   : api_get_marketdata_test.py

from allure import feature, story, title, severity, step
from pytest import mark, param

from src.entity.market_data import MarketData
from src.response.validator.marketdata_validator import MarketDataValidator
from src.response.validator.order_validator import OrderValidator
from tests.steps.api_orderbook_clean_steps import clean_orderbook
from tests.steps.api_marketdata_steps import get_marketdata, check_marketdata_bids_asks_count, \
    check_marketdata_bids_count, check_marketdata_asks_count, check_availability_of_a_bid, check_availability_of_ask
from tests.steps.common_steps import check_status_code, check_headers


@feature("Тестирование работы сервиса биржевого стакана")
@story("Тестирование запроса получения стакана")
class TestApiGetMarketdata:

    @title("01. Валидация кода и тела ответа при получении пустого стакана")
    @severity('normal')
    @mark.functional
    @mark.positive
    @mark.not_parallel
    def test_check_response_body_empty_orderbook(self):
        """
        Предусловия: Нет
        Описание: В тест-кейсе проверяем, что запрос корректно обрабатывается при получении пустого стакана.
        Также проверяем, что в теле сообщение нет заявок
        """
        clean_orderbook()
        response = MarketDataValidator(get_marketdata())
        check_status_code(response, 200)
        check_marketdata_bids_asks_count(response, 0, 0)

    @title("02. Валидация кода и тела ответа при получении стакана с заявками")
    @severity('critical')
    @mark.functional
    @mark.positive
    @mark.not_parallel
    @mark.parametrize("count_buy,count_sell", [
        (0, 0),
        (0, 1),
        (1, 0),
        param(1, 1, marks=mark.smoke),
        (10, 5),
        (3, 15)
    ])
    def test_check_response_body_not_empty_orderbook(self, count_buy, count_sell, clean_orderbook_ft,
                                                     prepare_temporary_order_list):
        """
        Предусловия: В стакане есть набор заявок на покупку и/или продажу
        Описание: В тест-кейсе проверяем, что запрос корректно обрабатывается при получении не пустого стакана.
        Также валидируем значения в заявках
        """
        # Получаем заявки на покупку и продажу, которые подготовили для выполнения теста
        buy_orders, sell_orders = prepare_temporary_order_list

        # Получаем маркетдату и проверяем код ответа
        response = MarketDataValidator(get_marketdata())
        check_status_code(response, 200)

        # Проверяем, что заявок на покупку и продажу ожидаемое количество(из предусловия)
        check_marketdata_asks_count(response, count_buy)
        check_marketdata_bids_count(response, count_sell)

        # Валидируем заявки на покупку и продажу на соответствие цены и количества
        if count_buy != 0:
            for i in range(count_buy):
                check_availability_of_ask(response, buy_orders[i].price, buy_orders[i].quantity)
        if count_sell != 0:
            for i in range(count_sell):
                check_availability_of_a_bid(response, sell_orders[i].price, sell_orders[i].quantity)

    @title("03. Проверка сортировки по убыванию цены")
    @severity('normal')
    @mark.functional
    @mark.positive
    @mark.not_parallel
    @mark.parametrize("count_buy,count_sell", [(10, 10)])
    def test_check_sorted_orderbook(self, count_buy, count_sell, clean_orderbook_ft, prepare_temporary_order_list):
        """
        Предусловия: Нет
        Описание: В тест-кейсе проверяем, что заявки на покупку и продажу сортируются по убыванию цены
        """
        buy_orders, sell_orders = prepare_temporary_order_list
        buy_prices, sell_prices = [order.price for order in buy_orders], [order.price for order in sell_orders]
        buy_prices.sort(reverse=True, key=int)
        sell_prices.sort(reverse=True, key=int)

        response = MarketData(get_marketdata().json())
        with step('Проверяем, что применена сортировка заявок на покупку от большей цены к меньшей'):
            for i in range(count_buy):
                assert response.asks[i].price == buy_prices[i]
        with step('Проверяем, что применена сортировка заявок на продажу от большей цены к меньшей'):
            for i in range(count_sell):
                assert response.bids[i].price == sell_prices[i]

    @title("04. Проверка обработки запроса с методом {method}")
    @severity('minor')
    @mark.security
    @mark.parallel
    @mark.parametrize("method", ["POST", "PUT", "DELETE"])
    def test_validate_response_get_orderbook_incorrect_method(self, method):
        """
        Описание: В тест-кейсе проверяем, что сервис отвечает ошибкой на запрос /api/marketdata, если метод отличный от GET
        """
        check_status_code(OrderValidator(get_marketdata(method)), 405)

    @title("05. Проверка заголовков в ответе на запрос удаления заявки")
    @severity('minor')
    @mark.functional
    @mark.positive
    @mark.parallel
    @mark.parametrize("count_buy,count_sell", [(0, 0), (1, 1)])
    def test_validate_response_headers(self, prepare_temporary_order_list):
        """
        Описание: В тест-кейсе проверяем, что в ответе на запрос /api/marketdata приходят нужные заголовки
        """
        response = OrderValidator(get_marketdata())
        check_headers(response, {'Connection': 'close', 'Content-Type': 'application/json'})
