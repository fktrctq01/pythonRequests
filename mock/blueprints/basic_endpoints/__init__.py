# blueprints/basic_endpoints/__ini__.py
import json

from flask import Blueprint, request, Response
from random import randint

from jsonschema import validate, ValidationError
from src.enums.order_type import OrderType
from src.json_schemas.order import ORDER_SCHEMA_RQ

blueprint = Blueprint('api', __name__, url_prefix='/mock')

orderbook = {}


def generate_response(code, data=None):
    response = Response(status=code, mimetype="application/json")
    response.response = json.dumps(data) if data is not None else []
    return response


@blueprint.route('/api/order/create', methods=['POST'])
def create_order():
    body = request.json

    # Генерируем новые значения для полей id и price, так как в запросе они опциональные и могут быть не переданы
    if body.get("id", None) is None:
        body["id"] = str(randint(1, 9999))
    if body.get("price", None) is None:
        body["price"] = str(randint(1, 9999))

    try:
        validate(body, ORDER_SCHEMA_RQ)
        orderbook.update({body["id"]: body})
        return generate_response(200, body)
    except ValidationError:
        return generate_response(400, {
            'message': 'Bad request'
        })


def is_valid_id(value):
    try:
        return True if 0 < int(value) < 10000 else False
    except ValueError:
        return False


@blueprint.route('/api/order', methods=['GET', 'DELETE'])
def get_and_delete_order():
    id = request.args.get("id")
    order = orderbook.get(id)

    if not is_valid_id(id):
        return generate_response(400)
    if order is None:
        return generate_response(404)

    # Возвращаем код 200 и json, если просто GET запрос.
    # Если DELETE, то возвращаем тоже самое, но через удаление из стакана заявок
    return generate_response(200, order if request.method == 'GET' else orderbook.pop(id))


@blueprint.route('/api/order/clean')
def clean_marketdata():
    orderbook.clear()
    return generate_response(200, {
        'message': 'Order book is clean.'
    })


def take_price(element):
    return float(element["price"])


@blueprint.route('/api/marketdata')
def get_marketdata():
    # Фильтруем все предложения по признаку покупка/продажа и формируем два отдельных справочника с price и quantity
    asks = list({'price': e['price'], 'quantity': e['quantity']} for e in orderbook.values()
                if OrderType(e["side"]) is OrderType.BUY)
    bids = list({'price': e['price'], 'quantity': e['quantity']} for e in orderbook.values()
                if OrderType(e["side"]) is OrderType.SELL)

    # Сортируем по убыванию цены, согласно требованиям
    asks.sort(reverse=True, key=take_price)
    bids.sort(reverse=True, key=take_price)

    return generate_response(200, {
        'asks': asks, 'bids': bids
    })
