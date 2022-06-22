from allure import step


@step("Проверяем, что код ответа равен {code}")
def check_status_code(response, code):
    return response.validate_status_code(code)


@step("Проверяем отсутствие тела сообщения в ответе")
def check_body_is_empty(response):
    return response.check_body_is_empty()


@step("Проверяем наличие тела сообщения в ответе")
def check_body_is_not_empty(response):
    return response.check_body_is_not_empty()


@step("Проверяем, что в теле сообщения возвращается корректная информация по заявке")
def check_body_data(response, expected_order):
    return response.validate_order(expected_order)
