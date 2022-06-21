from src.request import sender
from allure import step


@step("Инициируем отправку запроса получения заявки")
def get_order(id, method="GET"):
    return sender.get_order(id, method)


@step("Проверяем, что в теле сообщения возвращается корректная информация по заявке")
def check_body_data(response, expected_order):
    return response.validate_order(expected_order)
