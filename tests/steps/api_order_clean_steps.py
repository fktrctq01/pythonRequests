from src.request import sender
from allure import step


@step("Инициируем отправку запроса /api/order/clean")
def clean_orderbook(method="GET"):
    return sender.clean(method)


@step("Проверяем, что код ответа равен {code} на запрос очистки стакана")
def check_clean_status_code(response, code):
    return response.validate_status_code(code)


@step("Проверяем, что текст сообщения соответствует требованиям")
def check_clean_message_value(response):
    return response.validate_message("Order book is clean.")
