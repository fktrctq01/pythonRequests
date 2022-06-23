# @Date   : 21.06.2022
# @Author : Alexey Khmarskiy
# @File   : api_order_create_test.py

from allure import feature, story, title, severity, step
from pytest import mark, param
from allpairspy import AllPairs

from src.entity.order import Order
from src.request import sender
from src.response.validator.message_validator import MessageValidator
from src.response.validator.order_validator import OrderValidator
from src.enums.order_type import OrderType
from tests.steps.api_order_get_steps import get_order
from tests.steps.api_order_create_steps import create_order
from tests.steps.common_steps import check_status_code, check_body_data, check_body_is_not_empty


@feature("Тестирование работы сервиса биржевого стакана")
@story("Тестирование запроса создания заявки")
class TestApiCreateOrder:

    @title("01. Валидация кода и тела ответа на запрос создания заявки на покупку или продажу")
    @severity('critical')
    @mark.functional
    @mark.positive
    @mark.not_parallel
    @mark.parametrize("id,price,quantity,side", [param("1", "100", "10", OrderType.SELL, marks=mark.smoke)] + [
        value_list for value_list in AllPairs([
            ["1", "5000", "9999", None],
            ["0.01", "1", "5000.5", "9999", "9999.99", None],
            ["1", "4000", "9999"],
            [OrderType.SELL, OrderType.BUY]
        ])
    ])
    def test_check_response_body_create_order(self, id, price, quantity, side):
        """
        Предусловия: Нет
        Описание: В тест-кейсе проверяем, что запрос создания заявки обрабатыватся с различными входными параметрами
        """
        order = Order().set_id(id).set_price(price).set_quantity(quantity).set_side(side)
        response = create_order(order)
        order.set_id(id if id is not None else response.json()["id"])
        order.set_price(price if price is not None else response.json()["price"])
        check_status_code(OrderValidator(response), 200)
        check_body_data(OrderValidator(response), order)

    @title("02. Проверка реального создания заявки при отправке запроса создания заявки на покупку или продажу")
    @severity('critical')
    @mark.functional
    @mark.positive
    @mark.not_parallel
    @mark.parametrize("id,price,quantity,side", [
        value_list for value_list in AllPairs([
            ["1", "5000", "9999", None],
            ["0.01", "1", "5000.5", "9999", "9999.99", None],
            ["1", "4000", "9999"],
            [OrderType.SELL, OrderType.BUY]
        ])
    ])
    def test_check_create_order(self, id, price, quantity, side, check_order_and_delete_if_found):
        """
        Предусловия: Нет
        Описание: В тест-кейсе проверяем, что заявка реально создается после исполнения запроса создания заявки
        """
        response = create_order(Order().set_id(id).set_price(price).set_quantity(quantity).set_side(side))
        response = get_order(id if id is not None else response.json()["id"])
        check_status_code(OrderValidator(response), 200)

    @title("03. Проверка обработки запроса с методом {method}")
    @severity('minor')
    @mark.security
    @mark.parallel
    @mark.parametrize("method", ["GET", "PUT", "DELETE"])
    def test_validate_response_create_order_incorrect_method(self, method):
        """
        Описание: В тест-кейсе проверяем, что сервис отвечает ошибкой на запрос /api/order/create, если метод отличный от POST
        """
        check_status_code(OrderValidator(create_order(Order(), method)), 405)

    @title("04. Обработка ошибки, при создании заявки с некорректными входными данными")
    @severity('minor')
    @mark.functional
    @mark.negative
    @mark.parallel
    @mark.parametrize("id,price,quantity,side", [
        ("-1", "100", "10", OrderType.BUY),
        ("-0.01", "100", "10", OrderType.SELL),
        ("0", "100", "10", OrderType.BUY),
        ("0.01", "100", "10", OrderType.SELL),
        ("9999.99", "100", "10", OrderType.BUY),
        ("10000", "100", "10", OrderType.SELL),
        ("10000.01", "100", "10", OrderType.BUY),
        ("10001", "100", "10", OrderType.SELL),
        ("id", "100", "10", OrderType.BUY),

        ("1", "-1", "10", OrderType.SELL),
        ("1", "-0.01", "10", OrderType.BUY),
        ("1", "0", "10", OrderType.SELL),
        ("1", "10000", "10", OrderType.BUY),
        ("1", "10000.01", "10", OrderType.SELL),
        ("1", "10001", "10", OrderType.BUY),
        ("1", "price", "10", OrderType.SELL),

        ("1", "100", "-1", OrderType.SELL),
        ("1", "100", "-0.01", OrderType.BUY),
        ("1", "100", "0", OrderType.SELL),
        ("1", "100", "0.01", OrderType.SELL),
        ("1", "100", "9999.99", OrderType.SELL),
        ("1", "100", "10000", OrderType.BUY),
        ("1", "100", "10000.01", OrderType.SELL),
        ("1", "100", "10001", OrderType.BUY),
        ("1", "100", None, OrderType.BUY),
        ("1", "100", "quantity", OrderType.SELL)
    ])
    def test_check_response_body_create_order_with_invalid_data(self, id, price, quantity, side):
        """
        Предусловия: Нет
        Описание: В тест-кейсе проверяем, что запрос создания заявки обрабатыватся с различными входными параметрами
        """
        order = Order().set_id(id).set_price(price).set_quantity(quantity).set_side(side)
        response = create_order(order)
        check_status_code(OrderValidator(response), 400)
        check_body_is_not_empty(MessageValidator(response))
        MessageValidator(response).validate_message("Bad request")

    @title("05. Обработка запроса создания заявки с различными значениями в поле side")
    @severity('minor')
    @mark.functional
    @mark.parallel
    @mark.parametrize("side,status_code", [
        param("Buy", 400, marks=mark.negative),
        param("BUY", 400, marks=mark.negative),
        param("Sell", 400, marks=mark.negative),
        param("SELL", 400, marks=mark.negative),
        param("test", 400, marks=mark.negative),
        param(None, 400, marks=mark.negative),
        param("buy", 200, marks=mark.positive),
        param("sell", 200, marks=mark.positive)
    ])
    def test_check_create_order_with_diff_side_value(self, side, status_code):
        """
        Предусловия: Нет
        Описание: В тест-кейсе проверяем, что запрос создания заявки обрабатыватся с различными входными параметрами
        В требованиях явно есть противоречия в запросе(Buy/Sell) и в ответе (buy/sell), которые нужно уточнить
        Предполагаем, что регистр важен и обрабатываются только значения buy/sell.
        """
        body = Order().json()
        body["side"] = side

        with step('Инициируем отправку запроса создания заявки на бирже и валидируем код ответа'):
            response_create_order = sender.create_order(body)
            check_status_code(OrderValidator(response_create_order), status_code)

        if status_code == 200:
            with step('Проверяем, что в теле ответа корректно заполнено поле side'):
                OrderValidator(response_create_order).validate_side(OrderType(str(side).lower()))
            with step('Инициируем отправку запроса получения заявки на бирже по id'):
                response_get_order = sender.get_order(body["id"])
            with step('Проверяем, что в теле ответа корректно заполнено поле side'):
                OrderValidator(response_get_order).validate_side(OrderType(str(side).lower()))
        else:
            with step('Проверяем, что на невалидные входные параметры выдется корректный ответ'):
                MessageValidator(response_create_order).validate_message("Bad request")
