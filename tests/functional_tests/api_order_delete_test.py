# @Date   : 21.06.2022
# @Author : Alexey Khmarskiy
# @File   : api_order_delete_test.py

from allure import feature, story, title, severity, step
from pytest import mark, param
from random import randint
from allpairspy import AllPairs

from src.enums.order_type import OrderType
from src.response.validator.order_validator import OrderValidator
from tests.steps.api_order_get_steps import get_order
from tests.steps.api_order_delete_steps import delete_order
from tests.steps.common_steps import check_status_code, check_body_data, check_body_is_empty, check_headers


@feature("Тестирование работы сервиса биржевого стакана")
@story("Тестирование запроса удаления заявки по id")
class TestApiDeleteOrder:

    @title("01. Валидация кода и тела ответа на запрос удаления заявки, которой нет")
    @severity('normal')
    @mark.functional
    @mark.positive
    @mark.parallel
    def test_validate_response_delete_order_by_unknown_id(self):
        """
        Предусловия: В биржевом стакане не существует заявки, которую мы пытаемся удалить
        Описание: В тест-кейсе проверям, что в ответе на запрос /api/order?id=* по несуществущему id приходит код 404
        """
        id_rnd = randint(1, 9999)
        try:
            with step(f"Пробуем удалить заявку с номером {id_rnd}"):
                response = OrderValidator(delete_order(id_rnd))
                check_status_code(response, 404)
                check_body_is_empty(response)
        except AssertionError:
            with step(f"Так как существовала заявка с номером {id_rnd}, то повторно выполняем запрос на удаление"):
                response = OrderValidator(delete_order(id_rnd))
                check_status_code(response, 404)
                check_body_is_empty(response)

    @title("02. Валидация кода и тела ответа на запрос удаления заявки, которая присутствует в стакане")
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
    def test_validate_response_delete_order_by_id(self, prepare_temporary_order_by_params):
        """
        Предусловия: В биржевом стакане присутсвует заявка с нужными параметрами
        Описание: В тест-кейсе проверяем, что при удалении заявки по id в ответе выдаются ее корректные параметры
        """
        with step(f"Проверяем, что существует нужная нам заявка"):
            order = prepare_temporary_order_by_params
            response = OrderValidator(get_order(order.id))
            check_status_code(response, 200)
            check_body_data(response, order)
        with step(f"Удаляем заявку и валидируем ответ"):
            response = OrderValidator(delete_order(order.id))
            check_status_code(response, 200)
            check_body_data(response, order)
        with step(f"Проверяем, что заявка действительно удалена"):
            check_status_code(OrderValidator(get_order(order.id)), 404)

    @title("03. Обработка ошибки, при удалении заявки с некорректными входными данными")
    @severity('minor')
    @mark.functional
    @mark.negative
    @mark.parallel
    @mark.parametrize("id", ["-1", "-0.01", "0", "0.01", "9999.99", "10000", "10000.01", "10001", "id",
                             param(None, marks=mark.xfail(reason="Test don't work with mock"))])
    def test_validate_response_delete_order_by_invalid_id(self, id):
        """
        Предусловия: нет
        Описание: В тест-кейсе проверяем обработку запроса получения заявки по невалидному id
        """
        response = OrderValidator(delete_order(id))
        check_status_code(response, 400)
        check_body_is_empty(response)

    @title("04. Проверка обработки запроса с методом {method}")
    @severity('minor')
    @mark.security
    @mark.parallel
    @mark.parametrize("method", ["POST", "PUT"])
    def test_validate_response_delete_order_incorrect_method(self, method):
        """
        Описание: В тест-кейсе проверяем, что сервис отвечает ошибкой на запрос /api/order?id=*, если метод отличный от GET
        """
        check_status_code(OrderValidator(delete_order("1", method)), 405)

    @title("05. Проверка заголовков в ответе на запрос удаления заявки")
    @severity('minor')
    @mark.functional
    @mark.positive
    @mark.parallel
    def test_validate_response_headers(self, prepare_temporary_rnd_order):
        """
        Описание: В тест-кейсе проверяем, что в ответе на запрос /api/order?id=* приходят нужные заголовки
        """
        order = prepare_temporary_rnd_order
        response = OrderValidator(delete_order(order.id))
        check_headers(response, {'Connection': 'close', 'Content-Type': 'application/json'})
