# @Date   : 14.06.2022
# @Author : Alexey Khmarskiy
# @File   : api_orderbook_clean_test.py

from allure import feature, story, title, severity, step
from pytest import mark

from src.response.validator.marketdata_validator import MarketDataValidator
from src.response.validator.message_validator import MessageValidator
from tests.steps.api_orderbook_clean_steps import clean_orderbook, check_clean_message_value
from tests.steps.common_steps import check_status_code
from tests.steps.api_marketdata_steps import get_marketdata, check_marketdata_is_not_empty, \
    check_marketdata_bids_asks_count


@feature("Тестирование работы сервиса биржевого стакана")
@story("Тестирование запроса очистки стакана")
class TestApiOrderClean:

    @title("01. Валидация кода и тела ответа на запрос очистки стакана. Пустой стакан")
    @severity('normal')
    @mark.functional
    @mark.positive
    @mark.not_parallel
    def test_validate_response_clean_empty_orderbook(self):
        """
        Предусловия: Стакан заявок пуст
        Описание: В тест-кейсе проверяем, что в ответ на запрос /api/order/clean приходит код 200 и что ответ соответствует требованиям
        """
        try:
            check_marketdata_bids_asks_count(MarketDataValidator(get_marketdata()), 0, 0)
        except AssertionError:
            with step("Стакан не пуст. Инициируем запрос очистки стакана и повторно проверим стакан"):
                clean_orderbook()
                check_marketdata_bids_asks_count(MarketDataValidator(get_marketdata()), 0, 0)

        with step("Стакан пуст. Инициируем запрос очистки стакана и валидируем ответ"):
            response = MessageValidator(clean_orderbook())
            check_status_code(response, 200)
            check_clean_message_value(response)

    @title("02. Валидация кода и тела ответа на запрос очистки стакана. Наполненный стакан")
    @severity('critical')
    @mark.smoke
    @mark.functional
    @mark.positive
    @mark.not_parallel
    @mark.parametrize("count_buy,count_sell", [(1, 1)])
    def test_validate_response_clean_filled_orderbook(self, prepare_temporary_order_list):
        """
        Предусловия: Стакан заявок заполнен заявками на продажу и покупку
        Описание: В тест-кейсе проверяем, что в ответ на запрос /api/order/clean приходит код 200 и что ответ соответствует требованиям
        Убеждаемся, что стакан действительно очистился
        """
        check_marketdata_is_not_empty(MarketDataValidator(get_marketdata()))
        with step("Инициируем запрос очистки стакана и валидируем ответ"):
            response = MessageValidator(clean_orderbook())
            check_status_code(response, 200)
            check_clean_message_value(response)
        check_marketdata_bids_asks_count(MarketDataValidator(get_marketdata()), 0, 0)

    @title("03. Проверка обработки запроса с методом {method}")
    @severity('minor')
    @mark.security
    @mark.parallel
    @mark.parametrize("method", ["POST", "PUT", "DELETE"])
    def test_validate_response_clean_orderbook_incorrect_method(self, method):
        """
        Описание: В тест-кейсе проверяем, что сервис отвечает ошибкой на запрос /api/order/clean, если метод отличный от GET
        """
        check_status_code(MessageValidator(clean_orderbook(method)), 405)
