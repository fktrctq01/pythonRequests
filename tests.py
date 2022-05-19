import service
import pytest

@pytest.fixture(scope="function", autouse=True)
def before():
    # before test
    print("\n*** Test Start ***")
    service.doCleanRequest()

    yield

    # after test
    service.doCleanRequest()
    print("\n*** Test Finish ***")

def test_smoke():

    # Создаем заявку и проверям, что в ответе на запрос пришли корректные даныые
    data = {'id': '1', 'price': '100', 'quantity': '10', 'side': 'Sell'}
    response = service.doCreateOrderRequest(data)
    assert response.status_code == 200, "Статусный код при создании ордера #1 отличный от 200"
    assert response.json()["id"] == '1'
    assert response.json()["price"] == '100'
    assert response.json()["quantity"] == '10'
    assert response.json()["side"] == 'sell'

    # Создаем заявку и проверям, что в ответе на запрос пришли корректные даныые
    data = {'id': '2', 'price': '200', 'quantity': '20', 'side': 'Buy'}
    response = service.doCreateOrderRequest(data)
    assert response.status_code == 200, "Статусный код при создании ордера #2 отличный от 200"
    assert response.json()["id"] == '2'
    assert response.json()["price"] == '200'
    assert response.json()["quantity"] == '20'
    assert response.json()["side"] == 'buy'



    # Получаем маркетдату и проверяем, что обе заявки в стакане
    response = service.doGetMarkedDataRequest()
    assert response.status_code == 200, "Статусный код при получении маркетдаты отличный от 200"
    assert len(response.json()["asks"]) == 1
    assert response.json()["asks"][0]["price"] == '200'
    assert response.json()["asks"][0]["quantity"] == '20'
    assert len(response.json()["bids"]) == 1
    assert response.json()["bids"][0]["price"] == '100'
    assert response.json()["bids"][0]["quantity"] == '10'



    # Удаляем заявку и проверяем ответ
    response = service.doDeleteRequest("1")
    assert response.status_code == 200, "Статусный код при удалении ордера отличный от 200"
    assert response.json()["id"] == '1'
    assert response.json()["price"] == '100'
    assert response.json()["quantity"] == '10'
    assert response.json()["side"] == 'sell'



    # Проверяем, что одна заявка действительно удалена, а вторая на месте
    response = service.doGetRequest("1")
    assert response.status_code == 404, "Статусный код при получении удаленного ордера отличный от 404"

    response = service.doGetRequest("2")
    assert response.status_code == 200, "Статусный код при получении ордера отличный от 200"
    assert response.json()["id"] == '2'
    assert response.json()["price"] == '200'
    assert response.json()["quantity"] == '20'
    assert response.json()["side"] == 'buy'



    # Чистим стакан
    response = service.doCleanRequest()
    assert response.status_code == 200, "Статусный код при очистки стакана отличный от 200"
    assert response.json()["message"] == 'Order book is clean.'

    # Проверяем, что вторая заявка тоже удалена
    response = service.doGetRequest("2")
    assert response.status_code == 404, "Статусный код при получении удаленного ордера отличный от 404"