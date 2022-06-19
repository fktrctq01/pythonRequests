# @Date   : 17.06.2022
# @Author : Alexey Khmarskiy
# @File   : api_order_get_test.py

from allure import feature, story, title, severity, step
from pytest import mark

from src.response.validator.order_validator import OrderValidator
from tests.steps.api_order_get_steps import get_order, check_get_order_status_code, check_get_order_is_empty_body
from tests.steps.api_order_delete_steps import delete_order


@feature("Тестирование работы сервиса биржевого стакана")
@story("Тестирование запроса получения заказа по id")
@title("2.01. Валидация кода и тела ответа на запрос получения заказа, которого нет")
@severity('critical')
@mark.smoke
@mark.functional
@mark.positive
def test_validate_response_get_order_by_missing_id():
    """
    Предусловия: В биржевом стакане не существует заказа, который мы пытаемся найти
    Описание: В тест-кейсе проверям, что в ответе на запрос /api/order?id=* по несуществущему id приходит код 404
    """
    try:
        with step("Проверяем, существует ли в биржевом стакане заявка с номером 3457"):
            response = get_order(3457)
            check_get_order_status_code(OrderValidator(response), 404)
            check_get_order_is_empty_body(OrderValidator(response), True)
    except AssertionError:
        with step("Так как найдет заказ с номером 3457 - удаляем его"):
            delete_order(3457)
        with step("Повторно проверяем, существует ли в биржевом стакане заявка с номером 3457"):
            response = get_order(3457)
            check_get_order_status_code(OrderValidator(response), 404)
            check_get_order_is_empty_body(OrderValidator(response), True)


@feature("Тестирование работы сервиса биржевого стакана")
@story("Тестирование запроса получения заказа по id")
@title("2.02. Валидация кода и тела ответа на запрос получения заказа")
@severity('critical')
@mark.smoke
@mark.functional
@mark.positive
#TODO
def test_validate_response_get_order_by_misssing_id(prepare_temporary_rnd_order):
    """
    Предусловия: ???
    Описание: ???
    """

    order = prepare_temporary_rnd_order
    with step("Проверяем, существует ли в биржевом стакане созданная заявка"):
        response = get_order(order.id)
        check_get_order_status_code(OrderValidator(response), 200)
        check_get_order_is_empty_body(OrderValidator(response), False)

    # try:
    #     with step("Проверяем, существует ли в биржевом стакане заявка с номером 3457"):
    #         response = get_order(3457)
    #         check_get_order_status_code(OrderValidator(response), 404)
    #         check_get_order_is_empty_body(OrderValidator(response), True)
    # except AssertionError:
    #     with step("Так как найдет заказ с номером 3457 - удаляем его"):
    #         delete_order(3457)
    #     with step("Повторно проверяем, существует ли в биржевом стакане заявка с номером 3457"):
    #         response = get_order(3457)
    #         check_get_order_status_code(OrderValidator(response), 404)
    #         check_get_order_is_empty_body(OrderValidator(response), True)

