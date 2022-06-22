from src.request import sender
from allure import step


@step('Инициируем отправку запроса создания заявки на бирже')
def create_order(order, method="POST"):
    return sender.create_order(order.json(), method)
