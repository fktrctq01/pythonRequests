# blueprints/basic_endpoints/__ini__.py
import json

from flask import Blueprint, request, Response

from jsonschema import validate, ValidationError
from src.enums.order_type import OrderType
from src.json_schemas.order import ORDER_SCHEMA
from src.entity.order import Order


blueprint = Blueprint('api', __name__, url_prefix='/mock')

orders = {}


def to_json(data):
    return json.dumps(data) + "\n"


def resp(code, data=None):
    response = Response(status=code, mimetype="application/json")
    if data is not None:
        response.response = to_json(data)
    return response


@blueprint.route('/api/order/create', methods=['POST'])
def create_order():
    try:
        validate(request.json, ORDER_SCHEMA)
        order = Order(request.json)
        orders.update({order.id: order.json()})
        return resp(200, order.json())
    except ValidationError:
        return resp(400, {
            'message': 'Bad request'
        })


@blueprint.route('/api/order', methods=['GET', 'DELETE'])
def get_and_delete_order():
    id = request.args.get("id")
    order = orders.get(id)
    if order is not None:
        if request.method == 'GET':
            return resp(200, order)
        else:
            return resp(200, orders.pop(id))
    else:
        return resp(404)


@blueprint.route('/api/order/clean')
def clean_marketdata():
    orders.clear()
    return resp(200, {
        'message': 'Order book is clean.'
    })


@blueprint.route('/api/marketdata')
def get_marketdata():
    return resp(200, {
        'asks': list({'price': element['price'], 'quantity': element['quantity']} for element in orders.values()
                     if OrderType(element["side"]) == OrderType.BUY),
        'bids': list({'price': element['price'], 'quantity': element['quantity']} for element in orders.values()
                     if OrderType(element["side"]) == OrderType.SELL),
    })
