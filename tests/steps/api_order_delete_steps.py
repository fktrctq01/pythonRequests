from src.request import sender
from allure import step


@step("Инициируем отправку запроса удаления заявки на покупку или продажу")
def delete_order(id, method="DELETE"):
    return sender.delete_order(id, method)
