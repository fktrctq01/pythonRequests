# @Date   : 14.06.2022
# @Author : Alexey Khmarskiy
# @File   : orderbook_clean_test.py

from allure import feature, story, title, severity, step

from src.json_schemas.message import MESSAGE_SCHEMA
from src.request import sender
from src.response.validator.marketdata_validator import MarketDataValidator
from src.response.validator.message_validator import MessageValidator


@feature("Тестирование работы сервиса биржевого стакана")
@story("Тестирование запроса очистки стакана")
@title("Валидация кода и тела ответа на запрос очистки стакана. Пустой стакан")
@severity('critical')
def test_validate_response_clean_empty_orderbook():
    """
    Предусловия: Стакан заявок пуст
    Описание: В тест-кейсе проверяем, что в ответ на запрос /api/order/clean приходит код 200 и что ответ соответствует требованиям
    """
    with step("Инициируем отправку запроса /api/order/clean"):
        response = sender.clean()
    with step("Валидируем код и тело ответа"):
        validator = MessageValidator(response)
        validator.validate_status_code(200).validate_body(MESSAGE_SCHEMA).validate_message("Order book is clean.")


@feature("Тестирование работы сервиса биржевого стакана")
@story("Тестирование запроса очистки стакана")
@title("Валидация кода и тела ответа на запрос очистки стакана. Наполненный стакан")
@severity('critical')
def test_validate_response_clean_filled_orderbook(create_and_delete_buy_order, create_and_delete_sell_order):
    """
    Предусловия: Стакан заявок заполнен заявками на продажу и покупку
    Описание: В тест-кейсе проверяем, что в ответ на запрос /api/order/clean приходит код 200 и что ответ соответствует требованиям
    Убеждаемся, что стакан действительно очистился
    """
    with step("Получаем стакан заявок"):
        validator = MarketDataValidator(sender.get_marked_data())
    with step("Проверяем, что стакан заявок не пуст"):
        validator.validate_status_code(200).check_asks_is_not_empty().check_bids_is_not_empty()
    with step("Инициируем отправку запроса /api/order/clean"):
        response = sender.clean()
    with step("Валидируем код и тело ответа"):
        validator = MessageValidator(response)
        validator.validate_status_code(200).validate_body(MESSAGE_SCHEMA).validate_message("Order book is clean.")
    with step("Повторно получаем стакан заявок"):
        validator = MarketDataValidator(sender.get_marked_data())
    with step("Проверяем, что стакан заявок пуст"):
        validator.validate_status_code(200).check_count_asks(0).check_count_bids(0)
