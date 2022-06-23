# @Date   : 17.06.2022
# @Author : Alexey Khmarskiy
# @File   : api_order_get_test.py

from allure import feature, story, title, severity, step
from pytest import mark, param
from random import randint
from allpairspy import AllPairs

from src.enums.order_type import OrderType
from src.response.validator.order_validator import OrderValidator
from tests.steps.api_order_get_steps import get_order
from tests.steps.api_order_delete_steps import delete_order
from tests.steps.common_steps import check_status_code, check_body_data, check_body_is_empty


@feature("Тестирование работы сервиса биржевого стакана")
@story("Тестирование запроса получения заявки по id")
class TestApiGetOrder:

    @title("01. Валидация кода и тела ответа на запрос получения заявки, которой нет")
    @severity('normal')
    @mark.functional
    @mark.positive
    @mark.parallel
    def test_validate_response_get_order_by_unknown_id(self):
        """
        Предусловия: В биржевом стакане не существует заявки, который мы пытаемся найти
        Описание: В тест-кейсе проверям, что в ответе на запрос /api/order?id=* по несуществущему id приходит код 404
        """
        id_rnd = randint(1, 9999)
        try:
            with step(f"Проверяем, существует ли в биржевом стакане заявка с номером {id_rnd}"):
                response = get_order(id_rnd)
                check_status_code(OrderValidator(response), 404)
                check_body_is_empty(OrderValidator(response))
        except AssertionError:
            with step(f"Так как найдет заявка с номером {id_rnd}, то удаляем ее"):
                delete_order(id_rnd)
            with step(f"Повторно проверяем, существует ли в биржевом стакане заявка с номером {id_rnd}"):
                response = get_order(id_rnd)
                check_status_code(OrderValidator(response), 404)
                check_body_is_empty(OrderValidator(response))

    @title("02. Валидация кода и тела ответа на запрос получения заявки, которая есть в стакане")
    @severity('critical')
    @mark.functional
    @mark.positive
    @mark.not_parallel
    # -------All combinations-------
    # @mark.parametrize("id", ["1", "5000", "9999", None])
    # @mark.parametrize("price", ["0.01", "1", "5000.5", "9999", "9999.99", None])
    # @mark.parametrize("quantity", ["1", "4000", "9999"])
    # @mark.parametrize("side", [OrderType.SELL, OrderType.BUY])
    # -------Pairwise auto-------
    @mark.parametrize("id,price,quantity,side", [param("1", "100", "10", OrderType.SELL, marks=mark.smoke)] + [
        value_list for value_list in AllPairs([
            ["1", "5000", "9999", None],
            ["0.01", "1", "5000.5", "9999", "9999.99", None],
            ["1", "4000", "9999"],
            [OrderType.SELL, OrderType.BUY]
        ])
    ])
    def test_validate_response_get_order_by_id(self, prepare_temporary_order_by_params):
        """
        Предусловия: В биржевом стакане присутсвует заявка с нужными параметрами
        Описание: В тест-кейсе проверяем, что при запросе заявки по id в ответе выдаются ее корректные параметры
        """
        order = prepare_temporary_order_by_params
        response = OrderValidator(get_order(order.id))
        check_status_code(response, 200)
        check_body_data(response, order)

    @title("03. Обработка ошибки, при получении некорректных входных данных")
    @severity('minor')
    @mark.functional
    @mark.negative
    @mark.parallel
    @mark.parametrize("id", ["-1", "-0.01", "0", "0.01", "9999.99", "10000", "10000.01", "10001", "id",
                             param(None, marks=mark.xfail(reason="Test don't work with mock"))])
    def test_validate_response_get_order_by_invalid_id(self, id):
        """
        Предусловия: нет
        Описание: В тест-кейсе проверяем обработку запроса получения заявки по невалидному id
        """
        response = OrderValidator(get_order(id))
        check_status_code(response, 400)
        check_body_is_empty(response)

    @title("04. Проверка обработки запроса с методом {method}")
    @severity('minor')
    @mark.security
    @mark.parallel
    @mark.parametrize("method", ["POST", "PUT"])
    def test_validate_response_get_order_incorrect_method(self, method):
        """
        Описание: В тест-кейсе проверяем, что сервис отвечает ошибкой на запрос /api/order?id=*, если метод отличный от GET
        """
        check_status_code(OrderValidator(get_order("1", method)), 405)
