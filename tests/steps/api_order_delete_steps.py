from src.request import sender
from allure import step


@step("Инициируем отправку запроса удаления заказа /api/order")
def delete_order(id, method="DELETE"):
    return sender.delete_order(id, method)


@step("Проверяем код ответа на запрос удаления заказа")
def check_delete_order_status_code(response, code):
    return response.validate_status_code(code)


@step("Проверяем наличие или отсутствие тела сообщения в ответе")
def check_delete_order_is_empty_body(response, flag):
    return response.is_empty_body(flag)
