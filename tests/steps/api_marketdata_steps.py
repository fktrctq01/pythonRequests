from src.request import sender
from allure import step


@step("Инициируем отправку запроса получения стакана заявок")
def get_marketdata():
    return sender.get_marked_data()


@step("Проверяем, что в стакане заявок есть заявки на покупку и продажу")
def check_marketdata_is_not_empty(response):
    return response.check_asks_is_not_empty().check_bids_is_not_empty()


@step("Проверяем, что в стакане заявок нет заявок на покупку и продажу")
def check_marketdata_is_empty(response):
    return response.check_count_asks(0).check_count_bids(0)
