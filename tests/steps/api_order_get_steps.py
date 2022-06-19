from src.request import sender
from allure import step


@step("Инициируем отправку запроса получения заказа /api/order")
def get_order(id, method="GET"):
    return sender.get_order(id, method)


@step("Проверяем код ответа на запрос получения заказа")
def check_get_order_status_code(response, code):
    return response.validate_status_code(code)


@step("Проверяем наличие или отсутствие тела сообщения в ответе")
def check_get_order_is_empty_body(response, flag):
    return response.is_empty_body(flag)
