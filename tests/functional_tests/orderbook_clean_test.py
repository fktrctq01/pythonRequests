# @Date   : 14.06.2022
# @Author : Alexey Khmarskiy
# @File   : orderbook_clean_test.py

import allure

from tests.steps.global_steps import step_check_response_body_and_status_code_for_clean_order_book


@allure.feature("Тестирование работы сервиса биржевого стакана")
@allure.story("Тестирование запроса очистки стакана")
@allure.title("Валидация кода и тела ответа на запрос очистки стакана")
@allure.severity('critical')
def test_check_response_body_clean_order_book():
    """
    В тест-кейсе проверяем, что в ответ на запрос /api/order/clean приходит код 200 и что ответ соответствует требованиям
    """
    step_check_response_body_and_status_code_for_clean_order_book()
