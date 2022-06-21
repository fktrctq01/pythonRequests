# @Date   : 17.06.2022
# @Author : Alexey Khmarskiy
# @File   : api_order_get_test.py

from allure import feature, story, title, severity, step
from pytest import mark
from random import randint

from src.enums.order_type import OrderType
from src.response.validator.order_validator import OrderValidator
from tests.steps.api_order_get_steps import get_order, check_body_data
from tests.steps.api_order_delete_steps import delete_order
from tests.steps.common_steps import check_status_code, check_presence_a_message_body


@feature("Тестирование работы сервиса биржевого стакана")
@story("Тестирование запроса получения заказа по id")
@title("2.01. Валидация кода и тела ответа на запрос получения заказа, которого нет")
@severity('critical')
@mark.functional
@mark.positive
def test_validate_response_get_order_by_unknown_id():
    """
    Предусловия: В биржевом стакане не существует заказа, который мы пытаемся найти
    Описание: В тест-кейсе проверям, что в ответе на запрос /api/order?id=* по несуществущему id приходит код 404
    """
    id_rnd = randint(1, 9999)
    try:
        with step(f"Проверяем, существует ли в биржевом стакане заявка с номером {id_rnd}"):
            response = get_order(id_rnd)
            check_status_code(OrderValidator(response), 404)
            check_presence_a_message_body(OrderValidator(response), False)
    except AssertionError:
        with step(f"Так как найдет заказ с номером {id_rnd} - удаляем его"):
            delete_order(id_rnd)
        with step(f"Повторно проверяем, существует ли в биржевом стакане заявка с номером {id_rnd}"):
            response = get_order(id_rnd)
            check_status_code(OrderValidator(response), 404)
            check_presence_a_message_body(OrderValidator(response), False)


@feature("Тестирование работы сервиса биржевого стакана")
@story("Тестирование запроса получения заказа по id")
@title("2.02. Валидация кода и тела ответа на запрос получения заказа, который есть в стакане")
@severity('critical')
@mark.smoke
@mark.functional
@mark.positive
@mark.parametrize("id", ["1", "5000", "9999", None])
@mark.parametrize("price", ["0.01", "1", "5000.5", "9999", "9999.99", None])
@mark.parametrize("quantity", ["1", "4000", "9999"])
@mark.parametrize("side", [OrderType.SELL, OrderType.BUY])
def test_validate_response_get_order_by_id(prepare_temporary_order_by_params):
    """
    Предусловия: В биржевом стакане присутсвует заявка с нужными параметрами
    Описание: В тест-кейсе проверяем, что при запросе заявки по id в ответе выдаются ее корректные параметры
    """
    order = prepare_temporary_order_by_params
    response = get_order(order.id)
    check_status_code(OrderValidator(response), 200)
    check_body_data(OrderValidator(response), order)


@feature("Тестирование работы сервиса биржевого стакана")
@story("Тестирование запроса получения заявки по id")
@title("2.03. Обработка ошибки, при получении некорректных входных данных")
@severity('minor')
@mark.functional
@mark.negative
@mark.parametrize("id", ["-1", "-0.01", "0", "0.01", "9999.99", "10000", "10000.01", "10001", None, "id"])
def test_validate_response_get_order_by_invalid_id(id):
    """
    Предусловия: нет
    Описание: В тест-кейсе проверяем обработку запроса получения заявки по невалидному id
    """
    response = get_order(id)
    check_status_code(OrderValidator(response), 400)
    check_presence_a_message_body(OrderValidator(response), False)


@feature("Тестирование работы сервиса биржевого стакана")
@story("Тестирование запроса получения заявки по id")
@title("2.04. Проверка обработки запроса с методами отличными от GET")
@severity('minor')
@mark.security
@mark.parametrize("method", ["POST", "PUT"])
def test_validate_response_get_order_incorrect_method(method):
    """
    Описание: В тест-кейсе проверяем, что сервис отвечает ошибкой на запрос /api/order?id=*, если метод отличный от GET
    """
    response = OrderValidator(get_order("1", method))
    check_status_code(response, 405)
