from src.request import sender
from allure import step


@step("Инициируем отправку запроса для очистки биржевого стакана")
def clean_orderbook(method="GET"):
    return sender.clean(method)


@step("Валидирум тело сообщения в ответе на запрос очистки биржевого стакана")
def check_clean_message_value(response):
    response.validate_message("Order book is clean.")
