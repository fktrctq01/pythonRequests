from src.request import sender
from allure import step


@step("Инициируем отправку запроса очистки стакана")
def clean_orderbook(method="GET"):
    return sender.clean(method)


@step("Проверяем, что текст сообщения соответствует требованиям")
def check_clean_message_value(response):
    return response.validate_message("Order book is clean.")
