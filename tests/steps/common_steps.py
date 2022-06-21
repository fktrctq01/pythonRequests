from allure import step


@step("Проверяем, что код ответа равен {code}")
def check_status_code(response, code):
    return response.validate_status_code(code)


@step("Проверяем наличие или отсутствие тела сообщения в ответе")
def check_presence_a_message_body(response, flag):
    return response.check_presence_a_message_body(flag)
