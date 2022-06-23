from allure import step


@step("Проверяем, что код ответа равен {code}")
def check_status_code(response, code):
    response.validate_status_code(code)


@step("Проверяем, что тело сообщения отсутствует в ответе на запрос")
def check_body_is_empty(response):
    response.check_body_is_empty()


@step("Проверяем, что тело сообщения присутствует в ответе на запрос")
def check_body_is_not_empty(response):
    response.check_body_is_not_empty()


@step("Валидируем тело сообщения и данные о заявке на покупку или продажу")
def check_body_data(response, expected_order):
    response.validate_order(expected_order)
