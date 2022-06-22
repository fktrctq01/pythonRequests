from src.request import sender
from allure import step


@step("Инициируем отправку запроса получения стакана заявок")
def get_marketdata(method="GET"):
    return sender.get_marked_data(method)


@step("Проверяем, что в стакане заявок есть заявки на покупку и продажу")
def check_marketdata_is_not_empty(response):
    return response.check_asks_is_not_empty().check_bids_is_not_empty()


@step("Проверяем, что в стакане заявок есть заявка на покупку")
def check_availability_of_a_bid(response, price, quantity):
    return response.check_availability_of_a_bid(price, quantity)


@step("Проверяем, что в стакане заявок есть заявка на продажу")
def check_availability_of_ask(response, price, quantity):
    return response.check_availability_of_ask(price, quantity)


@step("Проверяем, что в стакане заявок нет заявок на покупку и продажу")
def check_marketdata_is_empty(response):
    return response.check_count_asks(0).check_count_bids(0)


@step("Проверяем, что в стакане заявок нет заявок на продажу")
def check_marketdata_bids_is_empty(response):
    return response.check_count_bids(0)


@step("Проверяем, что в стакане заявок нет заявок на покупку")
def check_marketdata_asks_is_empty(response):
    return response.check_count_asks(0)
