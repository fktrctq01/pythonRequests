from src.request import sender
from allure import step


@step("Инициируем отправку запроса получения биржевого стакана заявок")
def get_marketdata(method="GET"):
    return sender.get_marked_data(method)


@step("Проверяем, что в стакане заявок есть заявки на покупку и продажу")
def check_marketdata_is_not_empty(response):
    response.check_asks_is_not_empty().check_bids_is_not_empty()


@step("Валидируем данные о заявке на покупку в биржевом стакане")
def check_availability_of_a_bid(response, price, quantity):
    response.check_availability_of_a_bid(price, quantity)


@step("Валидируем данные о заявке на продажу в биржевом стакане")
def check_availability_of_ask(response, price, quantity):
    response.check_availability_of_ask(price, quantity)


@step("Проверяем количество заявок на покупку и продажу в биржевом стакане заявок")
def check_marketdata_bids_asks_count(response, bids_count, asks_count):
    check_marketdata_bids_count(response, bids_count)
    check_marketdata_asks_count(response, asks_count)


@step("Проверяем количество заявок на продажу в биржевом стакане заявок")
def check_marketdata_bids_count(response, count):
    response.check_bids_count(count)


@step("Проверяем количество заявок на покупку в биржевом стакане заявок")
def check_marketdata_asks_count(response, count):
    response.check_asks_count(count)
