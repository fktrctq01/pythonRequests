# blueprints/basic_endpoints/__ini__.py
import json

from flask import Blueprint, request, Response

from mock.validator.order_validator import OrderValidator
from src.json_schemas.order import ORDER_SCHEMA
from src.entity.order import Order


blueprint = Blueprint('api', __name__, url_prefix='/mock')


def to_json(data):
    return json.dumps(data) + "\n"


def resp(code, data):
    return Response(
        status=code,
        mimetype="application/json",
        response=to_json(data))


# TODO
@blueprint.route('/api/order/create', methods=['POST'])
def create_order():
    if OrderValidator(request).validate_body(ORDER_SCHEMA):
        order = Order(request.json)
        return resp(200, {
            'id': '1',
            'price': '500.5',
            'quantity': '10',
            'side': 'buy'
        })
    else:
        return resp(400, {
            'message': 'Bad request'
        })


# TODO
@blueprint.route('/api/order', methods=['GET', 'DELETE'])
def get_and_delete_order():
    id = request.args.get("id")
    return resp(200, {
        'id': '1',
        'price': '500.5',
        'quantity': '10',
        'side': 'buy'
    })


# TODO
@blueprint.route('/api/order/clean')
def clean_marketdata():
    return resp(200, {
        'message': 'Order book is clean.'
    })


# TODO
@blueprint.route('/api/marketdata')
def get_marketdata():
    return resp(200, {
        'asks': [],
        'bids': [],
    })
