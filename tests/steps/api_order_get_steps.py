from src.request import sender
from allure import step


@step("Инициируем отправку запроса получения заявки")
def get_order(id, method="GET"):
    return sender.get_order(id, method)
