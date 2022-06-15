# @Date   : 14.06.2022
# @Author : Alexey Khmarskiy
# @File   : orderbook_clean_test.py

from allure import feature, story, title, severity, step


@feature("Тестирование работы сервиса биржевого стакана")
@story("Тестирование запроса очистки стакана")
@title("Валидация кода и тела ответа на запрос очистки стакана")
@severity('critical')
def test_check_response_body_clean_order_book():
    """
    В тест-кейсе проверяем, что в ответ на запрос /api/order/clean приходит код 200 и что ответ соответствует требованиям
    """
