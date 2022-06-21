# @Date   : 14.06.2022
# @Author : Alexey Khmarskiy
# @File   : api_orderbook_clean_test.py

from allure import feature, story, title, severity, step
from pytest import mark

from src.response.validator.marketdata_validator import MarketDataValidator
from src.response.validator.message_validator import MessageValidator
from tests.steps.api_orderbook_clean_steps import clean_orderbook, check_clean_message_value
from tests.steps.common_steps import check_status_code
from tests.steps.api_marketdata_steps import get_marketdata, check_marketdata_is_not_empty, check_marketdata_is_empty


@feature("Тестирование работы сервиса биржевого стакана")
@story("1. Тестирование запроса очистки стакана")
@title("1.01. Валидация кода и тела ответа на запрос очистки стакана. Пустой стакан")
@severity('normal')
@mark.functional
@mark.positive
def test_validate_response_clean_empty_orderbook():
    """
    Предусловия: Стакан заявок пуст
    Описание: В тест-кейсе проверяем, что в ответ на запрос /api/order/clean приходит код 200 и что ответ соответствует требованиям
    """
    try:
        with step("Получаем стакан заявок и проверяем, что он пуст"):
            check_marketdata_is_empty(MarketDataValidator(get_marketdata()))
    except AssertionError:
        with step("Стакан не пуст. Выполняем запрос очистки стакана и валидируем ответ"):
            clean_orderbook()
        with step("Получаем стакан заявок и проверяем, что он пуст"):
            check_marketdata_is_empty(MarketDataValidator(get_marketdata()))

    with step("Стакан пуст. Повторно выполняем запрос очистки стакана и валидируем ответ"):
        response = MessageValidator(clean_orderbook())
        check_status_code(response, 200)
        check_clean_message_value(response)


@feature("Тестирование работы сервиса биржевого стакана")
@story("1. Тестирование запроса очистки стакана")
@title("1.02. Валидация кода и тела ответа на запрос очистки стакана. Наполненный стакан")
@severity('critical')
@mark.smoke
@mark.functional
@mark.positive
def test_validate_response_clean_filled_orderbook(prepare_temporary_order_on_buy, prepare_temporary_order_on_sell):
    """
    Предусловия: Стакан заявок заполнен заявками на продажу и покупку
    Описание: В тест-кейсе проверяем, что в ответ на запрос /api/order/clean приходит код 200 и что ответ соответствует требованиям
    Убеждаемся, что стакан действительно очистился
    """
    with step("Получаем стакан заявок и проверяем, что он не пуст"):
        check_marketdata_is_not_empty(MarketDataValidator(get_marketdata()))
    with step("Выполняем запрос очистки стакана и валидируем ответ"):
        response = MessageValidator(clean_orderbook())
        check_status_code(response, 200)
        check_clean_message_value(response)
    with step("Получаем стакан заявок и проверяем, что он пуст"):
        check_marketdata_is_empty(MarketDataValidator(get_marketdata()))


@feature("Тестирование работы сервиса биржевого стакана")
@story("1. Тестирование запроса очистки стакана")
@title("1.03. Проверка обработки запроса с методом {method}")
@severity('minor')
@mark.security
@mark.parametrize("method", ["POST", "PUT", "DELETE"])
def test_validate_response_clean_orderbook_incorrect_method(method):
    """
    Описание: В тест-кейсе проверяем, что сервис отвечает ошибкой на запрос /api/order/clean, если метод отличный от GET
    """
    check_status_code(MessageValidator(clean_orderbook(method)), 405)
